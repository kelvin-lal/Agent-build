"""
Kelvin's Agent
"""

def check_print(check):
    print("--------------------------------")
    print(f"{check.metric_type} Metrics:")
    print(f"Metrics Collected: {check.metric_quantity}")
    print(f"Status: {check.status}")
    print("--------------------------------")
