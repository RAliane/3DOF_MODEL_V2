import pytest
from unittest.mock import MagicMock
from src.directus_client import DirectusClient

def test_directus_client(mocker):
    mock_client = MagicMock()
    mocker.patch("directus.Directus", return_value=mock_client)

    client = DirectusClient("http://localhost:8055", "admin@example.com", "admin")
    client.log_data("flight_logs", {"altitude": 1000})

    mock_client.items.return_value.create.assert_called_once_with({"altitude": 1000})
    client.close()
