import requests
from bs4 import BeautifulSoup
import os, re


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

def scrapePages(images, name):
    """
    Scrapes a webpages for photos of an aircraft and downloads them
    :param images: Number of images to download
    :param name: Name of the aircraft
    """
    url = "https://www.airfighters.com/photosearch.php?key=" + name
    url_data = requests.get(url)
    print(url_data.url)
    if url_data.url.find("noresults") != -1:
        print(name + " could not be found in the database")
        return

    pages, photosAPage, totalPhotos = info(BeautifulSoup(url_data.content, "html.parser"))
    photos = 0
    url_data = ""
    print("Total Photos for " + name + " in database: " + str(totalPhotos))

    for i in range(pages):
        url_data = requests.get(url + "&pag=" + str(i + 1))
        soup = BeautifulSoup(url_data.content, "html.parser")
        jobs = soup.find_all("div", class_="row full-detail-row no-gutters pt-0 mb-5")
        for job_element in jobs:
            picture = job_element.find("img", class_ = "img-fluid")
            found = job_element.find_all("li", class_="list-item")[2].find("span").find_all("a")[1].contents[0]
            if found.lower().find(name.lower()) != -1:
                downloadImage("https://www.airfighters.com/" + picture['src'], photos, name)
                photos += 1
            if photos == images:
                return


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
    aircraft = input("What aircraft do you want images of? ")
    numImages = int(input("How many images do you want? "))
    scrapePages(numImages, aircraft)    

if __name__ == "__main__":
    main()