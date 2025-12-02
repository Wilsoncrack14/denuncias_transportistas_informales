from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Message
from connection_manager import manager
import json
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chat Service")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Save message to DB
            new_message = Message(sender_id=client_id, content=data)
            db.add(new_message)
            db.commit()
            
            # Broadcast message
            message_data = {
                "sender": client_id,
                "content": data,
                "timestamp": str(datetime.now())
            }
            await manager.broadcast(json.dumps(message_data))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp.desc()).limit(50).all()
    return messages

@app.get("/")
def read_root():
    return {"status": "Chat Service is running"}
