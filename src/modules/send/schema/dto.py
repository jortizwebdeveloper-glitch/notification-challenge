from typing import TypedDict


class SendData(TypedDict, total=False):
    to: str
    title: str
    content: str
    channle: str
    status: str
    job_id: str
    log: str | None = None
