from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv
import json

load_dotenv()

client = Anthropic()

@beta_tool
def weather_tool(city):
    """
    Get the current weather for a city.
    """
    return json.dumps({"temperature": "20°C", "condition": "Sunny"})

# def get_weather(city):
#     """
#     Get the current weather for a city.
#     """
#     return json.dumps({"temperature": "20°C", "condition": "Sunny"})

# weather_tool = {
#     "name": "get_weather",
#     "description": "Get the current weather for a city.",
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "city": {"type": "string", "description": "City name"}
#         },
#         "required": ["city"],
#     },
# }



response = client.beta.messages.tool_runner(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "high"},  
    tools=[weather_tool],
    messages=[
        {
            "role": "user",
            "content": "Plan a road trip out of San Francisco with two stops, "
                       "weighing weather and drive time.",
        }
    ],
)

final_message = response.until_done()
for block in final_message.content:
    if block.type == "text":
        print(block.text)




# messages = [{"role": "user", "content": "Plan a road trip out of San Francisco with two stops, weighing weather and drive time."}]

# while True:
#     response = client.messages.create(
#         model="claude-opus-5",
#         max_tokens=16000,
#         thinking={"type": "adaptive", "display": "summarized"},
#         tools=[weather_tool],
#         messages=messages,
#     )

#     # show thinking + any text this turn
#     for block in response.content:
#         if block.type == "thinking":
#             print(f"\n[Thinking]\n{block.thinking}")
#         elif block.type == "text":
#             print(f"\n[Answer]\n{block.text}")

#     if response.stop_reason != "tool_use":
#         break  # final answer reached

#     # append Claude's turn, then run each requested tool
#     messages.append({"role": "assistant", "content": response.content})
#     tool_results = []
#     for block in response.content:
#         if block.type == "tool_use":
#             result = get_weather(**block.input)  # your real function
#             tool_results.append({
#                 "type": "tool_result",
#                 "tool_use_id": block.id,
#                 "content": result,
#             })
#     messages.append({"role": "user", "content": tool_results})