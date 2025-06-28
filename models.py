from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Waypoint:
    """Represents a waypoint with coordinates and optional timing"""
    x: float
    y: float
    z: float = 0.0  # Default altitude for 2D missions
    time: Optional[float] = None  # Time to reach this waypoint


@dataclass
class Mission:
    """Represents a drone mission with waypoints and time window"""
    waypoints: List[Waypoint]
    start_time: float
    end_time: float
    drone_id: str = "primary"


@dataclass
class Conflict:
    """Represents a detected conflict between drones"""
    location: Waypoint
    time: float
    primary_drone: str
    conflicting_drone: str
    distance: float
    description: str