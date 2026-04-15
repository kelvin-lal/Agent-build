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
                        agent_thread.join()  
                case "2" | "exit" | "Exit":
                    print("Exiting...")
                    return
                case "3" | "check" | "Check":
                    checks.Check.metricsCheck()
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
                    agent_thread = threading.Thread(target=agent_module.agent, daemon=True)
                    agent_thread.start()
                case "2" | "Enter API Key" | "Enter API Key":
                    api_key = input("Enter API Key:")
                    config.set_DD_API_KEY(api_key)
                case "3" | "exit" | "Exit":
                    print("Exiting...")
                    return
                case _:
                    print("Invalid choice")
