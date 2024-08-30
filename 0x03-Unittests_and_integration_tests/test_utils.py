#!/usr/bin/env python3
"""
Unit tests module for utils.access_nested_map.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Class contains unit tests for utils.access_nested_map.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Ensure access_nested_map returns the expected result.
        """
        actual_output = access_nested_map(map, path)
        self.assertEqual(actual_output, expected_result)

    @parameterized.expand([
       ({}, ("a",), 'a'),
       ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_nested_map_exception(self, map, path, expected_exc):
        """
        Ensure access_nested_map raises the expected exception.
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(map, path)
        self.assertEqual(expected_exc, str(e.exception))


class TestGetJson(unittest.TestCase):
    """
    Class contains unit tests for utils.get_json.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Ensure get_json returns the expected result using unittest.mock.patch.
        """
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Class contains unit tests for utils.memoize decorator.
    """

    class TestClass:
        """
        The inner class is used to test memoization with utils.memoize.
        """

        def a_method(self):
            """
            The method returns a constant value (42).
            """
            return 42

        @memoize
        def a_property(self):
            """
            The property memoized and calls a_method to get the value.
            """
            return self.a_method()

    @patch('test_utils.TestMemoize.TestClass.a_method', new_callable=Mock)
    def test_memoize(self, mock_a_method):
        """
        Ensure memoization works as expected using unittest.mock.patch.
        """
        mock_a_method.return_value = 42

        instance = self.TestClass()

        result_1 = instance.a_property()
        result_2 = instance.a_property()

        mock_a_method.assert_called_once()

        self.assertEqual(result_1, 42)
        self.assertEqual(result_2, 42)
