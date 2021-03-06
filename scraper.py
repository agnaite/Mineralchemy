from bs4 import BeautifulSoup
from unicodedata import normalize
import urllib

def scrape_minfind(keywords, min_price, max_price):
	"""Scrape Minfind for listings within price range and return number of listings and array of dictionaries."""

	# Scrape initial search page with only keywords
	url = "http://www.minfind.com/search.php?" + urllib.urlencode({"qs":keywords})
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")
	minfind_listings = []

	listings = soup.find_all("div", {"class":"minbox"})
	count = 0

	for listing in listings:
		listing_price = float(listing.find("div", {"class":"minboxprice"}).string[1:])

		# Filter the listings within price range
		if listing_price > min_price and listing_price < max_price:
			listing_dict = {
				"listing_id": int(filter(str.isdigit, listing.a['href'])),
				"listing_origin": "minfind",
				"url": "http://www.minfind.com/" + listing.a['href'],
				"title": listing.find("div", {"class":"minboxmin"}).string.encode(encoding='UTF-8',errors='strict'),
				"price": listing_price
			}

			# Scrape individual listing details page to access description and all images
			details_html = urllib.urlopen(listing_dict["url"]).read()
			details_soup = BeautifulSoup(details_html, "lxml")
			main_content = details_soup.find("div", {"id":"maincontent"})

			unicode_description = main_content.find("div", {"class":"fptext"}).contents[2]
			listing_dict["description"] = unicode_description


			image_urls = []
			links = main_content.find("div", {"class":"allimages"}).findAll("a")
			for a in links:
				image_urls.append("http://www.minfind.com" + a['href'])
			listing_dict["image_urls"] = image_urls

			count += 1
			minfind_listings.append(listing_dict)

	return count, minfind_listings
