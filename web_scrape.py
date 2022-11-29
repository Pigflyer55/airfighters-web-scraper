import requests
from bs4 import BeautifulSoup
import os, re

#URL = "https://www.airfighters.com/photosearch.php?key=P-51"
URL = "https://www.airfighters.com/photosearch.php?key=F-22&pag=2"
page = requests.get(URL)

#print(page.text)
"""
soup = BeautifulSoup(page.content, "html.parser")
jobs = soup.find_all("div", class_="row full-detail-row no-gutters pt-0 mb-5")
for job_element in jobs:
    found = job_element.find("img", class_ = "img-fluid")
    print(found['src'], end="\n"*2)
"""

def info(soup):
    """
    Get information about amount of photos per page and total amount of photos
    """
    data = soup.find("div", class_ = "text-right pr-1 my-2")
    pages = data.find("span", class_= "text-large text-muted").previous_sibling.string.replace('\n', '')
    photosAPage = data.find("span", class_= "text-large text-muted").next_sibling.string
    photosTotal = data.find("span", class_= "d-none d-lg-inline-block").previous_sibling.string

    pagesMatch = re.search(r'\d+', pages).span()
    pagesNew = pages[pagesMatch[0]:pagesMatch[1]]

    return int(pagesNew), photosAPage, photosTotal

def scrapePages(images = 1000):
    return

def downloadImage():
    
    print()

def main():
    """ #Dovvnload image code
    img_url = "https://www.airfighters.com/photo_400_338322.jpg"
    img_data = requests.get(img_url).content
    with open("ac-130.jpg", 'wb') as handler:
        handler.write(img_data)
    """
    aircraft = input("What aircraft do you want images of? ")
    url = "https://www.airfighters.com/photosearch.php?key=" + aircraft
    url_data = requests.get(url)
    print(url_data.url)
    if url_data.url.find("noresults") != -1:
        print("not found")
    else:
        print("found")
    url2 = "https://www.airfighters.com/photosearch.php?key=Bf-109&pag=7"
    url2_data = requests.get(url2)
    print(url2_data.url)
    if url2_data.url.find("noresults") != -1:
        print("not found")
    else:
        print("found")

    soup = BeautifulSoup(url2_data.content, "html.parser")
    #soup.next_sibling
    #jobs = soup.find("div", class_="row no-gutters mb-3")
    found = soup.find("div", class_ = "text-right pr-1 my-2")
    print(found.find("span", class_= "text-large text-muted").previous_sibling.string)
    print(info(soup))

    

if __name__ == "__main__":
    main()