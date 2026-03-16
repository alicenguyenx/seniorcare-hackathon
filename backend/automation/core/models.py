from enum import StrEnum

from pydantic import BaseModel, Field


class AutomationStatus(StrEnum):
    RUNNING = "RUNNING"
    HUMAN_ASSIST_REQUIRED = "HUMAN_ASSIST_REQUIRED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AutomationTask(BaseModel):
    task_name: str
    starting_url: str
    goal: str
    navigation_hints: list[str] = Field(default_factory=list)
    profile_fields: dict[str, str] = Field(default_factory=dict)
    field_aliases: dict[str, list[str]] = Field(default_factory=dict)
    allowed_fields: list[str] = Field(default_factory=list)
    blocked_fields: list[str] = Field(default_factory=list)
    handoff_rules: list[str] = Field(default_factory=list)
    completion_rules: list[str] = Field(default_factory=list)


class AutomationRequest(BaseModel):
    task_name: str
    profile_overrides: dict[str, str] | None = None
    headless: bool = False
    keep_browser_open: bool = False
