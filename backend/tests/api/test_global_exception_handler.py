import pytest
from fastapi import Request, status
from unittest.mock import Mock

from app.api.global_exception_handler import (
    handle_value_error,
    handle_missing_columns_exception,
    handle_unexpected_exception
)
from app.application.exception.missing_columns_exception import MissingColumnsException


class TestHandleValueError:
    def test_returns_400_response(self):
        # Given
        mock_request = Mock(spec=Request)
        mock_request.url.path = "/test/path"
        error = ValueError("Invalid input")
        
        # When
        response = handle_value_error(mock_request, error)
        
        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.body is not None
        
    def test_response_contains_error_details(self):
        # Given
        mock_request = Mock(spec=Request)
        mock_request.url.path = "/test/path"
        error = ValueError("Invalid input")
        
        # When
        response = handle_value_error(mock_request, error)
        content = response.body.decode('utf-8')
        
        # Then
        assert "Invalid input" in content
        assert "400" in content
        assert "/test/path" in content


class TestHandleMissingColumnsException:
    def test_returns_422_response(self):
        # Given
        mock_request = Mock(spec=Request)
        mock_request.url.path = "/test/path"
        error = MissingColumnsException(["column1", "column2"])
        
        # When
        response = handle_missing_columns_exception(mock_request, error)
        
        # Then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.body is not None
        
    def test_response_contains_missing_columns(self):
        # Given
        mock_request = Mock(spec=Request)
        mock_request.url.path = "/test/path"
        error = MissingColumnsException(["column1", "column2"])
        
        # When
        response = handle_missing_columns_exception(mock_request, error)
        content = response.body.decode('utf-8')
        
        # Then
        assert "column1" in content
        assert "column2" in content
        assert "422" in content


class TestHandleUnexpectedException:
    def test_returns_500_response(self):
        # Given
        mock_request = Mock(spec=Request)
        mock_request.url.path = "/test/path"
        error = Exception("Unexpected error")
        
        # When
        response = handle_unexpected_exception(mock_request, error)
        
        # Then
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.body is not None
        
    def test_response_does_not_expose_internal_error_details(self):
        # Given
        mock_request = Mock(spec=Request)
        mock_request.url.path = "/test/path"
        error = Exception("Secret internal error")
        
        # When
        response = handle_unexpected_exception(mock_request, error)
        content = response.body.decode('utf-8')
        
        # Then
        assert "Secret internal error" not in content
        assert "Unexpected error" in content
        assert "500" in content
