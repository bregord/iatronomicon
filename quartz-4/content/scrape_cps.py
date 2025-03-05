import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time

# Base URL of the Clinical Problem Solvers website
base_url = 'https://clinicalproblemsolving.com'

# Function to download PDFs
def download_pdf(pdf_url, subspecialty_folder):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_name = pdf_url.split('/')[-1]
        pdf_path = os.path.join(subspecialty_folder, pdf_name)
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {pdf_name} to {subspecialty_folder}")
    else:
        print(f"Failed to retrieve: {pdf_url}")

# Function to scrape the list of frameworks from the main page
def scrape_framework_list(start_url):
    # Request the main page
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links in the alphabetical list
    # Assuming the links to the framework pages are contained in <a> tags, you may need to inspect the HTML structure of the page
    links = soup.find_all('a', href=True)

    # Loop through each link in the list
    for link in links:
        framework_url = urljoin(base_url, link['href'])
        
        # Check if the link appears to be related to a framework (for example, we could check if the URL contains "framework" or a similar term)
        if 'framework' in framework_url.lower():
            print(f"Visiting {framework_url}")
            scrape_framework_page(framework_url)
            time.sleep(1)  # Adding delay to avoid overwhelming the server

# Function to scrape each framework page and download the PDF
def scrape_framework_page(framework_url):
    # Request the framework page
    response = requests.get(framework_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for a PDF link on the page
    pdf_link = None
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.pdf'):
            pdf_link = urljoin(framework_url, link['href'])
            break  # Assuming there's only one PDF per framework page, stop after finding it
    
    if pdf_link:
        # Create a folder for the framework if it doesn't exist
        framework_name = framework_url.split('/')[-1]  # Or extract it from the URL if needed
        framework_folder = os.path.join('clinical_pdfs', framework_name)
        
        if not os.path.exists(framework_folder):
            os.makedirs(framework_folder)
        
        # Download the PDF
        download_pdf(pdf_link, framework_folder)
    else:
        print(f"No PDF found for {framework_url}")

# Start scraping from the main page (replace with the actual URL that contains the alphabetical list of frameworks)
scrape_framework_list(base_url)
