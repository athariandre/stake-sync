"""SendGrid email service integration."""
from typing import List, Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.config import get_settings

settings = get_settings()


class SendGridService:
    """Service for sending emails via SendGrid."""
    
    def __init__(self):
        """Initialize SendGrid client."""
        api_key = settings.sendgrid_api_key
        if not api_key:
            raise ValueError("SENDGRID_API_KEY not found in environment variables")
        self.client = SendGridAPIClient(api_key)
        self.from_email = settings.sendgrid_from_email
    
    def send_update(
        self,
        recipients: List[str],
        subject: str,
        content: str,
        audience_type: str
    ) -> Dict:
        """
        Send weekly update email to recipients.
        
        Args:
            recipients: List of email addresses
            subject: Email subject line
            content: Email body content
            audience_type: Type of audience (for tracking)
            
        Returns:
            SendGrid response data
        """
        try:
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=[To(email) for email in recipients],
                subject=subject,
                html_content=Content("text/html", self._format_html_content(content))
            )
            
            response = self.client.send(message)
            
            return {
                "status_code": response.status_code,
                "body": response.body,
                "headers": dict(response.headers)
            }
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
    
    def _format_html_content(self, content: str) -> str:
        """
        Format plain text content as HTML email.
        
        Args:
            content: Plain text content
            
        Returns:
            HTML formatted content
        """
        # Convert line breaks to HTML paragraphs
        paragraphs = content.split('\n\n')
        html_paragraphs = [f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                p {{
                    margin-bottom: 1em;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 0.9em;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            {''.join(html_paragraphs)}
            <div class="footer">
                <p>This update was sent via StakeSync</p>
            </div>
        </body>
        </html>
        """
        return html
