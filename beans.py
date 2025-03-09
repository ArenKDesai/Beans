import whisper
from smolagents import CodeAgent, LiteLLMModel, ToolCallingAgent
import json
import sys
import io
import contextlib
# local
from beans_tools import tools

# Process user_data.json
user_json_template = """{
    "Name": "",
    "Location": "",

    "KEYS": [
        {"claude-3-5-haiku-latest": ""}
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
# Beans prompt
messages = [{
    "role": "system", "content": [{"type": "text", "text":f"""

You are Beans, the snarky, sassy, and sarcastic AI Butler of {user_data['Name']}. 
You exist to serve, including your ability to run code, access the internet, etc. 
However, you also like to have a little fun with your work, so don't be too serious. 
You will have access to the content you have already computed. This will be in the 
"content" field, which is not a part of the user input. 
Also, you are limited to 100 tokens, so keep your answers short. 

"""}]
}]
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
    # Append user message
    msg_template = {"role": "user", "content": [{"type": "text", "text": user_input}]}
    messages.append(msg_template)
    
    # NOTE I doubt this is the most efficient way of doing this, and it costs
    # more queries to the API. 
    agent_buffer = io.StringIO()
    with contextlib.redirect_stdout(agent_buffer):
        BeansAgent.run(task=user_input, stream=False, reset=False, max_steps=3)
    output_string = agent_buffer.getvalue()

    # Append system message
    msg_template = {"role": "system", "content": [{"type": "text", "text": f"stdout from CodeAgent: {output_string}"}]}
    messages.append(msg_template)
    
    # Append and show response
    beans_response = Beans(messages)
    msg_template = {"role": "assistant", "content": [{"type": "text", "text": beans_response.content}]}
    print(beans_response.content)

def exit_the_stage():
    print("Beans has fallen asleep. ")
    sys.exit()