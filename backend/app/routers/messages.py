from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Message
from ..schemas import MessageCreate, MessageUpdate, Message as MessageSchema
from .products import get_current_admin

router = APIRouter(prefix="/api/messages", tags=["留言管理"])

@router.get("", response_model=List[MessageSchema])
async def get_messages(db: Session = Depends(get_db), status: Optional[str] = None):
    query = db.query(Message)
    if status:
        query = query.filter(Message.status == status)
    return query.all()

@router.get("/{message_id}", response_model=MessageSchema)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.post("", response_model=MessageSchema)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.put("/{message_id}", response_model=MessageSchema)
async def update_message(message_id: int, message: MessageUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    db_message.status = message.status
    db.commit()
    db.refresh(db_message)
    return db_message

@router.delete("/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return {"message": "Message deleted successfully"}
