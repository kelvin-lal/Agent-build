"""
Kelvin's Agent
"""
from agent.menu import menu

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nAgent interrupted by user.")
    except Exception as e:
        print(f"Agent failed to start: {e}")