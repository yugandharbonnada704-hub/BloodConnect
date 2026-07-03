from functools import wraps
from flask import request, g
from app.services.supabase_service import get_supabase
from app.utils.helpers import error_response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return error_response("Missing or invalid Authorization header. Expected 'Bearer <token>'", code=401)
        
        token = auth_header.split(" ")[1]
        
        # MOCK LOGIN TOKENS FOR TESTING / LOCAL RUNNING WITHOUT LIVE SUPABASE
        if token == "mock-donor-token":
            g.user = {
                "id": "00000000-0000-0000-0000-000000000001",
                "email": "donor@example.com",
                "email_confirmed_at": "2026-01-01T00:00:00Z"
            }
            g.profile = {
                "id": "00000000-0000-0000-0000-000000000001",
                "full_name": "Mock Donor User",
                "email": "donor@example.com",
                "phone_number": "+919876543210",
                "role": "donor",
                "state": "Maharashtra",
                "city": "Mumbai",
                "verification_status": "verified",
                "availability_status": "Available"
            }
            return f(*args, **kwargs)
            
        elif token == "mock-admin-token":
            g.user = {
                "id": "00000000-0000-0000-0000-000000000002",
                "email": "admin@example.com",
                "email_confirmed_at": "2026-01-01T00:00:00Z"
            }
            g.profile = {
                "id": "00000000-0000-0000-0000-000000000002",
                "full_name": "Mock Admin User",
                "email": "admin@example.com",
                "phone_number": "+919123456789",
                "role": "admin",
                "verification_status": "verified",
                "availability_status": "Available"
            }
            return f(*args, **kwargs)

        elif token == "mock-unverified-token":
            g.user = {
                "id": "00000000-0000-0000-0000-000000000003",
                "email": "unverified@example.com",
                "email_confirmed_at": None
            }
            g.profile = {
                "id": "00000000-0000-0000-0000-000000000003",
                "full_name": "Mock Unverified User",
                "email": "unverified@example.com",
                "phone_number": "+919988776655",
                "role": "donor",
                "verification_status": "pending",
                "availability_status": "Available"
            }
            return error_response("Email verification required. Please verify your email to access this feature.", code=403)

        # Real Supabase connection validation
        supabase = get_supabase()
        if not supabase:
            return error_response("Supabase connection is unconfigured. Unable to validate auth token.", code=503)
            
        try:
            user_response = supabase.auth.get_user(token)
            if not user_response or not user_response.user:
                return error_response("Invalid or expired authentication token.", code=401)
                
            user = user_response.user
            
            # Extract confirmation details
            email_confirmed_at = getattr(user, "email_confirmed_at", None)
            
            g.user = {
                "id": user.id,
                "email": user.email,
                "email_confirmed_at": email_confirmed_at
            }
            
            # Check email verification status
            if not email_confirmed_at:
                return error_response("Email verification required. Please verify your email to access this feature.", code=403)
                
            # Query user's profile details
            profile_response = supabase.table("profiles").select("*").eq("id", user.id).execute()
            if profile_response.data:
                g.profile = profile_response.data[0]
            else:
                g.profile = None
                
        except Exception as e:
            return error_response(f"Authentication failed: {str(e)}", code=401)
            
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not g.profile or g.profile.get("role") != "admin":
            return error_response("Access denied. Admin role required.", code=403)
        return f(*args, **kwargs)
    return decorated_function
