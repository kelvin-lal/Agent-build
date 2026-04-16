"""
Kelvin's Agent
"""
import threading
from agent import agent as agent_module
import checks.checkRun as checks
from agent.config import config
from metrics.metricsConfig import metrics_config
from metrics.tags.customTags import custom_tag_store

def custom_tags_menu():
    while True:
        print("\n--- Custom Tags ---")
        tags = custom_tag_store.get_tags()
        if tags:
            print(f"Current tags: {', '.join(tags)}")
        else:
            print("Current tags: (none)")
        print("1. Add tag")
        print("2. Remove tag")
        print("3. Back")
        choice = input("Enter:")

        match choice:
            case "1":
                tag = input("Enter tag (key:value format): ")
                if custom_tag_store.add(tag):
                    print(f"Tag '{tag}' added.")
            case "2":
                tags = custom_tag_store.get_tags()
                if not tags:
                    print("No custom tags to remove.")
                    continue
                print("Select a tag to remove:")
                custom_tag_store.list_tags()
                raw = input("Enter number: ")
                try:
                    idx = int(raw) - 1
                    if 0 <= idx < len(tags):
                        removed = tags[idx]
                        custom_tag_store.remove(removed)
                        print(f"Tag '{removed}' removed.")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            case "3" | "back" | "Back":
                return
            case _:
                print("Invalid choice")


def configuration_menu():
    while True:
        print("\n--- Configuration ---")
        print(f"Metric collection interval: {metrics_config.get_collection_interval()}s (fixed)")
        print(f"Metric submission interval: {metrics_config.get_submission_interval()}s")
        print("1. Change metric submission frequency")
        print("2. Manage custom tags")
        print("3. Back")
        choice = input("Enter:")

        match choice:
            case "1":
                raw = input("Enter metric submission frequency (seconds, minimum 1.0, e.g. 1.5):")
                try:
                    interval = float(raw)
                    if interval <= 0:
                        print("Frequency must be greater than 0.")
                        continue
                    metrics_config.set_submission_interval(interval)
                    actual = metrics_config.get_submission_interval()
                    if actual != interval:
                        print(f"Value clamped to minimum {actual}s")
                    print(f"Metric submission frequency set to {actual}s")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            case "2":
                custom_tags_menu()
            case "3" | "back" | "Back":
                return
            case _:
                print("Invalid choice")


def menu(): 
    agent_thread = None
    
    while True:
      try:
        if agent_module.agent_last_error and not agent_module.agent_running:
            print("================================")
            print(f"Agent stopped due to errors ({agent_module.agent_error_count} total)")
            print(f"Last error: {agent_module.agent_last_error}")
            print("================================")
            agent_module.agent_last_error = None
            agent_module.agent_error_count = 0
            config.set_DD_API_KEY("")
            print("API Key has been cleared. Please re-enter your API Key.")

        print("Kelvin's Agent")
        
        if agent_module.agent_running:
            print("1. Stop")
            print("2. Exit")
            print("3. Status Check")
            print("4. Configuration")
            choice = input("Enter:")
            
            match choice:
                case "1" | "stop" | "Stop":  
                    agent_module.agent_running = False
                    if agent_thread:
                        try:
                            agent_thread.join(timeout=5)
                        except Exception as e:
                            print(f"[ERROR] Failed to stop agent thread: {e}")
                case "2" | "exit" | "Exit":
                    agent_module.agent_running = False
                    if agent_thread:
                        agent_thread.join(timeout=5)
                    print("Exiting...")
                    return
                case "3" | "check" | "Check":
                    try:
                        checks.Check.metricsCheck()
                    except Exception as e:
                        print(f"[ERROR] Status check failed: {e}")
                case "4" | "configuration" | "Configuration":
                    configuration_menu()
                case _:
                    print("Invalid choice")
        else:
            print("1. Start")
            print("2. Enter API Key")
            print("3. Exit")
            print("4. Configuration")
            choice = input("Enter:")
            
            match choice:
                case "1" | "start" | "Start": 
                    if config.get_DD_API_KEY() == "":
                        print("API Key not set, please enter API Key")
                        continue
                    agent_module.agent_running = True
                    try:
                        agent_thread = threading.Thread(target=agent_module.agent, daemon=True)
                        agent_thread.start()
                    except Exception as e:
                        print(f"[ERROR] Failed to start agent thread: {e}")
                        agent_module.agent_running = False
                case "2" | "Enter API Key" | "Enter API Key":
                    api_key = input("Enter API Key:")
                    config.set_DD_API_KEY(api_key)
                case "3" | "exit" | "Exit":
                    print("Exiting...")
                    return
                case "4" | "configuration" | "Configuration":
                    configuration_menu()
                case _:
                    print("Invalid choice")
      except EOFError:
            print("\nInput stream closed. Exiting...")
            agent_module.agent_running = False
            return
      except KeyboardInterrupt:
            print("\nInterrupted. Shutting down...")
            agent_module.agent_running = False
            if agent_thread:
                agent_thread.join(timeout=5)
            return
      except Exception as e:
            print(f"[ERROR] Unexpected error in menu: {e}")
