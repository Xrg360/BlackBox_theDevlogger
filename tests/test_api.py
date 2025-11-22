# Blackbox Testing Suite

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import requests
from backend.models import EventType, RunStatus
import time

# Test configuration
API_URL = "http://localhost:8000"
TEST_TIMEOUT = 5  # seconds

def wait_for_api(max_attempts=10):
    """Wait for API to be available"""
    for i in range(max_attempts):
        try:
            response = requests.get(f"{API_URL}/health", timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            if i < max_attempts - 1:
                time.sleep(1)
    return False

@pytest.fixture(scope="session", autouse=True)
def check_api():
    """Ensure API is running before tests"""
    if not wait_for_api():
        pytest.exit("API server is not running. Start it with: python start_server.py")

class TestHealthCheck:
    def test_root_endpoint(self):
        """Test root endpoint returns health status"""
        response = requests.get(f"{API_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{API_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"

class TestUserEndpoints:
    def test_create_user(self):
        """Test user creation"""
        response = requests.post(
            f"{API_URL}/users",
            json={"username": f"test_user_{int(time.time())}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "username" in data
    
    def test_create_duplicate_user(self):
        """Test that duplicate usernames are rejected"""
        username = f"duplicate_user_{int(time.time())}"
        
        # Create first user
        response1 = requests.post(f"{API_URL}/users", json={"username": username})
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = requests.post(f"{API_URL}/users", json={"username": username})
        assert response2.status_code == 400
    
    def test_list_users(self):
        """Test listing users"""
        response = requests.get(f"{API_URL}/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
    
    def test_list_users_pagination(self):
        """Test user pagination"""
        response = requests.get(f"{API_URL}/users?skip=0&limit=5")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) <= 5

class TestProjectEndpoints:
    def test_create_project(self):
        """Test project creation"""
        response = requests.post(
            f"{API_URL}/projects",
            json={
                "name": f"Test Project {int(time.time())}",
                "description": "A test project"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "name" in data
    
    def test_list_projects(self):
        """Test listing projects"""
        response = requests.get(f"{API_URL}/projects")
        assert response.status_code == 200
        projects = response.json()
        assert isinstance(projects, list)

class TestEventEndpoints:
    def test_create_event(self):
        """Test event creation"""
        # First create a project
        project_response = requests.post(
            f"{API_URL}/projects",
            json={"name": f"Event Test Project {int(time.time())}"}
        )
        project_id = project_response.json()["id"]
        
        # Create event
        response = requests.post(
            f"{API_URL}/events",
            json={
                "project_id": project_id,
                "event_type": "info",
                "message": "Test event",
                "metadata_json": '{"test": true}'
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "timestamp" in data
    
    def test_list_events(self):
        """Test listing events"""
        response = requests.get(f"{API_URL}/events")
        assert response.status_code == 200
        events = response.json()
        assert isinstance(events, list)

class TestStatsEndpoint:
    def test_stats_summary(self):
        """Test stats summary endpoint"""
        response = requests.get(f"{API_URL}/stats/summary")
        assert response.status_code == 200
        data = response.json()
        
        # Check all expected fields are present
        assert "total_users" in data
        assert "total_projects" in data
        assert "total_sessions" in data
        assert "total_snippets" in data
        assert "total_runs" in data
        assert "total_events" in data
        assert "runs_by_status" in data
        assert "events_by_type" in data
        
        # Check values are non-negative integers
        assert data["total_users"] >= 0
        assert isinstance(data["runs_by_status"], dict)
        assert isinstance(data["events_by_type"], dict)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
