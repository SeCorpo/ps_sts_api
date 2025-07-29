from typing import Optional
from pydantic import BaseModel, model_validator

class SessionDataObject(BaseModel):
    trust_device: bool = False
    user_id: int
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    device_hash: Optional[str] = None

    @model_validator(mode="before")
    def strip_strings(cls, values: dict) -> dict:
        """ Strip whitespace and convert empty strings to None for all str fields """
        for k, v in values.items():
            if isinstance(v, str):
                v = v.strip()
                values[k] = v if v else None
        return values
