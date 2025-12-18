"""
Utility function tests.
"""

import re

import pytest


class TestStringUtilities:
    """Tests for string utility functions."""

    def test_string_not_empty(self):
        """Test string validation."""
        test_string = "Hello, Helix!"
        assert len(test_string) > 0
        assert isinstance(test_string, str)

    def test_email_format_validation(self):
        """Test basic email format validation."""

        def is_valid_email(email: str) -> bool:
            """Simple email validation."""
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return bool(re.match(pattern, email))

        valid_emails = ["test@example.com", "user.name@domain.org", "admin@site.co.uk"]
        for email in valid_emails:
            assert is_valid_email(email), f"{email} should be valid"

        invalid_emails = ["invalid", "no@domain", "@nodomain.com", "missing@. com", ""]
        for email in invalid_emails:
            assert not is_valid_email(email), f"{email} should be invalid"


class TestDataValidation:
    """Tests for data validation."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            (1, True),
            (0, False),
            (-1, True),
            (100, True),
        ],
    )
    def test_integer_boolean_conversion(self, value, expected):
        """Test integer to boolean conversion."""
        assert bool(value) == expected

    @pytest.mark.parametrize(
        "input_list,expected_length",
        [
            ([], 0),
            ([1], 1),
            ([1, 2, 3], 3),
            (list(range(100)), 100),
        ],
    )
    def test_list_length(self, input_list, expected_length):
        """Test list length calculation."""
        assert len(input_list) == expected_length
