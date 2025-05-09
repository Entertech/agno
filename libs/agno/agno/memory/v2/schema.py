import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class UserMemory:
    """Model for User Memories"""

    memory: str
    topics: Optional[List[str]] = None
    input: Optional[str] = None
    last_updated: Optional[datetime] = None
    memory_id: Optional[str] = None

    # When the topic is "Notes", the external data must be provided
    resource_uri: Optional[List[str]] = None
    resource_type: Optional[List[str]] = None

    # When the topic is "Reminders", the external data must be provided
    datetime_at: Optional[datetime] = None
    status: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.last_updated and isinstance(self.last_updated, str):
            self.last_updated = datetime.fromisoformat(self.last_updated)
        if self.datetime_at and isinstance(self.datetime_at, str):
            self.datetime_at = datetime.fromisoformat(self.datetime_at)
        _dict = {
            "memory_id": self.memory_id,
            "memory": self.memory,
            "topics": self.topics,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "input": self.input,
            "resource_uri": self.resource_uri,
            "resource_type": self.resource_type,
            "datetime_at": self.datetime_at.isoformat() if self.datetime_at else None,
            "status": self.status,
        }
        return {k: v for k, v in _dict.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserMemory":
        last_updated = data.get("last_updated")
        resource_uri = data.get("resource_uri")
        resource_type = data.get("resource_type")
        datetime_at = data.get("datetime_at")
        status = data.get("status")
        if last_updated:
            data["last_updated"] = datetime.fromisoformat(last_updated)
        if resource_uri:
            data["resource_uri"] = resource_uri
        if resource_type:
            data["resource_type"] = resource_type
        if datetime_at:
            data["datetime_at"] = datetime.fromisoformat(datetime_at)
        if status:
            data["status"] = status
        return cls(**data)


@dataclass
class Media:
    """Model for User Memories"""

    id: str
    type: str
    mime: str
    url: str

    def to_dict(self) -> Dict[str, Any]:
        _dict = {
            "id": self.id,
            "type": self.type,
            "mime": self.mime,
            "url": self.url,
        }
        return {k: v for k, v in _dict.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Media":
        return cls(**data)


class UserMemoryWithMedia(UserMemory):
    medias: Optional[List[Media]] = None

    def __init__(self, *args, **kwargs):
        if "medias" in kwargs:
            self.medias = kwargs.get("medias")
            del kwargs["medias"]
        super().__init__(*args, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        _dict = super().to_dict()
        _dict["medias"] = [media.to_dict() for media in self.medias or []]
        return _dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserMemoryWithMedia":
        medias = data.get("medias")
        data["medias"] = [Media.from_dict(media) for media in medias or []]
        return cls(**data)


if os.environ.get("AGNO_USER_MEMORY_CLASS") == "UserMemoryWithMedia":
    UserMemory = UserMemoryWithMedia


@dataclass
class SessionSummary:
    """Model for Session Summary."""

    summary: str
    topics: Optional[List[str]] = None
    last_updated: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        _dict = {
            "summary": self.summary,
            "topics": self.topics,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }
        return {k: v for k, v in _dict.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionSummary":
        last_updated = data.get("last_updated")
        if last_updated:
            data["last_updated"] = datetime.fromisoformat(last_updated)
        return cls(**data)
