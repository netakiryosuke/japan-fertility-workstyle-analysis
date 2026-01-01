from unittest.mock import Mock

from app.application.dependencies import get_fertility_analysis_application_service
from app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService


class TestGetFertilityAnalysisApplicationService:
    def test_returns_fertility_analysis_application_service_instance(self):
        # Given
        mock_csv_loader = Mock()
        
        # When
        result = get_fertility_analysis_application_service(csv_loader=mock_csv_loader)
        
        # Then
        assert isinstance(result, FertilityAnalysisApplicationService)
        assert result.csv_loader == mock_csv_loader
