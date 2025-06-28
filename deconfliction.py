import numpy as np
from typing import List, Dict, Optional
from dataclasses import asdict

from models import Waypoint, Mission, Conflict


class DroneDeconflictionSystem:
    """Main system for drone conflict detection and management"""
    
    def __init__(self, safety_buffer: float = 10.0):
        self.safety_buffer = safety_buffer
        self.primary_mission = None
        self.simulated_flights = []
        self.conflicts = []
        
    def add_primary_mission(self, mission: Mission):
        """Add the primary drone mission"""
        self.primary_mission = mission
        self._calculate_waypoint_times(mission)
        
    def add_simulated_flight(self, mission: Mission):
        """Add a simulated drone flight"""
        self._calculate_waypoint_times(mission)
        self.simulated_flights.append(mission)
        
    def _calculate_waypoint_times(self, mission: Mission):
        """Calculate timing for waypoints if not provided"""
        if not mission.waypoints:
            return
            
        # Calculate total distance of mission
        total_distance = 0
        distances = [0]  # Distance to each waypoint from start
        
        for i in range(1, len(mission.waypoints)):
            w1, w2 = mission.waypoints[i-1], mission.waypoints[i]
            dist = np.sqrt((w2.x - w1.x)**2 + (w2.y - w1.y)**2 + (w2.z - w1.z)**2)
            total_distance += dist
            distances.append(total_distance)
        
        # Calculate time for each waypoint based on proportional distance
        mission_duration = mission.end_time - mission.start_time
        
        for i, waypoint in enumerate(mission.waypoints):
            if waypoint.time is None:
                if total_distance > 0:
                    waypoint.time = mission.start_time + (distances[i] / total_distance) * mission_duration
                else:
                    waypoint.time = mission.start_time
    
    def _interpolate_position(self, mission: Mission, time: float) -> Optional[Waypoint]:
        """Interpolate drone position at a given time"""
        waypoints = mission.waypoints
        
        if time < mission.start_time or time > mission.end_time:
            return None
            
        # Find the two waypoints to interpolate between
        for i in range(len(waypoints) - 1):
            w1, w2 = waypoints[i], waypoints[i + 1]
            if w1.time <= time <= w2.time:
                if w2.time == w1.time:
                    t = 0
                else:
                    t = (time - w1.time) / (w2.time - w1.time)
                
                return Waypoint(
                    x=w1.x + t * (w2.x - w1.x),
                    y=w1.y + t * (w2.y - w1.y),
                    z=w1.z + t * (w2.z - w1.z),
                    time=time
                )
        
        # If time is at the last waypoint or beyond
        return waypoints[-1] if waypoints else None
    
    def check_conflicts(self) -> Dict:
        """Check for conflicts between primary mission and simulated flights"""
        self.conflicts = []
        
        if not self.primary_mission or not self.simulated_flights:
            return {"status": "clear", "conflicts": [], "details": "No flights to check"}
        
        # Time resolution for checking (every 0.1 seconds)
        time_step = 0.1
        start_time = self.primary_mission.start_time
        end_time = self.primary_mission.end_time
        
        # Check conflicts at each time step
        current_time = start_time
        while current_time <= end_time:
            primary_pos = self._interpolate_position(self.primary_mission, current_time)
            
            if primary_pos is None:
                current_time += time_step
                continue
            
            # Check against all simulated flights
            for sim_flight in self.simulated_flights:
                sim_pos = self._interpolate_position(sim_flight, current_time)
                
                if sim_pos is None:
                    continue
                
                # Calculate distance
                distance = np.sqrt(
                    (primary_pos.x - sim_pos.x)**2 + 
                    (primary_pos.y - sim_pos.y)**2 + 
                    (primary_pos.z - sim_pos.z)**2
                )
                
                # Check if within safety buffer
                if distance < self.safety_buffer:
                    conflict = Conflict(
                        location=Waypoint(
                            x=(primary_pos.x + sim_pos.x) / 2,
                            y=(primary_pos.y + sim_pos.y) / 2,
                            z=(primary_pos.z + sim_pos.z) / 2
                        ),
                        time=current_time,
                        primary_drone=self.primary_mission.drone_id,
                        conflicting_drone=sim_flight.drone_id,
                        distance=distance,
                        description=f"Conflict at time {current_time:.1f}s: distance {distance:.2f} < safety buffer {self.safety_buffer}"
                    )
                    self.conflicts.append(conflict)
            
            current_time += time_step
        
        # Consolidate nearby conflicts (within 1 second and 5 units)
        consolidated_conflicts = self._consolidate_conflicts()
        
        status = "conflict detected" if consolidated_conflicts else "clear"
        
        return {
            "status": status,
            "conflicts": [asdict(c) for c in consolidated_conflicts],
            "details": f"Found {len(consolidated_conflicts)} conflict zones" if consolidated_conflicts else "No conflicts detected"
        }
    
    def _consolidate_conflicts(self) -> List[Conflict]:
        """Consolidate nearby conflicts to avoid spam"""
        if not self.conflicts:
            return []
        
        consolidated = []
        used = set()
        
        for i, conflict in enumerate(self.conflicts):
            if i in used:
                continue
                
            similar_conflicts = [conflict]
            used.add(i)
            
            # Find similar conflicts
            for j, other_conflict in enumerate(self.conflicts[i+1:], i+1):
                if j in used:
                    continue
                
                time_diff = abs(conflict.time - other_conflict.time)
                spatial_diff = np.sqrt(
                    (conflict.location.x - other_conflict.location.x)**2 +
                    (conflict.location.y - other_conflict.location.y)**2 +
                    (conflict.location.z - other_conflict.location.z)**2
                )
                
                if time_diff <= 1.0 and spatial_diff <= 5.0:
                    similar_conflicts.append(other_conflict)
                    used.add(j)
            
            # Create consolidated conflict
            avg_time = np.mean([c.time for c in similar_conflicts])
            avg_x = np.mean([c.location.x for c in similar_conflicts])
            avg_y = np.mean([c.location.y for c in similar_conflicts])
            avg_z = np.mean([c.location.z for c in similar_conflicts])
            min_distance = min([c.distance for c in similar_conflicts])
            
            consolidated_conflict = Conflict(
                location=Waypoint(x=avg_x, y=avg_y, z=avg_z),
                time=avg_time,
                primary_drone=conflict.primary_drone,
                conflicting_drone=conflict.conflicting_drone,
                distance=min_distance,
                description=f"Conflict zone at time {avg_time:.1f}s: minimum separation {min_distance:.2f} units"
            )
            consolidated.append(consolidated_conflict)
        
        return consolidated