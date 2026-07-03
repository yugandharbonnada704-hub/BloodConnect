from flask import Blueprint, request, g
from app.services.supabase_service import get_supabase
from app.utils.helpers import success_response, error_response
from app.middleware import login_required
from datetime import datetime

request_bp = Blueprint("request", __name__)

@request_bp.route("", methods=["POST"])
@login_required
def create_request():
    data = request.get_json() or {}
    patient_name = data.get("patient_name")
    blood_group = data.get("blood_group")
    hospital_name = data.get("hospital_name")
    state = data.get("state")
    district = data.get("district")
    city = data.get("city")
    village = data.get("village")
    contact = data.get("contact_number")
    units = data.get("units_required", 1)
    urgency = data.get("urgency_level")
    
    if not all([patient_name, blood_group, hospital_name, state, district, city, contact, urgency]):
        return error_response("Missing required blood request fields (patient_name, blood_group, hospital_name, state, district, city, contact_number, urgency_level).")
        
    if blood_group not in ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']:
        return error_response(f"Invalid blood group: '{blood_group}'.")
        
    if urgency not in ['Critical', 'High', 'Medium', 'Low']:
        return error_response("Invalid urgency level. Must be Critical, High, Medium, or Low.")
        
    try:
        units = int(units)
        if units <= 0:
            raise ValueError()
    except ValueError:
        return error_response("Units required must be a positive integer.")

    request_payload = {
        "user_id": g.user["id"],
        "patient_name": patient_name,
        "blood_group": blood_group,
        "hospital_name": hospital_name,
        "state": state,
        "district": district,
        "city": city,
        "village": village,
        "contact_number": contact,
        "units_required": units,
        "urgency_level": urgency,
        "status": "Pending"
    }

    supabase = get_supabase()
    if not supabase:
        # Mock request response
        mock_req = {**request_payload, "id": "00000000-0000-0000-0000-000000000888", "created_at": datetime.utcnow().isoformat()}
        return success_response("Mock blood request created successfully.", mock_req, code=201)

    try:
        # Insert request
        response = supabase.table("blood_requests").insert(request_payload).execute()
        if not response.data:
            return error_response("Failed to create blood request.")
            
        req_id = response.data[0]["id"]
        
        # Log to status history
        history_payload = {
            "request_id": req_id,
            "status": "Pending",
            "updated_by": g.user["id"],
            "notes": "Request submitted."
        }
        supabase.table("blood_request_status_history").insert(history_payload).execute()
        
        return success_response("Blood request created successfully.", response.data[0], code=201)
    except Exception as e:
        return error_response(f"Error creating request: {str(e)}")

@request_bp.route("", methods=["GET"])
def list_requests():
    bg = request.args.get("blood_group")
    state = request.args.get("state")
    city = request.args.get("city")
    status = request.args.get("status")

    supabase = get_supabase()
    if not supabase:
        # Mock list
        mock_list = [
            {
                "id": "mock-req-1",
                "patient_name": "Ramesh Gupta",
                "blood_group": "O-",
                "hospital_name": "Apollo Hospital",
                "state": "Maharashtra",
                "district": "Mumbai",
                "city": "Mumbai",
                "village": "Worli",
                "contact_number": "+919876543210",
                "units_required": 3,
                "urgency_level": "Critical",
                "status": "Pending",
                "user_id": "00000000-0000-0000-0000-000000000001",
                "created_at": datetime.utcnow().isoformat()
            }
        ]
        return success_response("Mock blood requests retrieved.", mock_list)

    try:
        query = supabase.table("blood_requests").select("*")
        if bg:
            query = query.eq("blood_group", bg)
        if state:
            query = query.eq("state", state)
        if city:
            query = query.eq("city", city)
        if status:
            query = query.eq("status", status)
            
        response = query.order("created_at", desc=True).execute()
        return success_response("Blood requests retrieved successfully.", response.data)
    except Exception as e:
        return error_response(f"Error listing blood requests: {str(e)}")

@request_bp.route("/<id>", methods=["GET"])
def get_request_details(id):
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock request details retrieved.", {
            "request": {
                "id": id,
                "patient_name": "Ramesh Gupta",
                "blood_group": "O-",
                "status": "Pending",
                "hospital_name": "Apollo Hospital",
                "state": "Maharashtra",
                "city": "Mumbai",
                "contact_number": "+919876543210",
                "units_required": 3,
                "urgency_level": "Critical"
            },
            "history": [
                {"status": "Pending", "notes": "Request submitted.", "changed_at": datetime.utcnow().isoformat()}
            ]
        })

    try:
        req_response = supabase.table("blood_requests").select("*").eq("id", id).execute()
        if not req_response.data:
            return error_response("Blood request not found.", code=404)
            
        history_response = supabase.table("blood_request_status_history").select("*").eq("request_id", id).order("changed_at", desc=True).execute()
        
        return success_response("Blood request details retrieved.", {
            "request": req_response.data[0],
            "history": history_response.data
        })
    except Exception as e:
        return error_response(f"Error retrieving request details: {str(e)}")

@request_bp.route("/<id>", methods=["PUT"])
@login_required
def update_request(id):
    data = request.get_json() or {}
    
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock request updated successfully.")
        
    try:
        # Check current request ownership
        curr_response = supabase.table("blood_requests").select("*").eq("id", id).execute()
        if not curr_response.data:
            return error_response("Blood request not found.", code=404)
            
        req_obj = curr_response.data[0]
        
        # Admin or owner access only
        is_admin = g.profile and g.profile.get("role") == "admin"
        if req_obj["user_id"] != g.user["id"] and not is_admin:
            return error_response("Forbidden. You do not have permission to edit this request.", code=403)
            
        update_fields = {}
        for f in ["patient_name", "hospital_name", "contact_number", "units_required", "urgency_level", "state", "district", "city", "village"]:
            if f in data:
                update_fields[f] = data[f]
                
        if not update_fields:
            return error_response("No valid fields provided for update.")
            
        update_fields["updated_at"] = datetime.utcnow().isoformat()
        
        response = supabase.table("blood_requests").update(update_fields).eq("id", id).execute()
        return success_response("Blood request updated successfully.", response.data[0])
    except Exception as e:
        return error_response(f"Error updating request: {str(e)}")

@request_bp.route("/<id>/cancel", methods=["PUT"])
@login_required
def cancel_request(id):
    supabase = get_supabase()
    if not supabase:
        return success_response("Mock request cancelled successfully.")
        
    try:
        curr_response = supabase.table("blood_requests").select("*").eq("id", id).execute()
        if not curr_response.data:
            return error_response("Blood request not found.", code=404)
            
        req_obj = curr_response.data[0]
        
        # Admin or owner
        is_admin = g.profile and g.profile.get("role") == "admin"
        if req_obj["user_id"] != g.user["id"] and not is_admin:
            return error_response("Forbidden. You do not have permission to cancel this request.", code=403)
            
        if req_obj["status"] in ["Fulfilled", "Cancelled"]:
            return error_response(f"Cannot cancel a request that is already {req_obj['status']}.")
            
        response = supabase.table("blood_requests").update({
            "status": "Cancelled",
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", id).execute()
        
        # Log to history
        history_payload = {
            "request_id": id,
            "status": "Cancelled",
            "updated_by": g.user["id"],
            "notes": "Request cancelled by user/admin."
        }
        supabase.table("blood_request_status_history").insert(history_payload).execute()
        
        return success_response("Blood request cancelled successfully.", response.data[0])
    except Exception as e:
        return error_response(f"Error cancelling request: {str(e)}")
