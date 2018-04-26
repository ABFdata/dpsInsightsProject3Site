# Dependencies
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import warnings
warnings.filterwarnings('ignore')

# default web search to concatenate
default = "https://www.yelp.com/search?find_desc="
locationUrl = "&find_loc="
end = "&ns=1"

# empty lists to append to
# url = []
# business_name = []
# business_category = []
# yelp_rating = []
# review_count = []
# price_range = []
# price_category = []
# address = []
# phone = []
# website = []

# function to search input parameters on Yelp
def search_yelp(search, zipcode):
    url = []
    keyword = search;
    zipcode = zipcode;
    query_url = f"{default}{search}{locationUrl}{zipcode}{end}";
    response = requests.get(query_url)
    soup = BeautifulSoup(response.text, 'html.parser');
    for link in soup.find_all('a', class_="biz-name"):
        url.append("https://www.yelp.com"+link.get('href'))
    url.pop(0)
    print (url)
    scrape_yelp(url,search, zipcode)

    # function to scrape yelp data on each page
def scrape_yelp(url, search, zipcode):
    search = search
    zipcode = zipcode
    business_name = []
    business_category = []
    yelp_rating = []
    review_count = []
    price_range = []
    price_category = []
    address = []
    phone = []
    website = []
    print ("Hello")
    for i in url:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'html.parser')
        business_name.append(soup.find('h1', attrs={'class':'biz-page-title'}).text.strip())
        business_category.append(soup.find(attrs={'class': 'category-str-list'}).text.strip())
        yelp_rating.append(soup.find(attrs={"class":"i-stars"})["title"])
        review_count.append(soup.find(attrs={'class': 'review-count rating-qualifier'}).text.strip())
        
        if soup.find(attrs={'class': 'business-attribute price-range'}) is not None:
            price_range.append(soup.find(attrs={'class': 'business-attribute price-range'}).text.strip())
        else:
            price_range.append('unknown')
        
        if soup.find(attrs={'class': 'nowrap price-description'}) is not None:
            price_category.append(soup.find(attrs={'class': 'nowrap price-description'}).text.strip())
        else:
            price_category.append('unkown')
        
        address.append(soup.find(attrs={'class': 'street-address'}).text.strip())
        phone.append(soup.find(attrs={'class': 'biz-phone'}).text.strip())
        
        if soup.find("a", href=lambda href: href and "biz_redir?" in href) is not None:
            website.append(soup.find("a", href=lambda href: href and "biz_redir?" in href).text.strip())
        else:
            website.append('no website')     
    print (business_name)
    create_table(business_name, business_category, yelp_rating,review_count, price_range, price_category, address, phone, website, search, zipcode)

# create a dataframe with yelp data from yelp scrape
def create_table(business_name, business_category, yelp_rating,review_count, price_range, price_category, address, phone, website, search, zipcode):
    search = search
    zipcode = zipcode
    data = {
    'BusinessName' : business_name,
    'BusinessCategory' : business_category,
    'YelpRating' : yelp_rating,
    'ReviewCount' : review_count,
    'PriceRange($)' : price_range,
    'PriceCategory': price_category,
    'Address' : address, 
    'Phone' : phone,
    'Website' : website       
    }
    
    # return data
    df = pd.DataFrame.from_dict(data) 
    
    df = df[['BusinessName','BusinessCategory','YelpRating','ReviewCount','PriceRange($)', 'PriceCategory','Address',
            'Phone', 'Website']]
    df.to_csv(f'data/yelp_{search}{zipcode}.csv')
    print (df)
    return df
