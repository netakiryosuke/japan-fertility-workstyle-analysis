from app.api.main import api_router


class TestApiMain:
    def test_api_router_is_configured(self):
        # Given / When / Then
        assert api_router is not None
        assert len(api_router.routes) > 0
