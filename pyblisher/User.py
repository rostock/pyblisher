from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    _id: str
    username: str
    email: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    createdBy: Optional[str] = ''
    updatedBy: Optional[str] = ''
