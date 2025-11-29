import asyncio
import json
import websockets

async def test_llm_websocket():
    """
    Test client for the LLM WebSocket endpoint
    """
    # WebSocket endpoint URL
    uri = "ws://127.0.0.1:8000/api/llm/ws/chat"

    session = 'g2H7RsjFhFkBYSzfFyEYcUCWpyxqA1mlVv0YDw2H7vM'

    # Add token as query parameter
    uri_with_token = f"{uri}?token=Bearer%20{session}"

    # Request payload - adjust model as needed
    request_data = {
        "model": 'Qwen3-0.6b',  # Change to a valid model from your model_dicts
        "user_prompt": "Hello, can you explain what a WebSocket is?",
        "chat_session_id": None  # Set to an existing session ID if needed
    }

    try:
        # Connect to the WebSocket with token as query parameter
        async with websockets.connect(uri_with_token) as websocket:
            print("Connected to WebSocket")

            # Send the request
            await websocket.send(json.dumps(request_data))
            print(f"Sent request: {json.dumps(request_data, indent=2)}")

            # Receive and print responses
            while True:
                try:
                    response = await websocket.recv()
                    response_data = json.loads(response)

                    if response_data.get("type") == "chunk":
                        print(response_data['response_chunk'], end='')
                    elif response_data.get("type") == "error":
                        print(f"Error: {response_data.get('response_chunk')}")
                        break
                    elif response_data.get("type") == "message":
                        print(f"Message: {response_data.get('response_chunk')}")

                except Exception as e:
                    print(f"Connection closed: {e}")
                    break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm_websocket())
