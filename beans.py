import whisper
from smolagents import CodeAgent, LiteLLMModel
import json
# local
from beans_tools import tools

# Process user_data.json
user_json_template = """{
    "location": "",

    "KEYS": [
        {"claude-3-5-sonnet-20241022": ""}
    ]
}"""

try:
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
except FileNotFoundError:
    with open('user_data.json', 'w') as file:
        file.write(user_json_template)

# TODO Add difference levels of Beans intelligence level
brain = "anthropic/claude-3-5-haiku-latest"
messages = []
Beans = LiteLLMModel(model_id=brain, 
                     api_key=user_data['KEYS'][brain],
                     temperature=0.4,
                     max_tokens=100)
# TODO don't assume user has the key in KEYS
BeansAgent = CodeAgent(tools=tools, 
                  model=Beans,
                  add_base_tools=True)

# Beans Library Functions
def process_user_input(user_input: str) -> str:
    """
    Takes a string of user input, returns Bean's response. 
    Uses smolagent to build the agentic framework. 

    Args:
        user_input (String): User input. Typically a question. 
    
    Returns:
        String: Beans' response. 
    """
    msg_template = {"role": "user", "content": [{"type": "text", "text": user_input}]}
    messages.append(msg_template)
    
    BeansAgent.run(task=user_input, stream=False, reset=False)