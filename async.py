# we want to have the ability to run nodes parallely
# everything is handled by langGraph behind the scene, we just need to define our node edges so the nodes are in parallel

import operator
from typing import TypedDict, Any, Annotated
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    aggregate: Annotated[list, operator.add]

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


builder = StateGraph(State)
builder.add_node('a', ReturnNodeName("I'm A")) #b.c langgraph wants the node function to be callable, that's why we added __call__ to the class, 
# to be able to call it's objects like a function
builder.add_edge(START, 'a')
builder.add_node('b', ReturnNodeName("I'm B"))
builder.add_node('c', ReturnNodeName("I'm C"))
builder.add_node('d', ReturnNodeName("I'm D"))
builder.add_edge('a', 'b')
builder.add_edge('a', 'c') # This a->b and a->c is going to cause parallel execution
builder.add_edge('b', 'd')
builder.add_edge('c', 'd')
builder.add_edge('d', END)

graph= builder.compile()

if __name__ == "__main__":
    graph.invoke(input={"aggregate": []}, config={"configurable": {"thread_id": "foo"}})

