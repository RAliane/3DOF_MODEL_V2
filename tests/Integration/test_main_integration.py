# tests/integration/test_main_integration.py
import pytest
from main import main
from unittest.mock import patch

@patch("time.sleep")
def test_main_integration(mock_sleep):
    with patch("builtins.print") as mock_print:
        main()
        assert mock_print.call_count == 1000
