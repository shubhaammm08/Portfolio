from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid

class ContactFormRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    subject: str = Field(..., min_length=5, max_length=200, description="Subject line")
    message: str = Field(..., min_length=10, max_length=2000, description="Message content")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    company: Optional[str] = Field(None, max_length=100, description="Company name")
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('subject')
    def validate_subject(cls, v):
        if not v.strip():
            raise ValueError('Subject cannot be empty')
        return v.strip()
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()

class ContactFormResponse(BaseModel):
    id: str
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None
    company: Optional[str] = None
    submitted_at: datetime
    status: str = "pending"
    has_attachment: bool = False
    attachment_filename: Optional[str] = None

class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None
    company: Optional[str] = None
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    has_attachment: bool = False
    attachment_filename: Optional[str] = None
    attachment_path: Optional[str] = None
    attachment_size: Optional[int] = None
    attachment_type: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EmailTemplate(BaseModel):
    to_email: str
    subject: str
    html_content: str
    text_content: str
    from_name: str = "Shubham Kadam Portfolio"
    from_email: str = "noreply@shubhamkadam.dev"