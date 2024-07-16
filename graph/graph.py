def main():
    from graph.agents import get_plan_node, get_research_plan_node ,get_grader_node ,  get_generator_node , get_reviewer_node
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.sqlite import SqliteSaver
    import warnings
    planner = get_plan_node()
    researcher = get_research_plan_node()
    grader = get_grader_node()
    generator = get_generator_node()
    reviewer = get_reviewer_node()

    # Example usage
    from graph import AgentState  # Import here to avoid circular import
    
    # Initialize the Graph Builder
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner)
    workflow.add_node("research_plan", researcher)
    workflow.add_node("grader", grader)
    workflow.add_node("generate", generator)
    workflow.add_node("review", reviewer)

    # Set Entry Points and Edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "research_plan")
    workflow.add_edge("research_plan", "grader")
    # workflow.add_edge("grader", "generate")
    workflow.add_edge("generate", "review")

    # Conditional for grader node to determine if there is enough content to generate or to go get more content
    def enough_content(state):
        # print("passed enough content")
        if state['grading_score'] > 20 and state["search_number"] < state["max_searches"]:
            return "research_plan"
        print("passed enough content")
        return "generate"
    
    workflow.add_conditional_edges("grader", enough_content, {"research_plan": "research_plan", "generate": "generate"})

    # Conditional Edge for Review Node
    # Conditional to generate again or end the workflow
    def should_continue(state):
        if state['hellucination_score'] < 50 and state["revision_number"] < state["max_revisions"]:
            return "generate"
        print("FINAL STATE" , state)
        return END

    workflow.add_conditional_edges("review", should_continue, {"generate": "generate", END: END})

    # Compile the Graph
    memory = SqliteSaver.from_conn_string(":memory:")
    interrupt_after = ["research_plan", "grader", "generate", "review"]
    graph = workflow.compile(checkpointer=memory,
                            #  interrupt_after=interrupt_after
                             )
    
    thread = {"configurable": {"thread_id": "1"}}
    
    # Start the Graph
    for event in graph.stream(AgentState(
            task="I want to eat healthy and lose weight but I like eat out often espcially chinese food and jamaican food . I have a preference for american food  and I'm allergic to nuts and peaches.",
            plan="",
            generated="",
            content=[],
            grading_score=0,
            revision_number=0, 
            final_review="",
            hellucination_score=0,
            search_number = 0,
            max_searches = 2,
            max_revisions=2,
        ), thread):
        
        for v in event.values():
            print('------------------')
            print(v)
            print('------------------')

    # print(reviewer(state, use_saved_data=False))

if __name__ == "__main__":
    main()


