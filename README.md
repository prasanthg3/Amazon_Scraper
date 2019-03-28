# Amazon-Scraper #
amazon_scraper.py can be used to scrape product data from Amazon.in's search results.
## List of details scraped ##

* ASIN
* NAME
* SELLER
* SALE_PRICE
* CATEGORY
* AVAILABILITY
* URL
* AVG_RATING
* NO_OF_REVIEWS

# Requirements #
* Python 3
* pandas
* lxml
* requests

# Usage
Change the url in line 125 to your requirement ( page1 url of the search result). Then from the command prompt, execute 
***py amazon_scraper.py***  to get the output csv file containing list of product details
