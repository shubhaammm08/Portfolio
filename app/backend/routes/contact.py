from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from typing import Optional, List
import logging
from datetime import datetime

from models.contact import ContactFormRequest, ContactFormResponse, ContactMessage
from services.email_service import email_service
from utils.file_handler import file_handler
from database import db

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/contact", response_model=ContactFormResponse)
async def submit_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    phone: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """Submit contact form with optional file attachment"""
    try:
        # Validate form data
        form_data = ContactFormRequest(
            name=name,
            email=email,
            subject=subject,
            message=message,
            phone=phone,
            company=company
        )
        
        # Create contact message
        contact_message = ContactMessage(
            name=form_data.name,
            email=form_data.email,
            subject=form_data.subject,
            message=form_data.message,
            phone=form_data.phone,
            company=form_data.company,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        # Handle file upload if present
        if file and file.filename:
            is_valid, validation_message, file_path = file_handler.save_file(file, "contact")
            if not is_valid:
                raise HTTPException(status_code=400, detail=validation_message)
            
            if file_path:
                contact_message.has_attachment = True
                contact_message.attachment_filename = file.filename
                contact_message.attachment_path = file_path
                contact_message.attachment_size = file.size
                contact_message.attachment_type = file.content_type
        
        # Save to database
        result = await db.contact_messages.insert_one(contact_message.dict())
        
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to save contact message")
        
        # Prepare email data
        email_data = {
            "name": contact_message.name,
            "email": contact_message.email,
            "subject": contact_message.subject,
            "message": contact_message.message,
            "phone": contact_message.phone,
            "company": contact_message.company,
            "submitted_at": contact_message.submitted_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "has_attachment": contact_message.has_attachment,
            "attachment_filename": contact_message.attachment_filename
        }
        
        # Send notification email (non-blocking)
        try:
            notification_sent = email_service.send_contact_form_notification(email_data)
            if not notification_sent:
                logger.warning("Failed to send notification email")
        except Exception as e:
            logger.error(f"Email notification error: {str(e)}")
        
        # Send auto-reply (non-blocking)
        try:
            auto_reply_sent = email_service.send_auto_reply(email_data)
            if not auto_reply_sent:
                logger.warning("Failed to send auto-reply email")
        except Exception as e:
            logger.error(f"Auto-reply error: {str(e)}")
        
        # Return response
        return ContactFormResponse(
            id=contact_message.id,
            name=contact_message.name,
            email=contact_message.email,
            subject=contact_message.subject,
            message=contact_message.message,
            phone=contact_message.phone,
            company=contact_message.company,
            submitted_at=contact_message.submitted_at,
            status=contact_message.status,
            has_attachment=contact_message.has_attachment,
            attachment_filename=contact_message.attachment_filename
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Contact form submission error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/contact", response_model=List[ContactFormResponse])
async def get_contact_messages(
    limit: int = 50,
    skip: int = 0,
    status: Optional[str] = None
):
    """Get contact messages (admin endpoint)"""
    try:
        # Build query
        query = {}
        if status:
            query["status"] = status
        
        # Fetch from database
        cursor = db.contact_messages.find(query).skip(skip).limit(limit).sort("submitted_at", -1)
        messages = await cursor.to_list(length=limit)
        
        # Convert to response format
        return [
            ContactFormResponse(
                id=msg["id"],
                name=msg["name"],
                email=msg["email"],
                subject=msg["subject"],
                message=msg["message"],
                phone=msg.get("phone"),
                company=msg.get("company"),
                submitted_at=msg["submitted_at"],
                status=msg.get("status", "pending"),
                has_attachment=msg.get("has_attachment", False),
                attachment_filename=msg.get("attachment_filename")
            )
            for msg in messages
        ]
        
    except Exception as e:
        logger.error(f"Get contact messages error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/contact/{message_id}/status")
async def update_contact_message_status(
    message_id: str,
    status: str
):
    """Update contact message status"""
    try:
        if status not in ["pending", "read", "replied", "archived"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        result = await db.contact_messages.update_one(
            {"id": message_id},
            {"$set": {"status": status}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return {"message": "Status updated successfully", "status": status}
        
    except Exception as e:
        logger.error(f"Update status error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/contact/{message_id}")
async def delete_contact_message(message_id: str):
    """Delete contact message"""
    try:
        # Get message first to check for attachments
        message = await db.contact_messages.find_one({"id": message_id})
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Delete attachment if exists
        if message.get("attachment_path"):
            file_handler.delete_file(message["attachment_path"])
        
        # Delete from database
        result = await db.contact_messages.delete_one({"id": message_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return {"message": "Message deleted successfully"}
        
    except Exception as e:
        logger.error(f"Delete message error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")