from flask import Blueprint, request, g
from app.services.supabase_service import get_supabase
from app.services.email_service import EmailService
from app.utils.helpers import success_response, error_response
from app.middleware import admin_required
from datetime import datetime

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def admin_dashboard():
    supabase = get_supabase()
    if not supabase:
        # Return fallback mock numbers for admin analytics
        return success_response("Mock admin dashboard stats retrieved.", {
            "total_users": 10,
            "total_donors": 8,
            "verified_donors": 6,
            "available_donors": 4,
            "pending_verifications": 2,
            "total_requests": 6,
            "pending_requests": 3,
            "fulfilled_requests": 2
        })

    try:
        # Load user profiles
        p_res = supabase.table("profiles").select("role, verification_status, availability_status").execute()
        profiles = p_res.data
        
        total_users = len(profiles)
        total_donors = sum(1 for p in profiles if p.get("role") == "donor")
        verified_donors = sum(1 for p in profiles if p.get("role") == "donor" and p.get("verification_status") == "verified")
        available_donors = sum(1 for p in profiles if p.get("role") == "donor" and p.get("verification_status") == "verified" and p.get("availability_status") == "Available")
        pending_verifications = sum(1 for p in profiles if p.get("role") == "donor" and p.get("verification_status") == "pending")
        
        # Load requests
        r_res = supabase.table("blood_requests").select("status").execute()
        requests = r_res.data
        
        total_requests = len(requests)
        pending_requests = sum(1 for r in requests if r.get("status") == "Pending")
        fulfilled_requests = sum(1 for r in requests if r.get("status") == "Fulfilled")
        
        return success_response("Admin dashboard stats retrieved.", {
            "total_users": total_users,
            "total_donors": total_donors,
            "verified_donors": verified_donors,
            "available_donors": available_donors,
            "pending_verifications": pending_verifications,
            "total_requests": total_requests,
            "pending_requests": pending_requests,
            "fulfilled_requests": fulfilled_requests
        })
    except Exception as e:
        return error_response(f"Failed to fetch admin stats: {str(e)}")

@admin_bp.route("/donors", methods=["GET"])
@admin_required
def list_donors():
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock donor list retrieved.", [
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "full_name": "Arjun Sharma",
                "email": "arjun@example.com",
                "phone_number": "+919876543210",
                "role": "donor",
                "verification_status": "verified"
            },
            {
                "id": "00000000-0000-0000-0000-000000000003",
                "full_name": "Mock Unverified User",
                "email": "unverified@example.com",
                "phone_number": "+919988776655",
                "role": "donor",
                "verification_status": "pending"
            }
        ])
        
    try:
        response = supabase.table("profiles").select("*").eq("role", "donor").order("created_at", desc=True).execute()
        return success_response("Donors list retrieved.", response.data)
    except Exception as e:
        return error_response(f"Failed to fetch donors: {str(e)}")

@admin_bp.route("/donors/<id>/verify", methods=["PUT"])
@admin_required
def verify_donor(id):
    data = request.get_json() or {}
    status = data.get("verification_status")
    
    if status not in ["verified", "rejected", "pending"]:
        return error_response("Invalid status. Must be 'verified', 'rejected', or 'pending'.")
        
    supabase = get_supabase()
    if not supabase:
        EmailService.send_donor_approval_email("unverified@example.com", "Mock Unverified User", status)
        return success_response(f"Mock donor verification status updated to {status}.", {
            "id": id,
            "verification_status": status
        })
        
    try:
        # Retrieve target profile email/name for custom email notifications
        profile_res = supabase.table("profiles").select("*").eq("id", id).execute()
        if not profile_res.data:
            return error_response("Donor profile not found.", code=404)
            
        profile = profile_res.data[0]
        
        # Update
        update_res = supabase.table("profiles").update({
            "verification_status": status,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", id).execute()
        
        if not update_res.data:
            return error_response("Failed to update donor profile status.")
            
        # Notify donor of verification status change
        EmailService.send_donor_approval_email(profile.get("email"), profile.get("full_name"), status)
        
        return success_response(f"Donor verification status updated to {status} successfully.", update_res.data[0])
    except Exception as e:
        return error_response(f"Failed to update verification status: {str(e)}")

@admin_bp.route("/requests", methods=["GET"])
@admin_required
def list_all_requests():
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock admin request list retrieved.", [
            {
                "id": "mock-req-1",
                "patient_name": "Ramesh Gupta",
                "blood_group": "O-",
                "status": "Pending",
                "units_required": 3
            }
        ])
        
    try:
        response = supabase.table("blood_requests").select("*").order("created_at", desc=True).execute()
        return success_response("All requests retrieved.", response.data)
    except Exception as e:
        return error_response(f"Failed to retrieve requests: {str(e)}")

@admin_bp.route("/requests/<id>/status", methods=["PUT"])
@admin_required
def update_request_status(id):
    data = request.get_json() or {}
    status = data.get("status")
    notes = data.get("notes", "Status updated by Admin.")
    
    if status not in ["Pending", "Approved", "Fulfilled", "Cancelled"]:
        return error_response("Invalid status. Must be 'Pending', 'Approved', 'Fulfilled', or 'Cancelled'.")
        
    supabase = get_supabase()
    if not supabase:
        EmailService.send_request_status_change_email("donor@example.com", "Mock Donor User", "Patient", status)
        return success_response(f"Mock request status updated to {status}.", {
            "id": id,
            "status": status
        })
        
    try:
        # Retrieve request metadata
        req_res = supabase.table("blood_requests").select("*").eq("id", id).execute()
        if not req_res.data:
            return error_response("Blood request not found.", code=404)
            
        blood_request = req_res.data[0]
        
        # Load creator profile
        creator_res = supabase.table("profiles").select("*").eq("id", blood_request["user_id"]).execute()
        creator_email = "requester@example.com"
        creator_name = "Requester"
        if creator_res.data:
            creator_email = creator_res.data[0].get("email")
            creator_name = creator_res.data[0].get("full_name")
            
        # Update request status
        update_res = supabase.table("blood_requests").update({
            "status": status,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", id).execute()
        
        # Log to history
        history_payload = {
            "request_id": id,
            "status": status,
            "updated_by": g.user["id"],
            "notes": notes
        }
        supabase.table("blood_request_status_history").insert(history_payload).execute()
        
        # Notify request owner of update
        EmailService.send_request_status_change_email(creator_email, creator_name, blood_request.get("patient_name"), status)
        
        return success_response(f"Request status updated to {status} successfully.", update_res.data[0])
    except Exception as e:
        return error_response(f"Failed to update request status: {str(e)}")
