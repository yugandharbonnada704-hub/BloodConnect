from flask import Blueprint, request
from app.services.supabase_service import get_supabase
from app.services.location_service import LocationService
from app.utils.helpers import success_response, error_response

search_bp = Blueprint("search", __name__)

@search_bp.route("/donors", methods=["GET"])
def search_donors():
    blood_group = request.args.get("blood_group")
    state = request.args.get("state")
    district = request.args.get("district")
    city = request.args.get("city")
    village = request.args.get("village")
    availability = request.args.get("availability_status")

    supabase = get_supabase()
    if not supabase:
        # Mock Search Results with fallback
        mock_donors = [
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "full_name": "Arjun Sharma",
                "blood_group": "O+",
                "state": "Maharashtra",
                "district": "Mumbai",
                "city": "Mumbai",
                "village": "Worli",
                "availability_status": "Available",
                "phone_number": "+919876543210",
                "email": "arjun@example.com",
                "last_donation_date": "2026-05-10"
            },
            {
                "id": "00000000-0000-0000-0000-000000000004",
                "full_name": "Priya Nair",
                "blood_group": "A+",
                "state": "Karnataka",
                "district": "Bangalore Urban",
                "city": "Bangalore",
                "village": "Koramangala",
                "availability_status": "Available",
                "phone_number": "+919123456789",
                "email": "priya@example.com",
                "last_donation_date": "2026-04-20"
            },
            {
                "id": "00000000-0000-0000-0000-000000000005",
                "full_name": "Rohan Verma",
                "blood_group": "B-",
                "state": "Delhi",
                "district": "New Delhi",
                "city": "Delhi",
                "village": "Connaught Place",
                "availability_status": "Not Available",
                "phone_number": "+919988776655",
                "email": "rohan@example.com",
                "last_donation_date": "2026-01-05"
            }
        ]
        
        # Apply filters to mock data
        results = mock_donors
        if blood_group:
            results = [d for d in results if d["blood_group"] == blood_group]
        if state:
            results = [d for d in results if d["state"].lower() == state.lower()]
        if district:
            results = [d for d in results if d["district"].lower() == district.lower()]
        if city:
            results = [d for d in results if d["city"].lower() == city.lower()]
        if village:
            results = [d for d in results if d["village"].lower() == village.lower()]
        if availability:
            results = [d for d in results if d["availability_status"].lower() == availability.lower()]
            
        # Sort by availability status: "Available" first (alphabetically, A before N)
        results.sort(key=lambda x: x["availability_status"])
        return success_response("Mock search complete.", results)

    try:
        # Build query for verified profiles only
        query = supabase.table("profiles").select(
            "id, full_name, age, gender, blood_group, phone_number, email, state, district, city, village, address, availability_status, last_donation_date"
        ).eq("verification_status", "verified")
        
        # Apply optional parameters
        if blood_group:
            query = query.eq("blood_group", blood_group)
        if state:
            query = query.eq("state", state)
        if district:
            query = query.eq("district", district)
        if city:
            query = query.eq("city", city)
        if village:
            query = query.eq("village", village)
        if availability:
            query = query.eq("availability_status", availability)
            
        # Order by availability_status (ascending makes 'Available' come before 'Not Available')
        query = query.order("availability_status", desc=False)
        
        response = query.execute()
        return success_response("Search complete.", response.data)
        
    except Exception as e:
        return error_response(f"Search query failed: {str(e)}")

@search_bp.route("/locations/states", methods=["GET"])
def get_states():
    states = LocationService.get_states()
    return success_response("States retrieved successfully.", states)

@search_bp.route("/locations/districts", methods=["GET"])
def get_districts():
    state = request.args.get("state")
    if not state:
        return error_response("Parameter 'state' is required.")
    districts = LocationService.get_districts(state)
    return success_response("Districts retrieved successfully.", districts)

@search_bp.route("/locations/cities", methods=["GET"])
def get_cities():
    state = request.args.get("state")
    district = request.args.get("district")
    if not state or not district:
        return error_response("Parameters 'state' and 'district' are required.")
    cities = LocationService.get_cities(state, district)
    return success_response("Cities retrieved successfully.", cities)

@search_bp.route("/locations/villages", methods=["GET"])
def get_villages():
    state = request.args.get("state")
    district = request.args.get("district")
    city = request.args.get("city")
    if not state or not district or not city:
        return error_response("Parameters 'state', 'district', and 'city' are required.")
    villages = LocationService.get_villages(state, district, city)
    return success_response("Villages retrieved successfully.", villages)
