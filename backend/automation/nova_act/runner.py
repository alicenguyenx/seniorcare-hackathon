import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from nova_act import NovaAct

from automation.core.models import AutomationStatus, AutomationTask
from automation.core.prompt_builder import build_task_prompt
from automation.core.state_machine import normalize_status

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[2]
TASKS_DIR = BASE_DIR / "automation/tasks"
OPEN_SESSIONS: dict[str, NovaAct] = {}



def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_task(task_name: str) -> AutomationTask:
    task_path = TASKS_DIR / f"{task_name}.json"
    if not task_path.exists():
        raise FileNotFoundError(f"Unsupported automation task: {task_name}")

    return AutomationTask.model_validate(_load_json(task_path))

def _result_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": [status.value for status in AutomationStatus],
            },
            "summary": {"type": "string"},
            "current_url": {"type": "string"},
            "fields_identified": {
                "type": "array",
                "items": {"type": "string"},
            },
            "fields_filled": {
                "type": "array",
                "items": {"type": "string"},
            },
            "human_needed_reason": {"type": "string"},
        },
        "required": [
            "status",
            "summary",
            "current_url",
            "fields_identified",
            "fields_filled",
        ],
        "additionalProperties": False,
    }


def _empty_result(summary: str, human_needed_reason: str = "") -> dict[str, Any]:
    return {
        "status": AutomationStatus.FAILED.value,
        "summary": summary,
        "current_url": "",
        "fields_identified": [],
        "fields_filled": [],
        "human_needed_reason": human_needed_reason,
    }


def run_automation_task(
    task_name: str,
    profile_overrides: dict[str, str] | None = None,
    *,
    headless: bool = False,
    keep_browser_open: bool = False,
) -> dict[str, Any]:
    api_key = os.getenv("NOVA_ACT_API_KEY")
    if not api_key:
        return _empty_result(
            "Missing NOVA_ACT_API_KEY environment variable.",
            "Configuration required.",
        )

    task = _load_task(task_name)

    if profile_overrides:
        task = task.model_copy(
            update={
                "profile_fields": {
                    **task.profile_fields,
                    **profile_overrides,
                }
            }
        )

    prompt = build_task_prompt(task)
    session = NovaAct(
        starting_page=task.starting_url,
        headless=headless,
        tty=False,
        nova_act_api_key=api_key,
        ignore_https_errors=True,
    )

    try:
        session.start()
        session_id = getattr(getattr(session, "dispatcher", None), "session_id", None)
        if keep_browser_open and session_id:
            OPEN_SESSIONS[str(session_id)] = session

        result = session.act_get(
            prompt,
            schema=_result_schema(),
            max_steps=40,
            timeout=240,
        )
        parsed = result.parsed_response or {}
        status = normalize_status(parsed.get("status")).value

        return {
            "status": status,
            "summary": parsed.get("summary", "No summary returned."),
            "current_url": parsed.get("current_url", ""),
            "fields_identified": parsed.get("fields_identified", []),
            "fields_filled": parsed.get("fields_filled", []),
            "human_needed_reason": parsed.get("human_needed_reason", ""),
            "session_id": str(session_id) if session_id else "",
            "raw_result": repr(result),
        }
    except Exception as exc:
        return _empty_result(
            f"Nova Act run failed: {exc}",
            "Manual takeover needed.",
        )
    finally:
        if not keep_browser_open:
            try:
                session.stop()
            except Exception:
                pass
