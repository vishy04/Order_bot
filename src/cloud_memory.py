import modal

app = modal.App("order-memory")

agent_memory = modal.Dict.from_name("order-agent-state", create_if_missing=True)

