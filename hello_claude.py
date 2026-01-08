import os
from anthropic import Anthropic

def main():
    """
    Sends a simple 'hello world' message to the Claude API and prints the response.
    """
    # The client automatically picks up the ANTHROPIC_API_KEY environment variable
    # or you can pass it directly: client = Anthropic(api_key="your-api-key")
    client = Anthropic()

    print("Sending request to Claude...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514", # Use the latest recommended model
	system="You are a helpful assistant.", # Correct usage as a top-level parameter
        max_tokens=10,
        messages=[
            {"role": "user", "content": "Say 'hello world' in one short sentence."}
        ]
    )
    
    # Extract and print the text content from the response
    for block in message.content:
        if block.type == "text":
            print(f"Claude: {block.text}")

if __name__ == "__main__":
    main()

