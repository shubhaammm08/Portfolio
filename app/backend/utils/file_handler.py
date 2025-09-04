import os
import uuid
from typing import Optional, Tuple
from fastapi import UploadFile
import mimetypes
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, upload_dir: str = "/app/backend/uploads"):
        self.upload_dir = upload_dir
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.allowed_extensions = {'.pdf', '.doc', '.docx', '.txt', '.png', '.jpg', '.jpeg'}
        self.allowed_mime_types = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'image/png',
            'image/jpeg',
            'image/jpg'
        }
        
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, str]:
        """Validate uploaded file"""
        try:
            # Check file size
            if file.size > self.max_file_size:
                return False, f"File size too large. Maximum allowed: {self.max_file_size / (1024*1024):.1f}MB"
            
            # Check file extension
            if file.filename:
                _, ext = os.path.splitext(file.filename.lower())
                if ext not in self.allowed_extensions:
                    return False, f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
            
            # Check MIME type
            if file.content_type not in self.allowed_mime_types:
                return False, f"MIME type not allowed: {file.content_type}"
            
            return True, "File validation successful"
            
        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False, f"File validation failed: {str(e)}"
    
    def save_file(self, file: UploadFile, prefix: str = "contact") -> Tuple[bool, str, Optional[str]]:
        """Save uploaded file and return success status, message, and file path"""
        try:
            # Validate file first
            is_valid, message = self.validate_file(file)
            if not is_valid:
                return False, message, None
            
            # Generate unique filename
            file_ext = os.path.splitext(file.filename)[1] if file.filename else '.bin'
            unique_filename = f"{prefix}_{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
            
            logger.info(f"File saved successfully: {file_path}")
            return True, "File saved successfully", file_path
            
        except Exception as e:
            logger.error(f"File save error: {str(e)}")
            return False, f"Failed to save file: {str(e)}", None
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted successfully: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"File deletion error: {str(e)}")
            return False
    
    def get_file_info(self, file_path: str) -> dict:
        """Get file information"""
        try:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                return {
                    "filename": os.path.basename(file_path),
                    "size": stat.st_size,
                    "mime_type": mime_type,
                    "created_at": stat.st_ctime,
                    "modified_at": stat.st_mtime
                }
            return {}
        except Exception as e:
            logger.error(f"File info error: {str(e)}")
            return {}

# Create global instance
file_handler = FileHandler()