#!/usr/bin/env python3
"""
Module contains unit tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Class contains unit tests for client.GithubOrgClient.
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, org_name, mock_get_json):
        """
        Method to test org of GithubOrgClient
        """
        expected_result = {org_name: True}
        mock_get_json.return_value = expected_result
        github_org_client = GithubOrgClient(org_name)

        result = github_org_client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_result)

    def test_public_repos_url(self):
        """
        Test _public_repos_url method of GithubOrgClient
        """
        expected = 'https://api.github.com/orgs/testorg/repos'
        cli = GithubOrgClient('testorg')

        result = cli._public_repos_url

        self.assertEqual(result, expected)

    @patch('client.GithubOrgClient.get_json', return_value=[
           {'name': 'repo1'}, {'name': 'repo2'}])
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock,
           return_value='https://api.github.com/orgs/testorg/repos')
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test public_repos method of GithubOrgClient
        """
        expected_repos = [{'name': 'repo1'}, {'name': 'repo2'}]
        cli = GithubOrgClient('testorg')

        result = cli.public_repos

        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/testorg/repos')
        self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test has_license method of GithubOrgClient
        """
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value='https://api.github.com/orgs/testorg/repos'):
            with patch('client.GithubOrgClient.get_json', return_value=[repo]):
                cli = GithubOrgClient('testorg')
                result = cli.has_license(license_key)
                self.assertEqual(result, expected_result)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [
        ({'org_key': 'org_value'}, {'repos_key': 'repos_value'},
         {'expected_key': 'expected_value'}, {'apache2_key': 'apache2_value'})
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class for the test suite
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload),
            Mock(json=lambda: cls.expected_repos),
            Mock(json=lambda: cls.apache2_repos)
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class for the test suite
        """
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """
        Integration test for public_repos method
        """
        cli = GithubOrgClient('testorg')
        result = cli.public_repos

        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license_integration(self):
        """
        Integration test for public_repos method with license argument
        """
        cli = GithubOrgClient('testorg')
        result = cli.public_repos(license="apache-2.0")

        self.assertEqual(result, self.apache2_repos)
