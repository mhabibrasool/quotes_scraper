# scrape.py v1.0.1

# import requests, bs4, urlencode
import requests
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlencode

def parse(html_doc):
    ### Ask html_doc for every quote listing in that page.
    listings =  html_doc.find_all('div', {'class': 'quote'})
    
    ### Empty list
    page_quote = []
    
    ### Quotes, authors, tags
    for listing in listings:
        quotes = {
                'Quote' : listing.find('span', {'class' : 'text'}).text,
                'Author' : listing.find('small', {'class': 'author'}).text,
                'Tags' : [data.text for data in listing.find_all('a', {'class': 'tag'})]
                }
        
        page_quote.append(quotes)
    return page_quote
    ### Ask html_doc for the next page.


def main():
    # Launch requests.get for a response.
    response = requests.get('https://quotes.toscrape.com')    ## If it response.status_code== 200 
    if response.status_code == 200:
        
        # Requests successful, then extract the bs4 html code.
        soup = bs4(response.content, 'html.parser')
        
        # Call function parse(html_doc).
        output = parse(soup)
        
        next_page = 'https://quotes.toscrape.com' + soup.find('li', {'class': 'next'}).find('a').get('href')
        while next_page is not None:
            response = requests.get(next_page)
            soup = bs4(response.content, 'html.parser')
            output.append(parse(soup))
        else:
            pass
    
    else:           # Requests failed.
        print('Requests failed with', response.status_code)
    print(output)
        
if __name__ == '__main__':
    main()
    
