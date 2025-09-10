#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient class
"""
import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Set up mock return value
        test_payload = {"org": org_name}
        mock_get_json.return_value = test_payload

        # Create client instance
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Verify get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Verify the result matches the mock return value
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value"""
        # Mock payload for org method
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        # Patch the org property to return our test payload
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value=test_payload):
            # Create client instance
            client = GithubOrgClient("testorg")

            # Call the _public_repos_url property
            result = client._public_repos_url

            # Verify the result matches the expected URL
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list of repos"""
        # Mock payload for repos_payload
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = test_repos_payload

        # Mock the _public_repos_url property
        test_repos_url = "https://api.github.com/orgs/testorg/repos"
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value=test_repos_url):
            # Create client instance
            client = GithubOrgClient("testorg")

            # Call public_repos method
            result = client.public_repos()

            # Verify get_json was called once with correct URL
            mock_get_json.assert_called_once_with(test_repos_url)

            # Verify the result matches expected repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean value"""
        # Create client instance (static method, so no need for org setup)
        result = GithubOrgClient.has_license(repo, license_key)

        # Verify the result matches expected value
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class method for integration tests"""
        # Create a patcher for requests.get
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Set up side effect to return different payloads based on URL
        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/testorg":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method for integration tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method"""
        # Create client instance
        client = GithubOrgClient("testorg")

        # Call public_repos method
        result = client.public_repos()

        # Verify the result matches expected repos
        self.assertEqual(result, self.expected_repos)

        # Verify requests.get was called twice (org + repos)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        # Create client instance
        client = GithubOrgClient("testorg")

        # Call public_repos method with license filter
        result = client.public_repos(license="apache-2.0")

        # Verify the result matches expected apache2 repos
        self.assertEqual(result, self.apache2_repos)

        # Verify requests.get was called twice (org + repos)
        self.assertEqual(self.mock_get.call_count, 2)


if __name__ == '__main__':
    unittest.main()
