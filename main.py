from anthropic import Anthropic
from dotenv import load_dotenv  

load_dotenv()

def main():
    client = Anthropic()

    message = client.messages.create(
        max_tokens=1024,
        system="you are a helpful to the pointassistant that replayes in a friendly manner and gives a short answer less than 100 words",
        messages=[
            {"role": "user","content": "i am a user and i want to know how to use the anthropic api"},

        ],
        model="claude-haiku-4-5",
    )

    for block in message.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
