from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Status(str, Enum):
    ALIVE = "alive"
    DEAD = "dead"
    UNKNOWN = "unknown"


class Character(BaseModel):
    id: str = Field(..., description="Unique identifier for the character")
    name: str = Field(..., description="Full name of the character")
    status: Status = Field(default=Status.ALIVE, description="Current living status")
    location_id: Optional[str] = Field(default=None, description="Current location ID of the character")
    affiliations: List[str] = Field(default_factory=list, description="List of organizations or groups")
    core_memories: List[str] = Field(default_factory=list, description="Key memories/events shaping the character")


class EventScope(str, Enum):
    LOCAL = "local"
    GLOBAL = "global"


class Event(BaseModel):
    id: str = Field(..., description="Unique identifier for the event")
    name: str = Field(..., description="Name of the event")
    timestamp: str = Field(..., description="Timestamp or Era in the universe timeline")
    scope: EventScope = Field(default=EventScope.LOCAL, description="Scope of the event's impact")
    involved_entities: List[str] = Field(default_factory=list, description="List of IDs (characters, locations) involved")
    description: str = Field(..., description="Detailed description of what happened")


class Location(BaseModel):
    id: str = Field(..., description="Unique identifier for the location")
    name: str = Field(..., description="Name of the location")
    current_state: str = Field(..., description="Current status/condition of the location")
    governing_bodies: List[str] = Field(default_factory=list, description="Organizations or entities that govern this location")
