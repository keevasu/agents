from strands import Agent

# Agent automatically uses Bedrock and the default Claude model (e.g., Claude 4 Sonnet)
agent = Agent()
response = agent("who are you..")

# Or specify a specific Bedrock model ID
agent_specific = Agent(model="global.anthropic.claude-sonnet-4-5-20250929-v1:0")
response_specific = agent_specific("what model are you.?")
