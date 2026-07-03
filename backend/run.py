from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Determine port
    try:
        port = int(os.getenv("PORT", 5000))
    except ValueError:
        port = 5000
        
    # Start development server
    app.run(host="0.0.0.0", port=port, debug=True)
