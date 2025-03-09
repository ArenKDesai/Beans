from smolagents import DuckDuckGoSearchTool, tool
from typing import Dict, Any
import json

@tool
def read_user_data() -> Dict[str, Any]:
    """
    Allows Beans to read non-sensitive user data (so no API keys). 
    
    Args:
        user_data (Dict[str, Any]): JSON file of user data.
    
    Returns:
        Dict[str, Any]: user_data, but without sensitive data. 
    """
    with open("user_data.json", "r") as file:
        user_data = json.load(file)
    del user_data["KEYS"]
    return user_data

# Here's where we export all the tools Beans should have access to. 
tools = [
    DuckDuckGoSearchTool(),
    read_user_data
]