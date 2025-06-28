
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deconfliction import DroneDeconflictionSystem


class Visualizer3D:
    """3D visualization handler for drone missions"""
    
    def __init__(self, system: 'DroneDeconflictionSystem'):
        self.system = system
        self.colors = ['r', 'g', 'm', 'orange', 'brown']
    
    def plot_static(self):
        """Create static 3D visualization of missions and conflicts"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        if not self.system.primary_mission:
            ax.text(0.5, 0.5, 0.5, 'No primary mission loaded', transform=ax.transAxes)
            plt.show()
            return
        
        # Plot primary mission waypoints
        primary_x = [w.x for w in self.system.primary_mission.waypoints]
        primary_y = [w.y for w in self.system.primary_mission.waypoints]
        primary_z = [w.z for w in self.system.primary_mission.waypoints]
        ax.plot(primary_x, primary_y, primary_z, 'b-o', linewidth=2, markersize=8, label='Primary Mission')
        
        # Plot simulated flights
        for i, flight in enumerate(self.system.simulated_flights):
            flight_x = [w.x for w in flight.waypoints]
            flight_y = [w.y for w in flight.waypoints]
            flight_z = [w.z for w in flight.waypoints]
            color = self.colors[i % len(self.colors)]
            ax.plot(flight_x, flight_y, flight_z, f'{color}-s', linewidth=2, markersize=6, 
                   label=f'Simulated Flight {flight.drone_id}')
        
        # Plot conflicts
        if self.system.conflicts:
            conflict_x = [c.location.x for c in self.system.conflicts]
            conflict_y = [c.location.y for c in self.system.conflicts]
            conflict_z = [c.location.z for c in self.system.conflicts]
            ax.scatter(conflict_x, conflict_y, conflict_z, c='red', s=200, marker='x', 
                      linewidth=3, label='Conflicts')
        
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate (Altitude)')
        ax.set_title('Drone Mission Deconfliction - 3D View')
        ax.legend()
        
        plt.show()
    
    def animate(self):
        """Create 3D animation of drone movements"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        if not self.system.primary_mission:
            ax.text(0.5, 0.5, 0.5, 'No primary mission loaded', transform=ax.transAxes)
            plt.show()
            return
        
        # Plot static waypoint paths first
        primary_x = [w.x for w in self.system.primary_mission.waypoints]
        primary_y = [w.y for w in self.system.primary_mission.waypoints]
        primary_z = [w.z for w in self.system.primary_mission.waypoints]
        ax.plot(primary_x, primary_y, primary_z, 'b-o', linewidth=2, markersize=8, 
               label='Primary Mission', alpha=0.3)
        
        # Plot simulated flight paths
        for i, flight in enumerate(self.system.simulated_flights):
            flight_x = [w.x for w in flight.waypoints]
            flight_y = [w.y for w in flight.waypoints]
            flight_z = [w.z for w in flight.waypoints]
            color = self.colors[i % len(self.colors)]
            ax.plot(flight_x, flight_y, flight_z, f'{color}-s', linewidth=2, markersize=6, 
                   label=f'Simulated Flight {flight.drone_id}', alpha=0.3)
        
        # Plot conflicts
        if self.system.conflicts:
            conflict_x = [c.location.x for c in self.system.conflicts]
            conflict_y = [c.location.y for c in self.system.conflicts]
            conflict_z = [c.location.z for c in self.system.conflicts]
            ax.scatter(conflict_x, conflict_y, conflict_z, c='red', s=200, marker='x', 
                      linewidth=3, label='Conflicts')
        
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate (Altitude)')
        ax.legend()
        
        # Time parameters
        start_time = self.system.primary_mission.start_time
        end_time = self.system.primary_mission.end_time
        time_step = 0.1
        times = np.arange(start_time, end_time + time_step, time_step)
        
        # Store initial number of collections (conflicts + waypoint paths)
        initial_collections = len(ax.collections)
        
        def animate_frame(frame):
            current_time = times[frame % len(times)]
            
            # Remove old drone positions (keep initial collections)
            while len(ax.collections) > initial_collections:
                ax.collections[-1].remove()
            
            # Update primary drone position
            primary_pos = self.system._interpolate_position(self.system.primary_mission, current_time)
            if primary_pos:
                ax.scatter([primary_pos.x], [primary_pos.y], [primary_pos.z], 
                          c='blue', s=200, marker='o', alpha=0.9, edgecolors='darkblue')
            
            # Update simulated drone positions
            for i, flight in enumerate(self.system.simulated_flights):
                sim_pos = self.system._interpolate_position(flight, current_time)
                if sim_pos:
                    color = self.colors[i % len(self.colors)]
                    ax.scatter([sim_pos.x], [sim_pos.y], [sim_pos.z], 
                              c=color, s=150, marker='s', alpha=0.9, 
                              edgecolors='black', linewidth=0.5)
            
            # Update title with current time
            ax.set_title(f'Drone Mission Deconfliction - 3D Animation (t={current_time:.1f}s)')
            
            return ax.collections[initial_collections:]
        
        anim = animation.FuncAnimation(fig, animate_frame, frames=len(times), 
                                     interval=100, repeat=True, blit=False)
        plt.show()
        return anim