# Import necessary libraries
import requests
from bs4 import BeautifulSoup

def get_erp_solutions():
    """
    Scrapes the web for existing ERP solutions and returns a list of URLs.
    
    Returns:
        list: A list of URLs for different ERP solutions.
    """
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
    return urls

def get_feedback(urls):
    """
    Sends a GET request to each URL and extracts user feedback.
    
    Args:
        urls (list): A list of URLs for ERP solutions.
    
    Returns:
        dict: A dictionary with solution names as keys and their respective feedback as values.
    """
    solutions = {}
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', class_='firstHeading').text
        feedback = []
        # Extract user feedback from the page (simplified example, you may need to adjust this based on actual page structure)
        for p in soup.find_all('p'):
            feedback.append(p.text.strip())
        solutions[name] = ' '.join(feedback)
    return solutions

def main():
    urls = get_erp_solutions()
    feedback = get_feedback(urls)
    print("ERP Solutions Feedback:")
    for solution, text in feedback.items():
        print(f"{solution}: {text}")

if __name__ == "__main__":
    main()

```

Note: This script scrapes Wikipedia pages to gather information about ERP solutions and their user feedback. You may need to adjust the code based on the actual structure of the web pages you're scraping.

Also, be aware that web scraping might not always yield accurate results or be allowed by the websites being scraped. Always check the terms of service for any website before using automated scripts like this one.

This script also does not handle potential exceptions when making GET requests to the URLs. You may want to add error handling code depending on your needs.