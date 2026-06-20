```
from langgraph.checkpoint.sqlite import SqliteSaver

# In-memory SQLite (lost on restart)
with SqliteSaver.from_conn_string(":memory:") as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)

# Persistent file (survives restarts)
with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
```
