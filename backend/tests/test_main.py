from fastapi.testclient import TestClient

from app.main import app


class TestAppMain:
    def test_health_check_endpoint(self):
        # Given
        client = TestClient(app)
        
        # When
        response = client.get("/health")
        
        # Then
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        
    def test_app_has_title(self):
        # Given / When / Then
        assert app.title == "Japan Fertility Workstyle Analysis API"
        
    def test_app_includes_api_router(self):
        # Given / When / Then
        assert len(app.routes) > 0
        # Verify analysis endpoint is registered
        paths = [route.path for route in app.routes]
        assert "/analysis" in paths
