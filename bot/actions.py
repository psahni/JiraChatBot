import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import json

from sample_audit_data import audit_data

def filterIssuesByStatus(args) -> list[dict]:
    """
    Filters the audit data from status
    Args:
        status: string
    Returns:
        list[dict]: returns the new list with correct status
    """
    arguments = json.loads(args)
    print("filterIssuesByStatus()", arguments)


    filtered_items = [item for item in audit_data if item["type"] == arguments.get("status")]

    return filtered_items