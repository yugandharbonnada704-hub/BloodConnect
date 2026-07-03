from supabase import create_client, Client
from app.config import Config

supabase_client = None

def init_supabase():
    global supabase_client
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_KEY
    
    if url and key and "dummy" not in url and "dummy" not in key:
        try:
            url_clean = url.strip().strip('"').strip("'")
            key_clean = key.strip().strip('"').strip("'")
            supabase_client = create_client(url_clean, key_clean)
            print("Supabase client successfully initialized.")
        except Exception as e:
            print(f"Failed to initialize Supabase client: {e}")
            supabase_client = None
    else:
        print("Supabase is unconfigured or configured with dummy values. Supabase client set to None.")
        supabase_client = None

def get_supabase():
    global supabase_client
    if supabase_client is None:
        init_supabase()
    return supabase_client
