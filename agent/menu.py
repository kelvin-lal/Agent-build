"""
Kelvin's Agent
"""
import threading
from agent import agent as agent_module
import checks.checkRun as checks
from agent.config import config

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
                case _:
                    print("Invalid choice")
        else:
            print("1. Start")
            print("2. Enter API Key")
            print("3. Exit")
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
