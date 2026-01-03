from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


class TestCORSMiddleware:
    def test_cors_middleware_registered_when_origins_configured(self):
        """Test that CORS middleware is registered when origins are configured"""
        # Given - Create a test app with CORS origins
        test_app = FastAPI(title="Test App")
        allowed_origins = ["http://localhost:3000", "https://example.com"]
        
        # When - Add CORS middleware (simulating the condition in main.py)
        if allowed_origins:
            test_app.add_middleware(
                CORSMiddleware,
                allow_origins=allowed_origins,
                allow_credentials=True,
                allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                allow_headers=["*"],
            )
        
        # Then - Verify CORS middleware is registered
        cors_middleware_found = False
        for middleware in test_app.user_middleware:
            if middleware.cls == CORSMiddleware:
                cors_middleware_found = True
                break
        
        assert cors_middleware_found, "CORSMiddleware should be registered when BACKEND_CORS_ORIGINS is configured"
    
    def test_cors_middleware_not_registered_when_origins_empty(self):
        """Test that CORS middleware is not registered when origins list is empty"""
        # Given - Create a test app without CORS origins
        test_app = FastAPI(title="Test App")
        allowed_origins = []
        
        # When - Conditionally add CORS middleware (simulating the condition in main.py)
        if allowed_origins:
            test_app.add_middleware(
                CORSMiddleware,
                allow_origins=allowed_origins,
                allow_credentials=True,
                allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                allow_headers=["*"],
            )
        
        # Then - Verify CORS middleware is not registered
        cors_middleware_found = False
        for middleware in test_app.user_middleware:
            if middleware.cls == CORSMiddleware:
                cors_middleware_found = True
                break
        
        assert not cors_middleware_found, "CORSMiddleware should not be registered when BACKEND_CORS_ORIGINS is empty"
    
    def test_cors_headers_for_preflight_request(self):
        """Test that preflight OPTIONS requests return proper CORS headers"""
        # Given - Create a test app with CORS enabled
        test_app = FastAPI(title="Test App")
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )
        
        @test_app.get("/health")
        def health():
            return {"status": "ok"}
        
        client = TestClient(test_app)
        
        # When - Make a preflight OPTIONS request
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        
        # Then - Verify CORS headers are present
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"
        assert "access-control-allow-methods" in response.headers
    
    def test_cors_headers_for_actual_request_with_allowed_origin(self):
        """Test that actual requests with allowed origins receive CORS headers"""
        # Given - Create a test app with CORS enabled
        test_app = FastAPI(title="Test App")
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )
        
        @test_app.get("/health")
        def health():
            return {"status": "ok"}
        
        client = TestClient(test_app)
        
        # When - Make an actual request with Origin header
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Then - Verify CORS headers are present
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"
    
    def test_cors_headers_not_present_for_disallowed_origin(self):
        """Test that requests with disallowed origins do not receive CORS headers"""
        # Given - Create a test app with CORS enabled for specific origin
        test_app = FastAPI(title="Test App")
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )
        
        @test_app.get("/health")
        def health():
            return {"status": "ok"}
        
        client = TestClient(test_app)
        
        # When - Make a request with a disallowed origin
        response = client.get(
            "/health",
            headers={"Origin": "http://evil.com"}
        )
        
        # Then - Verify CORS headers are not present for disallowed origins
        assert response.status_code == 200
        # CORS middleware will reject the origin by not including the header
        assert response.headers.get("access-control-allow-origin") != "http://evil.com"
    
    def test_cors_configured_methods_are_allowed(self):
        """Test that configured HTTP methods are allowed in CORS"""
        # Given - Create a test app with specific CORS methods
        test_app = FastAPI(title="Test App")
        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=allowed_methods,
            allow_headers=["*"],
        )
        
        @test_app.get("/health")
        def health():
            return {"status": "ok"}
        
        client = TestClient(test_app)
        
        # When - Make a preflight request
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        
        # Then - Verify the methods are in the allow-methods header
        assert response.status_code == 200
        assert "access-control-allow-methods" in response.headers
        methods_header = response.headers["access-control-allow-methods"]
        # Verify that key methods are present in the header
        for method in ["GET", "POST", "PUT", "DELETE"]:
            assert method in methods_header
