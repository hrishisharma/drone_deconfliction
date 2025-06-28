import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deconfliction import DroneDeconflictionSystem


class Visualizer2D:
    """2D visualization handler for drone missions"""
    
    def __init__(self, system: 'DroneDeconflictionSystem'):
        self.system = system
        self.colors = ['r', 'g', 'm', 'orange', 'brown']
    
    def plot_static(self):
        """Create static 2D visualization of missions and conflicts"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        if not self.system.primary_mission:
            ax.text(0.5, 0.5, 'No primary mission loaded', ha='center', va='center', transform=ax.transAxes)
            plt.show()
            return
        
        # Plot primary mission waypoints
        primary_x = [w.x for w in self.system.primary_mission.waypoints]
        primary_y = [w.y for w in self.system.primary_mission.waypoints]
        ax.plot(primary_x, primary_y, 'b-o', linewidth=2, markersize=8, label='Primary Mission')
        
        # Plot simulated flights
        for i, flight in enumerate(self.system.simulated_flights):
            flight_x = [w.x for w in flight.waypoints]
            flight_y = [w.y for w in flight.waypoints]
            color = self.colors[i % len(self.colors)]
            ax.plot(flight_x, flight_y, f'{color}-s', linewidth=2, markersize=6, 
                   label=f'Simulated Flight {flight.drone_id}')
        
        # Plot conflicts
        if self.system.conflicts:
            conflict_x = [c.location.x for c in self.system.conflicts]
            conflict_y = [c.location.y for c in self.system.conflicts]
            ax.scatter(conflict_x, conflict_y, c='red', s=200, marker='x', linewidth=3, 
                      label='Conflicts', zorder=10)
            
            # Add safety buffer circles around conflicts
            for conflict in self.system.conflicts:
                circle = plt.Circle((conflict.location.x, conflict.location.y), 
                                  self.system.safety_buffer, fill=False, color='red', 
                                  linestyle='--', alpha=0.5)
                ax.add_patch(circle)
        
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Drone Mission Deconfliction - 2D View')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        plt.show()
    
    def animate(self):
        """Create 2D animation of drone movements"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        if not self.system.primary_mission:
            ax.text(0.5, 0.5, 'No primary mission loaded', ha='center', va='center', transform=ax.transAxes)
            plt.show()
            return
        
        # Plot static waypoint paths first
        primary_x = [w.x for w in self.system.primary_mission.waypoints]
        primary_y = [w.y for w in self.system.primary_mission.waypoints]
        ax.plot(primary_x, primary_y, 'b-o', linewidth=2, markersize=8, label='Primary Mission', alpha=0.3)
        
        # Plot simulated flight paths
        for i, flight in enumerate(self.system.simulated_flights):
            flight_x = [w.x for w in flight.waypoints]
            flight_y = [w.y for w in flight.waypoints]
            color = self.colors[i % len(self.colors)]
            ax.plot(flight_x, flight_y, f'{color}-s', linewidth=2, markersize=6, 
                   label=f'Simulated Flight {flight.drone_id}', alpha=0.3)
        
        # Plot conflicts
        if self.system.conflicts:
            conflict_x = [c.location.x for c in self.system.conflicts]
            conflict_y = [c.location.y for c in self.system.conflicts]
            ax.scatter(conflict_x, conflict_y, c='red', s=200, marker='x', linewidth=3, 
                      label='Conflicts', zorder=10)
        
        # Initialize drone position markers
        primary_drone, = ax.plot([], [], 'bo', markersize=12, label='Primary Drone', zorder=20)
        sim_drones = []
        
        for i, flight in enumerate(self.system.simulated_flights):
            color = self.colors[i % len(self.colors)]
            drone, = ax.plot([], [], f'{color}s', markersize=10, 
                           label=f'{flight.drone_id} Drone', zorder=20)
            sim_drones.append(drone)
        
        # Set up axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        # Time parameters
        start_time = self.system.primary_mission.start_time
        end_time = self.system.primary_mission.end_time
        time_step = 0.1
        times = np.arange(start_time, end_time + time_step, time_step)
        
        def animate_frame(frame):
            current_time = times[frame % len(times)]
            
            # Update primary drone position
            primary_pos = self.system._interpolate_position(self.system.primary_mission, current_time)
            if primary_pos:
                primary_drone.set_data([primary_pos.x], [primary_pos.y])
            else:
                primary_drone.set_data([], [])
            
            # Update simulated drone positions
            for i, (flight, drone_marker) in enumerate(zip(self.system.simulated_flights, sim_drones)):
                sim_pos = self.system._interpolate_position(flight, current_time)
                if sim_pos:
                    drone_marker.set_data([sim_pos.x], [sim_pos.y])
                else:
                    drone_marker.set_data([], [])
            
            # Update title with current time
            ax.set_title(f'Drone Mission Deconfliction - 2D Animation (t={current_time:.1f}s)')
            
            return [primary_drone] + sim_drones
        
        anim = animation.FuncAnimation(fig, animate_frame, frames=len(times), 
                                     interval=100, blit=True, repeat=True)
        plt.show()
        return anim