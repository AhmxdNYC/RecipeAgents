import json
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

from .prompts import PLAN_PROMPT
def plan_node(state, use_saved_data: bool = False):
    from graph import AgentState , model
    directory = os.environ.get("PLANNER_DATA_DIR", "../tests/plan_save")
    filename = os.path.join(directory, "plan_data.json")
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # use saved data if available
    if use_saved_data and os.path.exists(filename):
        print("From saved data!")
        with open(filename, 'r') as file:
            saved_data = json.load(file)
            return {"plan": saved_data["plan"]}
    
    messages = [
        SystemMessage(content=PLAN_PROMPT), 
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    
    # Saving
    with open(filename, 'w') as file:
        json.dump({"plan": response.content}, file)

    return {"plan": response.content}
# Test
# if __name__ == "__main__":
#     from graph import AgentState  # Import here to avoid circular import

#     state = AgentState(
#         task="I want to eat healthy and lose weight but I like pizza and donuts. I have a preference for greasy meals and I'm allergic to nuts and bananas.",
#         plan="", 
#         generated="", 
#         content=[], 
#         revision_number=0, 
#         max_revisions=2
#     )

#     print(plan_node(state, use_saved_data=True))