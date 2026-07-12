import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import websockets

app = FastAPI()

# CONFIGURATION
FOUNDRY_RESOURCE_NAME = os.getenv("FOUNDRY_RESOURCE_NAME", "<YOUR_FOUNDRY_RESOURCE>")
FOUNDRY_DEPLOYMENT_NAME = os.getenv("FOUNDRY_DEPLOYMENT_NAME", "gpt-realtime-translate")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    target_language = websocket.query_params.get("lang", "es")
    print(f"Initialising translation pipeline. Target language: {target_language}")
    
    azure_ws_url = f"wss://{FOUNDRY_RESOURCE_NAME}.openai.azure.com/openai/v1/realtime/translations?model={FOUNDRY_DEPLOYMENT_NAME}"
    
    try:
        token = token_provider()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        async with websockets.connect(azure_ws_url, additional_headers=headers) as azure_ws:
            print("Connected successfully to Foundry GPT-realtime-translate Endpoint.")
            
            session_update = {
                "type": "session.update",
                "session": {
                    "audio": {
                        "output": {
                            "language": target_language 
                        }
                    }
                }
            }
            await azure_ws.send(json.dumps(session_update))

            async def receive_from_azure():
                try:
                    async for message in azure_ws:
                        event = json.loads(message)
                        if event.get("type") == "session.output_transcript.delta":
                            await websocket.send_json({"text": event["delta"]})
                except Exception as e:
                    print(f"Error in Foundry read loop: {e}")

            azure_task = asyncio.create_task(receive_from_azure())

            try:
                while True:
                    base64_audio = await websocket.receive_text()
                    audio_append = {
                        "type": "session.input_audio_buffer.append",
                        "audio": base64_audio
                    }
                    await azure_ws.send(json.dumps(audio_append))
            except WebSocketDisconnect:
                print("Frontend closed stream.")
            finally:
                azure_task.cancel()
                
    except Exception as e:
        print(f"Connection failed: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)