# we want to have the ability to run nodes parallely
# everything is handled by langGraph behind the scene, we just need to define our node edges so the nodes are in parallel

import operator
from typing import TypedDict, Any, Annotated
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    which: str

class ReturnNodeName:
    def __init__(self, node_name: str) -> None:   # constructor method
        self._value = node_name
    
    def __call__(self, state: State) -> Any: # __call__ — Make an Object Behave Like a Function
        print(f"Adding {self._value} to the {state['aggregate']}")
        return {"aggregate": [self._value]}

# class Greeter:
#     def __call__(self):
#         print("Hello")

# g = Greeter()

# g()


def route_bc_or_cd(state: State):
    if state['which'] == "bc":
        return ["b", "c"]
    return ["c", "d"]

builder = StateGraph(State)
builder.add_node('a', ReturnNodeName("I'm A")) #b.c langgraph wants the node function to be callable, that's why we added __call__ to the class, to be able to call it's objects like a function
builder.add_node('b', ReturnNodeName("I'm B"))
builder.add_node('c', ReturnNodeName("I'm C"))
builder.add_node('d', ReturnNodeName("I'm D"))
builder.add_node('e', ReturnNodeName("I'm E"))

builder.add_edge(START, 'a')
builder.add_conditional_edges("a", route_bc_or_cd, {
    "b": "b",
    'c': 'c',
    'd': 'd'
})
# builder.add_edge(['b', 'c', 'd'], 'e')   # This is a fan-in edge — e only starts when all nodes in the list have completed. It acts as a synchronization barrier.
# above one can't be used here as all of 3 couldn't run at same time so this won't trigger
builder.add_edge(['b', 'c'], 'e')
builder.add_edge(['c', 'd'], 'e')
builder.add_edge('e', END)

graph= builder.compile()

if __name__ == "__main__":
    # graph.invoke(input={"aggregate": [], "which": "bc"}, config={"configurable": {"thread_id": "foo"}})
    graph.invoke(input={"aggregate": [], "which": ""}, config={"configurable": {"thread_id": "foo"}})


