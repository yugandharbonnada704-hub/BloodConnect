from app.services.supabase_service import get_supabase

class LocationService:
    @staticmethod
    def get_states():
        supabase = get_supabase()
        if not supabase:
            # Return static fallback list for local debugging
            return ["Maharashtra", "Karnataka", "Delhi", "Telangana", "Tamil Nadu", "West Bengal"]
        try:
            response = supabase.table("locations").select("state").execute()
            states = sorted(list(set(row["state"] for row in response.data)))
            return states
        except Exception as e:
            print(f"Error fetching states: {e}")
            return ["Maharashtra", "Karnataka", "Delhi", "Telangana", "Tamil Nadu", "West Bengal"]

    @staticmethod
    def get_districts(state):
        supabase = get_supabase()
        if not supabase:
            if state == "Maharashtra":
                return ["Mumbai", "Pune"]
            elif state == "Karnataka":
                return ["Bangalore Urban"]
            elif state == "Delhi":
                return ["New Delhi"]
            return []
        try:
            response = supabase.table("locations").select("district").eq("state", state).execute()
            districts = sorted(list(set(row["district"] for row in response.data)))
            return districts
        except Exception as e:
            print(f"Error fetching districts for {state}: {e}")
            return []

    @staticmethod
    def get_cities(state, district):
        supabase = get_supabase()
        if not supabase:
            if district == "Mumbai":
                return ["Mumbai"]
            elif district == "Pune":
                return ["Pune"]
            elif district == "Bangalore Urban":
                return ["Bangalore"]
            elif district == "New Delhi":
                return ["Delhi"]
            return []
        try:
            response = supabase.table("locations").select("city").eq("state", state).eq("district", district).execute()
            cities = sorted(list(set(row["city"] for row in response.data)))
            return cities
        except Exception as e:
            print(f"Error fetching cities for {state}/{district}: {e}")
            return []

    @staticmethod
    def get_villages(state, district, city):
        supabase = get_supabase()
        if not supabase:
            if city == "Mumbai":
                return ["Worli", "Bandra", "Andheri"]
            elif city == "Pune":
                return ["Shivaji Nagar", "Kothrud"]
            elif city == "Bangalore":
                return ["Koramangala", "Indiranagar", "Whitefield"]
            elif city == "Delhi":
                return ["Connaught Place", "Karol Bagh"]
            return []
        try:
            response = supabase.table("locations").select("village").eq("state", state).eq("district", district).eq("city", city).execute()
            villages = sorted(list(set(row["village"] for row in response.data if row.get("village"))))
            return villages
        except Exception as e:
            print(f"Error fetching villages for {state}/{district}/{city}: {e}")
            return []
