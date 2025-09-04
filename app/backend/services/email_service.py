import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional
import logging
from jinja2 import Template

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@shubhamkadam.dev')
        self.from_name = os.getenv('FROM_NAME', 'Shubham Kadam Portfolio')
        self.to_email = os.getenv('TO_EMAIL', 'shubham.kadam@email.com')
        
    def send_contact_form_notification(self, contact_data: dict) -> bool:
        """Send notification email when contact form is submitted"""
        try:
            # Create email content
            subject = f"New Contact Form Submission: {contact_data['subject']}"
            
            html_template = """
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }
                    .content { background: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px; }
                    .field { margin-bottom: 15px; }
                    .label { font-weight: bold; color: #555; }
                    .value { background: white; padding: 10px; border-radius: 4px; border-left: 4px solid #667eea; }
                    .message-box { background: white; padding: 15px; border-radius: 4px; border-left: 4px solid #28a745; }
                    .footer { margin-top: 20px; font-size: 12px; color: #666; text-align: center; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>🚀 New Contact Form Submission</h2>
                        <p>You have received a new message from your portfolio website.</p>
                    </div>
                    <div class="content">
                        <div class="field">
                            <div class="label">Name:</div>
                            <div class="value">{{ name }}</div>
                        </div>
                        <div class="field">
                            <div class="label">Email:</div>
                            <div class="value">{{ email }}</div>
                        </div>
                        <div class="field">
                            <div class="label">Subject:</div>
                            <div class="value">{{ subject }}</div>
                        </div>
                        {% if phone %}
                        <div class="field">
                            <div class="label">Phone:</div>
                            <div class="value">{{ phone }}</div>
                        </div>
                        {% endif %}
                        {% if company %}
                        <div class="field">
                            <div class="label">Company:</div>
                            <div class="value">{{ company }}</div>
                        </div>
                        {% endif %}
                        <div class="field">
                            <div class="label">Message:</div>
                            <div class="message-box">{{ message }}</div>
                        </div>
                        {% if has_attachment %}
                        <div class="field">
                            <div class="label">Attachment:</div>
                            <div class="value">📎 {{ attachment_filename }}</div>
                        </div>
                        {% endif %}
                        <div class="field">
                            <div class="label">Submitted At:</div>
                            <div class="value">{{ submitted_at }}</div>
                        </div>
                    </div>
                    <div class="footer">
                        <p>This email was sent from your portfolio contact form.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            template = Template(html_template)
            html_content = template.render(**contact_data)
            
            # Text content
            text_content = f"""
            New Contact Form Submission
            
            Name: {contact_data['name']}
            Email: {contact_data['email']}
            Subject: {contact_data['subject']}
            Message: {contact_data['message']}
            Submitted At: {contact_data['submitted_at']}
            """
            
            return self._send_email(
                to_email=self.to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send contact form notification: {str(e)}")
            return False
    
    def send_auto_reply(self, contact_data: dict) -> bool:
        """Send auto-reply to the person who submitted the contact form"""
        try:
            subject = f"Thank you for contacting me - {contact_data['subject']}"
            
            html_template = """
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; }
                    .content { background: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px; }
                    .message-box { background: white; padding: 15px; border-radius: 4px; border-left: 4px solid #28a745; }
                    .footer { margin-top: 20px; font-size: 12px; color: #666; text-align: center; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>👋 Thank you for reaching out!</h2>
                    </div>
                    <div class="content">
                        <p>Hi {{ name }},</p>
                        <p>Thank you for contacting me through my portfolio website. I have received your message and will get back to you as soon as possible.</p>
                        
                        <div class="message-box">
                            <h4>Your Message:</h4>
                            <p><strong>Subject:</strong> {{ subject }}</p>
                            <p><strong>Message:</strong> {{ message }}</p>
                        </div>
                        
                        <p>I typically respond within 24-48 hours. In the meantime, feel free to:</p>
                        <ul>
                            <li>Check out my latest projects on <a href="https://github.com/shubham-kadam">GitHub</a></li>
                            <li>Connect with me on <a href="https://linkedin.com/in/shubham-kadam">LinkedIn</a></li>
                            <li>View my data science work on <a href="https://kaggle.com/shubhamkadam">Kaggle</a></li>
                        </ul>
                        
                        <p>Best regards,<br>
                        <strong>Shubham Kadam</strong><br>
                        Data Analyst & Developer</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated response. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            template = Template(html_template)
            html_content = template.render(**contact_data)
            
            text_content = f"""
            Hi {contact_data['name']},
            
            Thank you for contacting me through my portfolio website. I have received your message and will get back to you as soon as possible.
            
            Your Message:
            Subject: {contact_data['subject']}
            Message: {contact_data['message']}
            
            I typically respond within 24-48 hours.
            
            Best regards,
            Shubham Kadam
            Data Analyst & Developer
            """
            
            return self._send_email(
                to_email=contact_data['email'],
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send auto-reply: {str(e)}")
            return False
    
    def _send_email(self, to_email: str, subject: str, html_content: str, text_content: str, attachment_path: Optional[str] = None) -> bool:
        """Send email using SMTP"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            
            # Add text and HTML parts
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")
            
            message.attach(text_part)
            message.attach(html_part)
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(attachment_path)}'
                    )
                    message.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
                
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

# Create global instance
email_service = EmailService()