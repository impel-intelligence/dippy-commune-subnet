from datetime import datetime, timezone

from pydantic import BaseModel, Field
from typing import Optional, Dict


class NodeEntry(BaseModel):
    hotkey: Optional[str] = Field(None, description="The hotkey of the node")
    ip: Optional[str] = Field(None, description="The IP address of the node")
    port: Optional[int] = Field(None, description="The port number of the node")
    initial_score: float = Field(default=0, description="The score ")
    submission_time: datetime = Field(
        default_factory=lambda: datetime(2099, 1, 1, tzinfo=timezone.utc),
        description="The time of the last submission"
    )
    submission_data: Optional[Dict[str, str]] = Field(
        None, description="The submission model reference"
    )
    def tz_update(self):
        self.submission_time = self.submission_time.replace(tzinfo=timezone.utc)

    class Config:
        json_schema_extra = {
            "example": {
                "hotkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
                "ip": "192.168.1.100",
                "port": 9769,
            }
        }
