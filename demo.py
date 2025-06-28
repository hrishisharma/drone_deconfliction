from models import Waypoint, Mission
from deconfliction import DroneDeconflictionSystem


def create_basic_demo():
    """Create a basic demo scenario with sample missions"""
    system = DroneDeconflictionSystem(safety_buffer=10.0)
    
    # Primary mission (diagonal path)
    primary_waypoints = [
        Waypoint(0, 0, 10),
        Waypoint(50, 20, 15),
        Waypoint(100, 40, 20),
        Waypoint(150, 60, 15),
        Waypoint(200, 80, 10)
    ]
    primary_mission = Mission(primary_waypoints, start_time=0, end_time=60, drone_id="Primary")
    system.add_primary_mission(primary_mission)
    
    # Simulated flight 1 (intersects with primary)
    sim1_waypoints = [
        Waypoint(50, 0, 12),
        Waypoint(100, 30, 18),
        Waypoint(150, 60, 22),
        Waypoint(200, 90, 15)
    ]
    sim1_mission = Mission(sim1_waypoints, start_time=10, end_time=50, drone_id="Sim1")
    system.add_simulated_flight(sim1_mission)
    
    # Simulated flight 2 (safe path)
    sim2_waypoints = [
        Waypoint(0, 100, 25),
        Waypoint(50, 120, 30),
        Waypoint(100, 140, 35),
        Waypoint(150, 160, 30)
    ]
    sim2_mission = Mission(sim2_waypoints, start_time=5, end_time=55, drone_id="Sim2")
    system.add_simulated_flight(sim2_mission)
    
    # Simulated flight 3 (potential conflict)
    sim3_waypoints = [
        Waypoint(180, 20, 8),
        Waypoint(120, 40, 12),
        Waypoint(80, 60, 16),
        Waypoint(40, 80, 20)
    ]
    sim3_mission = Mission(sim3_waypoints, start_time=15, end_time=45, drone_id="Sim3")
    system.add_simulated_flight(sim3_mission)
    
    return system


def create_complex_demo():
    """Create a more complex demo scenario with multiple conflicts"""
    system = DroneDeconflictionSystem(safety_buffer=15.0)
    
    # Primary mission (figure-8 pattern)
    primary_waypoints = [
        Waypoint(0, 0, 20),
        Waypoint(30, 30, 25),
        Waypoint(60, 0, 30),
        Waypoint(90, -30, 25),
        Waypoint(120, 0, 20),
        Waypoint(90, 30, 25),
        Waypoint(60, 0, 30),
        Waypoint(30, -30, 25),
        Waypoint(0, 0, 20)
    ]
    primary_mission = Mission(primary_waypoints, start_time=0, end_time=120, drone_id="Alpha")
    system.add_primary_mission(primary_mission)
    
    # Multiple conflicting flights
    conflicts = [
        # Flight Beta - crosses primary path
        Mission([
            Waypoint(-20, -20, 22),
            Waypoint(60, 60, 28),
            Waypoint(140, 140, 35)
        ], start_time=20, end_time=80, drone_id="Beta"),
        
        # Flight Gamma - parallel but too close
        Mission([
            Waypoint(5, 5, 22),
            Waypoint(35, 35, 27),
            Waypoint(65, 5, 32),
            Waypoint(95, -25, 27),
            Waypoint(125, 5, 22)
        ], start_time=10, end_time=110, drone_id="Gamma"),
        
        # Flight Delta - crossing pattern
        Mission([
            Waypoint(120, 40, 18),
            Waypoint(60, 20, 24),
            Waypoint(0, 40, 30),
            Waypoint(-30, 20, 26)
        ], start_time=30, end_time=90, drone_id="Delta")
    ]
    
    for flight in conflicts:
        system.add_simulated_flight(flight)
    
    return system


def create_safe_demo():
    """Create a demo scenario with no conflicts"""
    system = DroneDeconflictionSystem(safety_buffer=10.0)
    
    # Primary mission (straight line)
    primary_waypoints = [
        Waypoint(0, 0, 20),
        Waypoint(100, 0, 20),
        Waypoint(200, 0, 20)
    ]
    primary_mission = Mission(primary_waypoints, start_time=0, end_time=60, drone_id="Safe1")
    system.add_primary_mission(primary_mission)
    
    # Safe flights at different altitudes and locations
    safe_flights = [
        # High altitude flight
        Mission([
            Waypoint(0, 50, 50),
            Waypoint(100, 50, 50),
            Waypoint(200, 50, 50)
        ], start_time=0, end_time=60, drone_id="Safe2"),
        
        # Low altitude flight
        Mission([
            Waypoint(0, -50, 5),
            Waypoint(100, -50, 5),
            Waypoint(200, -50, 5)
        ], start_time=10, end_time=70, drone_id="Safe3"),
        
        # Perpendicular flight at safe distance
        Mission([
            Waypoint(50, -100, 25),
            Waypoint(50, 0, 25),
            Waypoint(50, 100, 25)
        ], start_time=20, end_time=80, drone_id="Safe4")
    ]
    
    for flight in safe_flights:
        system.add_simulated_flight(flight)
    
    return system


def create_2d_demo():
    """Create a 2D demo scenario (z=0 for all waypoints)"""
    system = DroneDeconflictionSystem(safety_buffer=8.0)
    
    # Primary mission (square pattern)
    primary_waypoints = [
        Waypoint(0, 0, 0),
        Waypoint(50, 0, 0),
        Waypoint(50, 50, 0),
        Waypoint(0, 50, 0),
        Waypoint(0, 0, 0)
    ]
    primary_mission = Mission(primary_waypoints, start_time=0, end_time=80, drone_id="Square")
    system.add_primary_mission(primary_mission)
    
    # Intersecting flights
    intersecting_flights = [
        # Diagonal cross
        Mission([
            Waypoint(-10, -10, 0),
            Waypoint(60, 60, 0)
        ], start_time=15, end_time=65, drone_id="Diagonal"),
        
        # Horizontal cross
        Mission([
            Waypoint(-20, 25, 0),
            Waypoint(70, 25, 0)
        ], start_time=25, end_time=75, drone_id="Horizontal")
    ]
    
    for flight in intersecting_flights:
        system.add_simulated_flight(flight)
    
    return system