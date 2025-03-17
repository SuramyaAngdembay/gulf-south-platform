from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Conversation, Message, User
from app.schemas.message import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse
)
from app.core.auth import get_current_user
from app.core.websocket import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all conversations for the current user
    """
    conversations = db.query(Conversation).filter(
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).order_by(Conversation.updated_at.desc()).all()
    return conversations

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new conversation with another user
    """
    # Check if conversation already exists
    existing = db.query(Conversation).filter(
        ((Conversation.user1_id == current_user.id) & (Conversation.user2_id == conversation.participant_id)) |
        ((Conversation.user1_id == conversation.participant_id) & (Conversation.user2_id == current_user.id))
    ).first()
    
    if existing:
        return existing
    
    # Create new conversation
    db_conversation = Conversation(
        user1_id=current_user.id,
        user2_id=conversation.participant_id
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all messages in a conversation
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()
    
    return messages

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message in a conversation
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db_message = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=message.content
    )
    db.add(db_message)
    
    # Update conversation's updated_at timestamp
    conversation.updated_at = db_message.created_at
    
    db.commit()
    db.refresh(db_message)
    
    # Notify other participant through WebSocket
    recipient_id = conversation.user2_id if conversation.user1_id == current_user.id else conversation.user1_id
    await manager.send_personal_message(
        recipient_id,
        {
            "type": "new_message",
            "conversation_id": conversation_id,
            "message": db_message.dict()
        }
    )
    
    return db_message

@router.post("/conversations/{conversation_id}/read")
async def mark_conversation_read(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark all messages in a conversation as read
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Update all unread messages
    db.query(Message).filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != current_user.id,
        Message.read == False
    ).update({"read": True})
    
    db.commit()
    return {"message": "Conversation marked as read"}

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete all messages first
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    # Then delete the conversation
    db.delete(conversation)
    db.commit()
    
    return {"message": "Conversation deleted"}

@router.websocket("/ws/messages/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time messaging
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket) 