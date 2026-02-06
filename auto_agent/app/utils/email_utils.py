"""
Email Utils
Email operation utilities
"""

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional


class EmailUtils:
    """Email utility class"""

    @staticmethod
    def send_email(
        smtp_server: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        from_email: str,
        to_emails: List[str],
        subject: str,
        body: str,
        is_html: bool = False,
        attachments: Optional[List[str]] = None,
    ) -> bool:
        """
        Send email

        Args:
            smtp_server: SMTP server
            smtp_port: SMTP port
            smtp_user: SMTP user
            smtp_password: SMTP password
            from_email: From email address
            to_emails: To email addresses
            subject: Email subject
            body: Email body
            is_html: Whether body is HTML
            attachments: List of attachment file paths

        Returns:
            Whether email was sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = from_email
            msg["To"] = ", ".join(to_emails)
            msg["Subject"] = subject

            # Add body
            if is_html:
                msg.attach(MIMEText(body, "html", "utf-8"))
            else:
                msg.attach(MIMEText(body, "plain", "utf-8"))

            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    try:
                        with open(attachment_path, "rb") as f:
                            part = MIMEApplication(f.read())
                            part.add_header(
                                "Content-Disposition",
                                "attachment",
                                filename=attachment_path.split("/")[-1],
                            )
                            msg.attach(part)
                    except Exception:
                        pass

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            return True
        except Exception:
            return False

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address

        Args:
            email: Email address to validate

        Returns:
            Whether email is valid
        """
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract email addresses from text

        Args:
            text: Text to extract emails from

        Returns:
            List of extracted email addresses
        """
        import re

        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        return re.findall(pattern, text)


# Global instance
email_utils = EmailUtils()
