"""
Kelvin's Agent
"""
from checks.checkPrint import check_print
from checks.customCheck import CustomCheck

class Check:
    metric_counts = {
        "cpu": 0,
        "memory": 0,
        "disk": 0,
        "custom": 0
    } 

    def __init__(self, metric_type, metric_quantity=0):
        self.metric_type = metric_type
        self.metric_quantity = metric_quantity
        self.status = "OK" if metric_quantity > 0 else "Error"

    def print_results(self):
        check_print(self)

    def check():
        cpu_check = Check("CPU")
        memory_check = Check("Memory")
        disk_check = Check("Disk")
        custom_check = CustomCheck("Custom Check")

    def metricsCheck():
        counts = Check.metric_counts
        
        cpu_check = Check("CPU", counts["cpu"]) 
        memory_check = Check("Memory", counts["memory"])
        disk_check = Check("Disk", counts["disk"])
        custom_check = Check("Custom Check", counts["custom"])
        
        print("Status Check:\n")
        check_print(cpu_check)
        check_print(memory_check)
        check_print(disk_check)
        check_print(custom_check)
