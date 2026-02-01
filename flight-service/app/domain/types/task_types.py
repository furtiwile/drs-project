from typing import TypedDict, Optional, Literal


TaskStatusType = Literal['pending', 'processing', 'completed', 'failed', 'not_found']


class TaskStatus(TypedDict, total=False):
    """Type definition for task status"""
    status: TaskStatusType
    created_at: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]
    result: Optional[dict]
    error: Optional[str]


class TaskResult(TypedDict):
    """Type definition for task result"""
    task_id: str
    status: TaskStatusType
