from typing import TypedDict
from langgraph import graph
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

# custom state:
class State(TypedDict):
    input: str
    user_feedback: str

# graph node methods:
def step_1(state: State):
    print("--step 1--")

def human_in_the_loop(state: State):
    print("--human in the loop--")

def step_3(state: State):
    print("--step 3--")

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_in_the_loop", human_in_the_loop)
builder.add_node("step_3", step_3)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_in_the_loop")
builder.add_edge("human_in_the_loop", "step_3")
builder.add_edge("step_3", END)

graph = builder.compile(checkpointer=MemorySaver(), interrupt_before=["human_in_the_loop"])
# due to checkpointer whatever progress is done will be stored in the memory so we can interrupt for live human feedback

def main():
    print("Hello from langgraph-persistence!")
    thread = {    # The MemorySaver checkpointer saves graph state per thread. Think of it like a session ID 
        "configurable": {
            "thread_id": 1
        }
    }
    # Without a thread_id, the checkpointer wouldn't know which saved state to look up when you resume.
    
    initial_input = {"input": "Hello world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):   # will run until interupt
        print("--first--\n",event) # stream_mode controls what data gets emitted during each step of the graph execution — not how the graph runs, just what you see as output.

    print(graph.get_state(thread).next)

    user_input = input("tell me how you want to update the state\n")

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_in_the_loop") # as_node="human_in_the_loop" is important — it tells LangGraph to treat this update as if human_in_the_loop node already ran
    #So after above call, the graph considers human_in_the_loop complete and moves past it
    # user_feedback will be the key name in the state

    print("--state after update--\n\n")
    print("--current state--\n",graph.get_state(thread))

    print("--next state--\n",graph.get_state(thread).next)

    for event in graph.stream(None, thread, stream_mode="values"): # None as input means "don't start fresh — resume from checkpoint"
        print("--second--\n",event)




if __name__ == "__main__":
    main()
