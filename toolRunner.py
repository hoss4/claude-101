from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv  
import json

load_dotenv()

client = Anthropic()

@beta_tool
def get_weather(city):
    """
    Get the current weather for a city.
    """
    return json.dumps({"temperature": "20°C", "condition": "Sunny"})
@beta_tool
def get_forecast(city):
    """
    Get the weather forecast for the next few days for a city.
    """
    return json.dumps({
        "city": city,
        "forecast": [
            {"day": "sunday", "temperature": "95F", "condition": "sunny"},
            {"day": "monday", "temperature": "90F", "condition": "cloudy"},
            {"day": "tuesday", "temperature": "85F", "condition": "rainy"}
        ]
    })

messages = [
    {"role": "user", "content": "I am gointg on a 3 day trip to Austin, Texas. What should I pack?"},
]


result =  client.beta.messages.tool_runner(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=[get_weather, get_forecast],
    messages=messages,
)

# get final result

final_message = result.until_done()
for block in final_message.content:
    if block.type == "text":
        print(block.text)


# loop over interactions

# final_message = None
# for message in result:
#     try: 
#         final_message = message 
#         print(final_message.content[0].text)
#     except Exception as e:
#         print(f"Error: {e}")    



