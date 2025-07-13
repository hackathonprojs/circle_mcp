import pytest
import os
from unittest.mock import patch, Mock
import requests
from server import get_public_key


class TestGetPublicKey:
    """Test suite for get_public_key function."""

    @pytest.mark.asyncio
    async def test_get_public_key_success(self):
        """Test successful public key retrieval."""
        # Mock environment variables
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': 'test-api-key'
        }):
            # Mock the requests.get call
            mock_response = Mock()
            mock_response.text = '{"public_key": "0x1234567890abcdef"}'
            
            with patch('requests.get', return_value=mock_response) as mock_get:
                result = await get_public_key()
                
                assert result == '{"public_key": "0x1234567890abcdef"}'
                mock_get.assert_called_once_with(
                    "https://api.circle.com/v1/w3s/config/entity/publicKey",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer test-api-key"
                    }
                )

    @pytest.mark.asyncio
    async def test_get_public_key_missing_api_key(self):
        """Test error when CIRCLE_API_KEY is missing."""
        with patch.dict(os.environ, {}, clear=True):
            result = await get_public_key()
            
            assert result == "Error: CIRCLE_API_KEY environment variable must be set"

    @pytest.mark.asyncio
    async def test_get_public_key_empty_api_key(self):
        """Test error when CIRCLE_API_KEY is empty string."""
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': ''
        }):
            result = await get_public_key()
            
            assert result == "Error: CIRCLE_API_KEY environment variable must be set"

    @pytest.mark.asyncio
    async def test_get_public_key_whitespace_api_key(self):
        """Test that whitespace-only API key is treated as missing."""
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': '   '
        }):
            result = await get_public_key()
            
            assert result == "Error: CIRCLE_API_KEY environment variable must be set"

    @pytest.mark.asyncio
    async def test_get_public_key_request_exception(self):
        """Test handling of requests exceptions."""
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': 'test-api-key'
        }):
            # Mock requests.get to raise an exception
            with patch('requests.get', side_effect=requests.RequestException("Connection error")):
                result = await get_public_key()
                
                assert result == "Exception when calling Circle API: Connection error"

    @pytest.mark.asyncio
    async def test_get_public_key_timeout_exception(self):
        """Test handling of timeout exceptions."""
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': 'test-api-key'
        }):
            # Mock requests.get to raise a timeout
            with patch('requests.get', side_effect=requests.Timeout("Request timeout")):
                result = await get_public_key()
                
                assert result == "Exception when calling Circle API: Request timeout"

    @pytest.mark.asyncio
    async def test_get_public_key_http_error(self):
        """Test handling of HTTP errors."""
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': 'test-api-key'
        }):
            # Mock requests.get to raise an HTTP error
            with patch('requests.get', side_effect=requests.HTTPError("404 Not Found")):
                result = await get_public_key()
                
                assert result == "Exception when calling Circle API: 404 Not Found"

    @pytest.mark.asyncio
    async def test_get_public_key_response_text(self):
        """Test that the response.text is returned correctly."""
        with patch.dict(os.environ, {
            'CIRCLE_API_KEY': 'test-api-key'
        }):
            # Mock the requests.get call with different response text
            mock_response = Mock()
            mock_response.text = '{"data": {"publicKey": "0xabcdef1234567890"}}'
            
            with patch('requests.get', return_value=mock_response):
                result = await get_public_key()
                
                assert result == '{"data": {"publicKey": "0xabcdef1234567890"}}'


# Integration test (requires actual environment variables)
class TestGetPublicKeyIntegration:
    """Integration tests for get_public_key function."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_public_key_integration(self):
        """Integration test with real Circle API (requires valid credentials)."""
        # This test will only run if the API key is set
        api_key = os.getenv('CIRCLE_API_KEY')
        
        if not api_key:
            pytest.skip("Integration test requires CIRCLE_API_KEY environment variable")
        
        result = await get_public_key()
        
        # The result should not be an error message
        assert not result.startswith("Error:")
        assert not result.startswith("Exception when calling")
        # The result should be a non-empty string
        assert len(result) > 0
