from bs4 import BeautifulSoup
import requests
import pandas as pd

def query_string_remove(url):
    return url[:url.find('&')]
    
keyword = "会社　行きたくない"
def get_search_results_df(keyword):
    columns = ["rank", "title", "url", "affiliate_url"]
    df = pd.DataFrame(columns = columns)
    html_doc = requests.get("https://www.google.com/search?q=" + keyword).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    tags = soup.find_all('div', class_= 'kCrYT')
    rank = 1
    for tag in tags:
        title = tag.text
        link = tag.select("a")
        if link:
            link = query_string_remove(link[0].get("href").replace("/url?q=",""))
            affiliate_url = ""
            se = pd.Series([rank, title, link, affiliate_url], columns)
            df = df.append(se, ignore_index=True)
            rank += 1

search_results_df = get_search_results_df(keyword)
search_results_df.head(10)