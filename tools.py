from anthropic import Anthropic
from dotenv import load_dotenv  

load_dotenv()

client = Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for",
                }
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_forecast",
        "description": "Get the weather forecast for the next few days for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": { 
                    "type": "string",
                    "description": "The city to check" 
                }
            },
            "required": ["city"]
        }
    }
]

def run_tool(name, tool_input):

    match name:
        case "get_weather":
            return f"Weather in {tool_input['city']}: 95F, sunny"
        case "get_forecast":
            return f"Forecast for {tool_input['city']}:  sunday: 95F, sunny; monday: 90F, cloudy; tuesday: 85F, rainy"


messages = [
    {"role": "user", "content": "I am gointg on a 3 day trip to Austin, Texas. What should I pack?"},
]


while True:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "end_turn":
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    if response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = run_tool(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
