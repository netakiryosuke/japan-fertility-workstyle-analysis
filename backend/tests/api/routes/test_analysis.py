import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from io import BytesIO

from app.main import app
from app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService
from app.domain.model.fixed_effects_result import FixedEffectsResult


class TestAnalysisRoute:
    def test_analyze_endpoint_returns_200_on_success(self):
        # Given
        client = TestClient(app)
        
        # Create sufficient panel data with variation
        csv_content = "prefecture,year,fertility_rate,work_hours\n"
        for year in [2018, 2019, 2020, 2021, 2022]:
            csv_content += f"Tokyo,{year},{1.2 + (year-2018)*0.05},{40 - (year-2018)}\n"
            csv_content += f"Osaka,{year},{1.5 + (year-2018)*0.05},{42 - (year-2018)*0.5}\n"
            csv_content += f"Kyoto,{year},{1.3 + (year-2018)*0.02},{41 - (year-2018)*0.5}\n"
        
        files = {"csv_file": ("test.csv", csv_content, "text/csv")}
        data = {
            "dependent_var": "fertility_rate",
            "independent_vars": ["work_hours"]
        }
        
        # When
        response = client.post("/analysis", files=files, data=data)
        
        # Then
        assert response.status_code == 200
        result = response.json()
        assert "nobs" in result
        assert "params" in result
        assert "rsquared_within" in result
        
    def test_analyze_endpoint_with_multiple_independent_vars(self):
        # Given
        client = TestClient(app)
        
        csv_content = "prefecture,year,fertility_rate,work_hours,income\n"
        csv_content += "Tokyo,2020,1.2,40,500\n"
        csv_content += "Tokyo,2021,1.3,38,520\n"
        csv_content += "Osaka,2020,1.5,42,480\n"
        csv_content += "Osaka,2021,1.6,40,500\n"
        
        files = {"csv_file": ("test.csv", csv_content, "text/csv")}
        data = {
            "dependent_var": "fertility_rate",
            "independent_vars": ["work_hours", "income"]
        }
        
        # When
        response = client.post("/analysis", files=files, data=data)
        
        # Then
        assert response.status_code == 200
        result = response.json()
        assert "work_hours" in result["params"]
        assert "income" in result["params"]
        
    def test_analyze_endpoint_returns_422_on_missing_columns(self):
        # Given
        client = TestClient(app)
        
        csv_content = "prefecture,year,fertility_rate\n"
        csv_content += "Tokyo,2020,1.2\n"
        csv_content += "Osaka,2020,1.5\n"
        
        files = {"csv_file": ("test.csv", csv_content, "text/csv")}
        data = {
            "dependent_var": "fertility_rate",
            "independent_vars": ["work_hours"]
        }
        
        # When
        response = client.post("/analysis", files=files, data=data)
        
        # Then
        assert response.status_code == 422
        result = response.json()
        assert "detail" in result
        
    def test_analyze_endpoint_returns_400_on_invalid_csv(self):
        # Given
        client = TestClient(app)
        
        invalid_csv = b"\x80\x81\x82"
        
        files = {"csv_file": ("test.csv", invalid_csv, "text/csv")}
        data = {
            "dependent_var": "fertility_rate",
            "independent_vars": ["work_hours"]
        }
        
        # When
        response = client.post("/analysis", files=files, data=data)
        
        # Then
        assert response.status_code == 400
