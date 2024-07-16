import requests
import json
import os
from graph.agents import get_plan_node, get_research_plan_node, get_grader_node, get_generator_node, get_reviewer_node
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from graph import AgentState  # avoid circular import

def send_data_to_server(data):
    print("Sending data to server:", data) 
    response = requests.post('http://127.0.0.1:5000/api/processed', json=data)
    if response.status_code == 200:
        print("Processed data sent successfully:", response.json())
    else:
        print("Error sending processed data:", response.status_code, response.text)

def process_user_input(user_input):
    print("Starting process_user_input with:", user_input)  
    planner = get_plan_node()
    researcher = get_research_plan_node()
    grader = get_grader_node()
    generator = get_generator_node()
    reviewer = get_reviewer_node()

    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner)
    workflow.add_node("research_plan", researcher)
    workflow.add_node("grader", grader)
    workflow.add_node("generate", generator)
    workflow.add_node("review", reviewer)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "research_plan")
    workflow.add_edge("research_plan", "grader")
    workflow.add_edge("grader", "generate")
    workflow.add_edge("generate", "review")

    def enough_content(state):
        if state['grading_score'] > 20 and state["search_number"] < state["max_searches"]:
            return "research_plan"
        return "generate"
    
    workflow.add_conditional_edges("grader", enough_content, {"research_plan": "research_plan", "generate": "generate"})

    def should_continue(state):
        if state['hellucination_score'] < 50 and state["revision_number"] < state["max_revisions"]:
            return "generate"
        return END

    workflow.add_conditional_edges("review", should_continue, {"generate": "generate", END: END})

    memory = SqliteSaver.from_conn_string(":memory:")
    graph = workflow.compile(checkpointer=memory)

    thread = {"configurable": {"thread_id": "1"}}

    # Process the user input
    processed_result = f"Processed: {user_input}"  
    print("Processed result:", processed_result)

    state = AgentState(
        task=processed_result,
        plan="",
        generated="", 
        content=[],
        grading_score=0, 
        revision_number=0, 
        final_review="",
        hellucination_score=0,  
        search_number=0,
        max_searches=1, # Adjust (1-2 recommendeded)
        max_revisions=1, # Adjust (1-2 recommendeded)
    )

    # Start the Graph
    for event in graph.stream(state, thread):
        print('------------------')
        # for key, value in event.items():
        #     print(key, value)
        # print('------------------')

    # Retrieve the review data from the file
    directory = os.environ.get("REVIEW_DATA_DIR", "../tests/review_save")
    filename = os.path.join(directory, "review_results.json")
    with open(filename, 'r') as file:
        saved_data = json.load(file)

    # Prepare the data to send
    data_to_send = {
        "generated": saved_data["generated"],
        "grading_score": saved_data["grading_score"],
        "hellucination_score": saved_data["hellucination_score"],
    }
    print("saved generation", saved_data["generated"])

    # Send the saved data to the server
    send_data_to_server(data_to_send)

    # Return the processed result
    return data_to_send  

if __name__ == "__main__":
    # standalone Testing
    user_input = "I want to eat healthy and lose weight but I like eating out often, especially Chinese and Jamaican food. I have a preference for American food and I'm allergic to nuts and peaches."
    result = process_user_input(user_input)
    print(result)
