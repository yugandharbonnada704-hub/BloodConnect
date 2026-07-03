from flask import Blueprint, request, g
from app.services.supabase_service import get_supabase
from app.utils.helpers import success_response, error_response
from app.utils.validators import validate_email, validate_phone
from app.middleware import login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone_number")
    password = data.get("password")
    role = data.get("role", "donor") # Defaults to donor
    
    if not all([full_name, email, phone, password]):
        return error_response("Missing required registration fields (full_name, email, phone_number, password).")
        
    if not validate_email(email):
        return error_response("Invalid email format.")
        
    if not validate_phone(phone):
        return error_response("Invalid phone format.")
        
    supabase = get_supabase()
    if not supabase:
        # Mock registration for testing/debugging
        return success_response("Mock registration successful. Verification email sent.", {
            "user": {"email": email, "id": "00000000-0000-0000-0000-000000000001"}
        }, code=201)

    try:
        # Sign up in Supabase Auth
        # Supabase will automatically send an email verification link.
        signup_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "phone": phone,
            "options": {
                "data": {
                    "full_name": full_name,
                    "role": role
                }
            }
        })
        
        if not signup_response or not signup_response.user:
            return error_response("Registration failed. No user object returned.")
            
        user_data = {
            "id": signup_response.user.id,
            "email": signup_response.user.email,
            "role": role
        }
        return success_response("Registration successful. Verification email has been sent.", user_data, code=201)
        
    except Exception as e:
        return error_response(f"Registration failed: {str(e)}")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return error_response("Email and password are required.")
        
    supabase = get_supabase()
    if not supabase:
        # Mock login for testing/debugging
        if email == "admin@example.com":
            return success_response("Mock login successful.", {
                "access_token": "mock-admin-token",
                "user": {"email": email, "id": "00000000-0000-0000-0000-000000000002", "role": "admin"}
            })
        elif email == "unverified@example.com":
            return error_response("Email verification required. Please check your inbox.", code=403)
        else:
            return success_response("Mock login successful.", {
                "access_token": "mock-donor-token",
                "user": {"email": email, "id": "00000000-0000-0000-0000-000000000001", "role": "donor"}
            })

    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        user = auth_response.user
        session = auth_response.session
        
        if not user or not session:
            return error_response("Invalid credentials.", code=401)
            
        # Verify email confirmation
        # In Supabase Auth, email_confirmed_at indicates if verified
        email_confirmed_at = getattr(user, "email_confirmed_at", None)
        if not email_confirmed_at:
            return error_response("Email verification required. Please check your inbox.", code=403)
            
        # Fetch profile
        profile_response = supabase.table("profiles").select("*").eq("id", user.id).execute()
        role = "donor"
        profile = None
        if profile_response.data:
            profile = profile_response.data[0]
            role = profile.get("role", "donor")
            
        return success_response("Login successful.", {
            "access_token": session.access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": role,
                "profile": profile
            }
        })
        
    except Exception as e:
        return error_response(f"Login failed: {str(e)}", code=401)

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return error_response("Email is required.")
        
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock recovery email sent.")
        
    try:
        supabase.auth.reset_password_email(email)
        return success_response("Password reset email has been sent.")
    except Exception as e:
        return error_response(f"Failed to request password reset: {str(e)}")

@auth_bp.route("/reset-password", methods=["POST"])
@login_required
def reset_password():
    data = request.get_json() or {}
    new_password = data.get("password")
    if not new_password:
        return error_response("New password is required.")
        
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock password reset successful.")
        
    try:
        # Update user password using the current session
        # Supabase API handles token context internally via client headers
        supabase.auth.update_user({"password": new_password})
        return success_response("Password has been reset successfully.")
    except Exception as e:
        return error_response(f"Failed to reset password: {str(e)}")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock logout successful.")
        
    try:
        # Supabase logs out the active session
        supabase.auth.sign_out()
        return success_response("Logged out successfully.")
    except Exception as e:
        return error_response(f"Logout failed: {str(e)}")

@auth_bp.route("/profile", methods=["GET"])
@login_required
def get_current_profile():
    return success_response("Profile retrieved successfully.", {
        "user": g.user,
        "profile": g.profile
    })
