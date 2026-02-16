import unittest
from main import get_erp_solutions, get_feedback
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
import requests

class TestEps(unittest.TestCase):

    @patch('requests.get')
    def test_get_erp_solutions(self, mock_get):
        mock_response = Mock()
        mock_response.text = '<html><body><table class="wikitable sortable"><tr><td><a href="https://example.com">Example</a></td></tr></table></body></html>'
        mock_get.return_value = mock_response
        urls = get_erp_solutions()
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0], 'https://example.com')

    @patch('requests.get')
    def test_get_feedback(self, mock_get):
        mock_response = Mock()
        mock_response.text = '<html><body><h1>Example</h1><p>This is some feedback.</p></body></html>'
        mock_get.return_value = mock_response
        urls = ['https://example.com']
        feedback = get_feedback(urls)
        self.assertEqual(feedback['Example'], 'This is some feedback.')

    def test_get_erp_solutions_empty_table(self):
        url = "https://en.wikipedia.org/wiki/Comparison_of_enterprise_resource_planning_software"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table', class_='wikitable sortable')[0]
        urls = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) > 2:
                url = cols[1].find('a')['href']
                if not url.startswith('http'):
                    url = 'https://en.wikipedia.org' + url
                urls.append(url)
        self.assertEqual(len(urls), 0)

if __name__ == '__main__':
    unittest.main()