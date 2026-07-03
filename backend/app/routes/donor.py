from flask import Blueprint, request, g
from app.services.supabase_service import get_supabase
from app.utils.helpers import success_response, error_response
from app.utils.validators import validate_donor_profile_data
from app.middleware import login_required
from datetime import datetime

donor_bp = Blueprint("donor", __name__)

@donor_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    if not g.profile:
        return error_response("Profile not found.", code=404)
    return success_response("Donor profile retrieved.", g.profile)

@donor_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    data = request.get_json() or {}
    
    # Validate input data
    errors = validate_donor_profile_data(data)
    if errors:
        return error_response(errors[0])
        
    supabase = get_supabase()
    
    update_data = {
        "full_name": data.get("full_name"),
        "age": data.get("age"),
        "gender": data.get("gender"),
        "blood_group": data.get("blood_group"),
        "phone_number": data.get("phone_number"),
        "state": data.get("state"),
        "district": data.get("district"),
        "city": data.get("city"),
        "village": data.get("village"),
        "address": data.get("address"),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    if "last_donation_date" in data:
        update_data["last_donation_date"] = data.get("last_donation_date")

    if not supabase:
        # Mock update behavior
        mock_profile = {**g.profile, **update_data}
        return success_response("Mock profile updated successfully.", mock_profile)

    try:
        response = supabase.table("profiles").update(update_data).eq("id", g.user["id"]).execute()
        if not response.data:
            return error_response("Failed to update profile.")
        return success_response("Profile updated successfully.", response.data[0])
    except Exception as e:
        return error_response(f"Error updating profile: {str(e)}")

@donor_bp.route("/profile", methods=["DELETE"])
@login_required
def delete_profile():
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock profile deleted successfully.")
        
    try:
        response = supabase.table("profiles").delete().eq("id", g.user["id"]).execute()
        # Deleting profile from public.profiles table (auth user remains but has no profile)
        return success_response("Profile deleted successfully.")
    except Exception as e:
        return error_response(f"Error deleting profile: {str(e)}")

@donor_bp.route("/availability", methods=["PUT"])
@login_required
def toggle_availability():
    data = request.get_json() or {}
    status = data.get("availability_status")
    
    if status not in ["Available", "Not Available"]:
        return error_response("Invalid status. Must be 'Available' or 'Not Available'.")
        
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock availability status updated.", {"availability_status": status})
        
    try:
        response = supabase.table("profiles").update({"availability_status": status}).eq("id", g.user["id"]).execute()
        if not response.data:
            return error_response("Failed to update availability status.")
        return success_response("Availability status updated successfully.", response.data[0])
    except Exception as e:
        return error_response(f"Error updating availability: {str(e)}")

@donor_bp.route("/donations", methods=["POST"])
@login_required
def add_donation():
    data = request.get_json() or {}
    donation_date = data.get("donation_date")
    hospital_name = data.get("hospital_name")
    units = data.get("units_donated", 1)
    donation_type = data.get("donation_type", "Voluntary")
    notes = data.get("notes")
    
    if not donation_date or not hospital_name:
        return error_response("Donation date and hospital name are required.")
        
    if donation_type not in ["Voluntary", "Emergency", "Camp"]:
        return error_response("Invalid donation type. Must be 'Voluntary', 'Emergency', or 'Camp'.")
        
    try:
        units = int(units)
        if units <= 0:
            raise ValueError()
    except ValueError:
        return error_response("Units donated must be a positive integer.")

    supabase = get_supabase()
    
    donation_data = {
        "user_id": g.user["id"],
        "donation_date": donation_date,
        "hospital_name": hospital_name,
        "units_donated": units,
        "donation_type": donation_type,
        "notes": notes
    }
    
    if not supabase:
        mock_record = {**donation_data, "id": "00000000-0000-0000-0000-000000000999"}
        return success_response("Mock donation record added.", mock_record, code=201)

    try:
        # Insert donation record
        response = supabase.table("donation_history").insert(donation_data).execute()
        if not response.data:
            return error_response("Failed to save donation record.")
            
        # Update profile last donation date
        supabase.table("profiles").update({"last_donation_date": donation_date}).eq("id", g.user["id"]).execute()
        
        return success_response("Donation record added successfully.", response.data[0], code=201)
    except Exception as e:
        return error_response(f"Error adding donation history: {str(e)}")

@donor_bp.route("/donations", methods=["GET"])
@login_required
def get_donations():
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock donation history retrieved.", [
            {"date": "2026-05-15", "hospital_name": "Apollo Hospital", "units_donated": 1, "donation_type": "Voluntary"}
        ])
        
    try:
        response = supabase.table("donation_history").select("*").eq("user_id", g.user["id"]).order("donation_date", desc=True).execute()
        return success_response("Donation history retrieved successfully.", response.data)
    except Exception as e:
        return error_response(f"Error fetching donation history: {str(e)}")

@donor_bp.route("/dashboard", methods=["GET"])
@login_required
def donor_dashboard():
    profile = g.profile
    if not profile:
        return error_response("Profile not found.", code=404)
        
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock donor dashboard stats retrieved.", {
            "profile_status": profile.get("verification_status"),
            "availability_status": profile.get("availability_status"),
            "donation_count": 1,
            "donation_history": [
                {"donation_date": "2026-05-15", "hospital_name": "Apollo Hospital", "units_donated": 1, "donation_type": "Voluntary"}
            ]
        })
        
    try:
        # Total donation count
        count_response = supabase.table("donation_history").select("id", count="exact").eq("user_id", g.user["id"]).execute()
        donation_count = count_response.count if count_response.count is not None else len(count_response.data)
        
        # Recent history
        history_response = supabase.table("donation_history").select("*").eq("user_id", g.user["id"]).order("donation_date", desc=True).limit(5).execute()
        
        return success_response("Donor dashboard stats retrieved.", {
            "profile_status": profile.get("verification_status"),
            "availability_status": profile.get("availability_status"),
            "donation_count": donation_count,
            "donation_history": history_response.data
        })
    except Exception as e:
        return error_response(f"Error loading donor dashboard: {str(e)}")
