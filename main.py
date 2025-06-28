import warnings
warnings.filterwarnings('ignore')
from visualisation_2d import Visualizer2D
from visualisation_3d import Visualizer3D
from demo import create_basic_demo, create_complex_demo, create_safe_demo, create_2d_demo


def print_conflict_report(result):
    """Print a formatted conflict report"""
    print(f"Status: {result['status']}")
    print(f"Details: {result['details']}")
    
    if result['conflicts']:
        print("\nConflict Details:")
        for i, conflict in enumerate(result['conflicts'], 1):
            print(f"  Conflict {i}:")
            print(f"    Time: {conflict['time']:.1f}s")
            print(f"    Location: ({conflict['location']['x']:.1f}, {conflict['location']['y']:.1f}, {conflict['location']['z']:.1f})")
            print(f"    Minimum Distance: {conflict['distance']:.2f} units")
            print(f"    Conflicting Drone: {conflict['conflicting_drone']}")
            print(f"    Description: {conflict['description']}")


def run_basic_demo():
    """Run the basic demo scenario"""
    print("=" * 60)
    print("BASIC DEMO SCENARIO")
    print("=" * 60)
    
    system = create_basic_demo()
    
    # Check for conflicts
    print("Checking for conflicts...")
    result = system.check_conflicts()
    print_conflict_report(result)
    
    print("\nGenerating visualizations...")
    print("Close the plot windows to continue...")
    
    # 2D visualization
    viz_2d = Visualizer2D(system)
    viz_2d.plot_static()
    viz_2d.animate()
    
    # 3D visualization
    viz_3d = Visualizer3D(system)
    viz_3d.plot_static()
    viz_3d.animate()


def run_complex_demo():
    """Run the complex demo scenario"""
    print("=" * 60)
    print("COMPLEX DEMO SCENARIO")
    print("=" * 60)
    
    system = create_complex_demo()
    
    # Check for conflicts
    print("Checking for conflicts...")
    result = system.check_conflicts()
    print_conflict_report(result)
    
    print("\nGenerating visualizations...")
    print("Close the plot windows to continue...")
    
    # 2D visualization
    viz_2d = Visualizer2D(system)
    viz_2d.animate()
    
    # 3D visualization
    viz_3d = Visualizer3D(system)
    viz_3d.animate()


def run_safe_demo():
    """Run the safe demo scenario"""
    print("=" * 60)
    print("SAFE DEMO SCENARIO")
    print("=" * 60)
    
    system = create_safe_demo()
    
    # Check for conflicts
    print("Checking for conflicts...")
    result = system.check_conflicts()
    print_conflict_report(result)
    
    print("\nGenerating visualizations...")
    print("Close the plot windows to continue...")
    
    # 3D visualization
    viz_3d = Visualizer3D(system)
    viz_3d.plot_static()


def run_2d_demo():
    """Run the 2D demo scenario"""
    print("=" * 60)
    print("2D DEMO SCENARIO")
    print("=" * 60)
    
    system = create_2d_demo()
    
    # Check for conflicts
    print("Checking for conflicts...")
    result = system.check_conflicts()
    print_conflict_report(result)
    
    print("\nGenerating visualizations...")
    print("Close the plot windows to continue...")
    
    # 2D visualization
    viz_2d = Visualizer2D(system)
    viz_2d.animate()


def interactive_menu():
    """Interactive menu for demo selection"""
    while True:
        print("\n" + "=" * 60)
        print("DRONE DECONFLICTION SYSTEM DEMO")
        print("=" * 60)
        print("Select a demo scenario:")
        print("1. Basic Demo (mixed conflicts)")
        print("2. Complex Demo (multiple conflicts)")
        print("3. Safe Demo (no conflicts)")
        print("4. 2D Demo (planar flights)")
        print("5. Run All Demos")
        print("0. Exit")
        print("-" * 60)
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                run_basic_demo()
            elif choice == '2':
                run_complex_demo()
            elif choice == '3':
                run_safe_demo()
            elif choice == '4':
                run_2d_demo()
            elif choice == '5':
                run_basic_demo()
                run_complex_demo()
                run_safe_demo()
                run_2d_demo()
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # You can either run the interactive menu or run a specific demo
    
    # Interactive menu
    interactive_menu()
    
    # Or run a single demo directly:
    # run_basic_demo()