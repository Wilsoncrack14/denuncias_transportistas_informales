from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import logging
import os
from dotenv import load_dotenv
import aiosmtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service")

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

@app.post("/send-email/")
async def send_email(email_data: EmailSchema):
    """
    Sends an email using Brevo SMTP.
    """
    try:
        # Get credentials from environment variables
        smtp_server = os.getenv("BREVO_SMTP_SERVER")
        smtp_port = int(os.getenv("BREVO_PORT", 587))
        smtp_login = os.getenv("BREVO_LOGIN")
        smtp_password = os.getenv("BREVO_PASSWORD")
        sender_email = os.getenv("SENDER_EMAIL", "wilsoncueva907@gmail.com")

        if not all([smtp_server, smtp_login, smtp_password]):
            logger.warning("SMTP credentials not found. Logging email instead.")
            logger.info(f"SENDING EMAIL TO: {email_data.email}")
            return {"message": "Email logged (credentials missing)", "recipient": email_data.email}

        # Create email message
        message = EmailMessage()
        message["From"] = sender_email
        message["To"] = email_data.email
        message["Subject"] = email_data.subject
        message.set_content(email_data.message)

        # Send email
        await aiosmtplib.send(
            message,
            hostname=smtp_server,
            port=smtp_port,
            username=smtp_login,
            password=smtp_password,
            start_tls=True,
        )
        
        logger.info(f"Email sent successfully to {email_data.email}")
        return {"message": "Email sent successfully", "recipient": email_data.email}
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "Notification Service is running"}
