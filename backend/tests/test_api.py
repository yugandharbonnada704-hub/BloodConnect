import unittest
import json
import sys
import os

# Append the parent directory to the path so python can resolve app imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class BloodDonorSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_health_check(self):
        """Test the application health status endpoint."""
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')

    def test_auth_register(self):
        """Test API registration route validation and response format."""
        payload = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone_number": "+919988776655",
            "password": "securepassword123"
        }
        response = self.client.post('/api/auth/register', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertIn('email', data['data']['user'])

    def test_auth_login_donor(self):
        """Test API login route for donor role."""
        payload = {
            "email": "donor@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/auth/login', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['access_token'], 'mock-donor-token')

    def test_auth_login_admin(self):
        """Test API login route for admin role."""
        payload = {
            "email": "admin@example.com",
            "password": "password123"
        }
        response = self.client.post('/api/auth/login', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['access_token'], 'mock-admin-token')

    def test_unauthorized_access(self):
        """Test that access is rejected for protected routes when token is missing."""
        response = self.client.get('/api/donors/profile')
        self.assertEqual(response.status_code, 401)

    def test_donor_profile_get(self):
        """Test fetching donor profile with authorized header."""
        headers = {"Authorization": "Bearer mock-donor-token"}
        response = self.client.get('/api/donors/profile', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['full_name'], 'Mock Donor User')

    def test_donor_profile_update_validation(self):
        """Test input validation constraint errors on profile update."""
        headers = {"Authorization": "Bearer mock-donor-token"}
        payload = {
            "full_name": "New Name",
            "phone_number": "12345", # Invalid format (too short)
            "state": "Maharashtra",
            "district": "Mumbai",
            "city": "Mumbai"
        }
        response = self.client.put('/api/donors/profile', 
                                  headers=headers,
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')

    def test_donor_toggle_availability(self):
        """Test updating donor availability state."""
        headers = {"Authorization": "Bearer mock-donor-token"}
        payload = {"availability_status": "Not Available"}
        response = self.client.put('/api/donors/availability', 
                                  headers=headers,
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

    def test_search_donors(self):
        """Test donor location and blood group search filtering."""
        response = self.client.get('/api/search/donors?blood_group=O%2B&city=Mumbai')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['full_name'], 'Arjun Sharma')

    def test_location_hierarchical_lookup(self):
        """Test that states and districts can be fetched hierarchically."""
        res = self.client.get('/api/search/locations/states')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Maharashtra", data['data'])

        res = self.client.get('/api/search/locations/districts?state=Maharashtra')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Mumbai", data['data'])

    def test_create_blood_request(self):
        """Test submission of a new emergency blood request."""
        headers = {"Authorization": "Bearer mock-donor-token"}
        payload = {
            "patient_name": "Test Patient",
            "blood_group": "A+",
            "hospital_name": "City Hospital",
            "state": "Maharashtra",
            "district": "Mumbai",
            "city": "Mumbai",
            "contact_number": "+919876543210",
            "urgency_level": "High",
            "units_required": 2
        }
        response = self.client.post('/api/requests', 
                                   headers=headers,
                                   data=json.dumps(payload),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')

    def test_admin_dashboard_unauthorized(self):
        """Test that non-admins are blocked from requesting administrative data."""
        headers = {"Authorization": "Bearer mock-donor-token"}
        response = self.client.get('/api/admin/dashboard', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_admin_dashboard_authorized(self):
        """Test admin analytics dashboard retrieval."""
        headers = {"Authorization": "Bearer mock-admin-token"}
        response = self.client.get('/api/admin/dashboard', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['verified_donors'], 6)

    def test_admin_verify_donor(self):
        """Test admin approval operation for a donor account."""
        headers = {"Authorization": "Bearer mock-admin-token"}
        payload = {"verification_status": "verified"}
        response = self.client.put('/api/admin/donors/mock-uuid-here/verify', 
                                  headers=headers,
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
