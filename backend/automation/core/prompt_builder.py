import json

from .models import AutomationTask


def build_task_prompt(task: AutomationTask) -> str:
    profile_subset = {
        field: value
        for field, value in task.profile_fields.items()
        if field in task.allowed_fields
    }

    return f"""
You are automating a senior-friendly government-assistance flow.

Task name:
{task.task_name}

Goal:
{task.goal}

Starting URL:
{task.starting_url}

Navigation hints:
{json.dumps(task.navigation_hints, indent=2)}

Approved profile fields:
{json.dumps(profile_subset, indent=2)}

Field aliases:
{json.dumps(task.field_aliases, indent=2)}

Allowed fields:
{json.dumps(task.allowed_fields, indent=2)}

Blocked fields:
{json.dumps(task.blocked_fields, indent=2)}

Human handoff rules:
{json.dumps(task.handoff_rules, indent=2)}

Instructions:
1. Open the official website at the starting URL.
2. Read the visible page and navigate toward the task goal.
3. Use the navigation hints when they match the visible UI.
4. Identify form fields semantically by label, placeholder, surrounding text, or accessibility name.
5. Fill only approved non-sensitive fields from the profile if they appear.
6. Never fill blocked fields or any value the user has not already approved.
7. If login, CAPTCHA, OTP, legal confirmation, payment, or final submit appears, stop and mark the task as HUMAN_ASSIST_REQUIRED.
8. If the page structure changes, retry using label-based and semantic element search.
9. Stop before final submission unless an explicit human confirmation is provided outside this run.

Return a structured result with:
- status
- summary
- current_url
- fields_identified
- fields_filled
- human_needed_reason
""".strip()
