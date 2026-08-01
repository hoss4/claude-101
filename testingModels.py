from anthropic import Anthropic
from datetime import datetime
from dotenv import load_dotenv  

load_dotenv()

client = Anthropic()

models = ["claude-opus-5","claude-sonnet-5","claude-haiku-4-5"]

prompt = "Explain prompt context engineering in a few sentences."

for model in models:

    start_time = datetime.now()
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {"role":"user","content": prompt},
        ],
        model=model
    )   
    time_taken = datetime.now() - start_time

    for block in message.content:
        if block.type == "text":
            print(block.text)
    print(f"Time taken for {model}: {time_taken}")