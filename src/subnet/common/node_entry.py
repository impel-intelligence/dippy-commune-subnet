from pydantic import BaseModel, Field
from typing import Optional

class NodeEntry(BaseModel):
    hotkey: Optional[str] = Field(None, description="The hotkey of the node")
    ip: Optional[str] = Field(None, description="The IP address of the node")
    port: Optional[int] = Field(None, description="The port number of the node")
    score: Optional[int] = Field(None, description="The score node")
    last_block_submission: Optional[int] = Field(None, description="The block number of the last submission")

    class Config:
        json_schema_extra = {
            "example": {
                "hotkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
                "ip": "192.168.1.100",
                "port": 8080
            }
        }

