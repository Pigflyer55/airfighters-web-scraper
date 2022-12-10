import requests
from bs4 import BeautifulSoup
import os, re

#URL = "https://www.airfighters.com/photosearch.php?key=P-51"
URL = "https://www.airfighters.com/photosearch.php?key=F-22&pag=2"
page = requests.get(URL)

#print(page.text)

soup = BeautifulSoup(page.content, "html.parser")
jobs = soup.find_all("div", class_="row full-detail-row no-gutters pt-0 mb-5")
for job_element in jobs:
    found = job_element.find("img", class_ = "img-fluid")
    print(found['src'], end="\n"*2)


def info(soup):
    """
    Get information about total amount of pages, amount of photos per page, and total amount of photos
    :param soup: Beautiful soup object to extract data from a url
    """
    data = soup.find("div", class_ = "text-right pr-1 my-2")
    pages = data.find("span", class_= "text-large text-muted").previous_sibling.string.replace('\n', '')
    photosAPage = data.find("span", class_= "text-large text-muted").next_sibling.string
    photosTotal = data.find("span", class_= "d-none d-lg-inline-block").previous_sibling.string

    pagesMatch = re.findall(r'\d+', pages)[1]
    photosAPageMatch = re.findall(r'\d+', photosAPage)[0]
    photosTotalMatch = photosTotal.rstrip()

    return int(pagesMatch), int(photosAPageMatch), int(photosTotalMatch)

def scrapePages(url, images, name):
    """
    Scrapes a webpage for photos of an aircraft and downloads them
    :param url: A url of a website
    :param images: Number of images to download
    :param name: Name of the aircraft
    """
    pages, photosAPage, totalPhotos = info(BeautifulSoup(requests.get(url).content, "html.parser"))
    photos = 0
    url_data = ""
    print("Total Photos for " + name + " in database: " + str(totalPhotos))

    for i in range(pages):
        url_data = requests.get(url + "&pag=" + str(i + 1))
        soup = BeautifulSoup(url_data.content, "html.parser")
        jobs = soup.find_all("div", class_="row full-detail-row no-gutters pt-0 mb-5")
        for job_element in jobs:
            found = job_element.find("img", class_ = "img-fluid")
            downloadImage("https://www.airfighters.com/" + found['src'], photos, name)
            photos += 1
            if photos == images:
                break
        if photos == images:
            break


def downloadImage(imgUrl, imgNum, planeName):
    """
    :param imgUrl: A url of the image to be downloaded
    :param imgNum: Number to indicate the nth photo downloaded
    :planeName: Name of the aircraft
    """
    try:
        os.makedirs(planeName)
    except FileExistsError:
        pass

    img_data = requests.get(imgUrl).content
    with open(planeName + "/" + planeName + "_" + str(imgNum) + ".jpg", 'wb') as handler:
        handler.write(img_data)

def main():
    """ #Dovvnload image code
    img_url = "https://www.airfighters.com/photo_400_338322.jpg"
    img_data = requests.get(img_url).content
    with open("ac-130.jpg", 'wb') as handler:
        handler.write(img_data)
    """
    aircraft = input("What aircraft do you want images of? ")
    numImages = int(input("How many images do you want? "))
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
    #print(found.find("span", class_= "text-large text-muted").previous_sibling.string)
    #print(info(soup))
    scrapePages(url, numImages, aircraft)

    

if __name__ == "__main__":
    main()