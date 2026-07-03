import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-12345")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    
    # Supabase config
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # SMTP Email config
    SMTP_HOST = os.getenv("SMTP_HOST")
    try:
        SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        SMTP_PORT = 587
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SENDER = os.getenv("SMTP_SENDER", "noreply@bloodconnect.com")

    @classmethod
    def validate(cls):
        # Validate that essential keys are present
        warnings = []
        if not cls.SUPABASE_URL or "dummy-project" in cls.SUPABASE_URL:
            warnings.append("SUPABASE_URL is not configured or is using the dummy placeholder.")
        if not cls.SUPABASE_KEY or "dummy-service-role" in cls.SUPABASE_KEY:
            warnings.append("SUPABASE_KEY is not configured or is using the dummy placeholder.")
        
        if warnings:
            print("\n" + "="*60)
            print("  SUPABASE CONFIGURATION WARNINGS")
            print("="*60)
            for w in warnings:
                print(f" - {w}")
            print("="*60 + "\n")
