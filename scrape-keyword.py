# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Initialize an empty list to hold the scraped data
data=[]

# Define the keyword(s) to be used for the search
keywords ='kidnap'

# Define a function to scrape news articles from a given webpage for a specific keyword
def find_news(keyword,pageNo):
    # Define the base url of the website to be scraped
    base_url = 'https://punchng.com/page/'
    # Define the specific search query to be used for the keyword
    key= '/?s='+ keyword
    # Combine the base url, page number and search query to form the complete url to be scraped
    url = base_url+ str(pageNo)+key
    # Use the requests library to fetch the HTML content of the page
    html_text= requests.get(url).text
    # Use BeautifulSoup to parse the HTML content
    soap = BeautifulSoup(html_text,'html.parser')
    # Find all the articles on the page
    articles = soap.find_all('article')

    # Loop through each article and extract relevant data
    for article in articles:
        # Find the article title
        title = article.find_all('h1',class_='post-title')
        if title is not None:
            # Loop through all the titles (there might be more than one) and extract the text content
            for i in title:
                title = i.text.strip()
                # Find the brief summary of the article
                content= article.find('p', class_='post-excerpt').text.strip()
                # Find the link to the full article
                links= i.a['href']
                # Use requests to fetch the full article page
                article_response = requests.get(links)
                # Use BeautifulSoup to parse the full article page
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                # Find the full content of the article
                news_=article_soup.find_all('div',class_='post-content')
                # Find the date the article was published
                pub_date =article_soup.find('span',class_='post-date').text.strip()
                # Loop through all the full content sections (there might be more than one) and extract the text content
                for news_article in news_:
                    news = news_article.find('p')
                    if news is not None:
                        # Append the extracted information to the data list
                        data.append({'Date_published':pub_date,'Title': title, 'Brief_summary':content,
                                     'Full_Content': news.text.strip()})

# Loop through a specified number of pages and call the find_news function for each page
for x in range(1,3):
    find_news(keywords,x) 

# Convert the data list into a pandas dataframe
df=pd.DataFrame(data)

# Exporting the dataframe to an Excel file
df.to_excel('Kidnap.xlsx')

# Print a success message to the console
print('Exported Successfully')
