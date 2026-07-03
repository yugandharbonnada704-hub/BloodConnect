import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import Config

class EmailService:
    @staticmethod
    def send_email(to_email, subject, html_content):
        # Check if SMTP configuration is provided
        if not Config.SMTP_HOST or not Config.SMTP_USER or not Config.SMTP_PASSWORD:
            print("\n" + "="*80)
            print(f" [MOCK EMAIL SENT]")
            print(f" To: {to_email}")
            print(f" Subject: {subject}")
            print(f" Content:\n{html_content}")
            print("="*80 + "\n")
            return True
        
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = Config.SMTP_SENDER
            msg["To"] = to_email
            
            part = MIMEText(html_content, "html")
            msg.attach(part)
            
            # Connect via SMTP
            server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_SENDER, to_email, msg.as_string())
            server.quit()
            print(f"Real email sent to {to_email} successfully.")
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email} via SMTP: {e}")
            print("Printing email content to console as fallback:")
            print(f"To: {to_email}\nSubject: {subject}\nContent: {html_content}")
            return False

    @classmethod
    def send_donor_approval_email(cls, to_email, donor_name, status):
        subject = f"BloodConnect Profile Update - {status.capitalize()}"
        if status == "verified":
            html = f"""
            <h3>Dear {donor_name},</h3>
            <p>We are excited to inform you that your donor profile has been <strong>approved and verified</strong> by the administrator!</p>
            <p>You are now visible in public search results, allowing hospitals and patients to find you in case of emergencies.</p>
            <br>
            <p>Thank you for your willingness to save lives.</p>
            <p>Best regards,<br>BloodConnect Team</p>
            """
        else:
            html = f"""
            <h3>Dear {donor_name},</h3>
            <p>Your donor profile status has been updated to: <strong>{status}</strong>.</p>
            <p>Please contact the administrator or verify your profile details if any correction is needed.</p>
            <br>
            <p>Best regards,<br>BloodConnect Team</p>
            """
        return cls.send_email(to_email, subject, html)

    @classmethod
    def send_request_status_change_email(cls, to_email, requester_name, patient_name, status):
        subject = f"Blood Request Update - {status.capitalize()}"
        html = f"""
        <h3>Dear {requester_name},</h3>
        <p>The status of your blood request for patient <strong>{patient_name}</strong> has been updated to: <strong>{status}</strong>.</p>
        <p>You can check the dashboard for details.</p>
        <br>
        <p>Best regards,<br>BloodConnect Team</p>
        """
        return cls.send_email(to_email, subject, html)
