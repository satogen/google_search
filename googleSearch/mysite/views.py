from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import pandas as pd
from .forms import SearchForm


def query_string_remove(url):
    return url[:url.find('&')]
    
def counter_evaluation(counter):
    pagecounter = []
    if counter == "":
        counter = 0
        pagecounter.append(counter)
        print('counter no value!')
    elif counter == "0":
      counter = int(counter)
      pagecounter.append(counter)
      print('this is 0')
    else:
        counter = int(counter)
        pagecounter = range(0, counter, 10)
    return pagecounter

def get_search_results(keyword, counter):
    links = []
    titles = []
    pagecounter = counter_evaluation(counter)
    print(pagecounter)
    if keyword.find('https://') > -1 or keyword.find('http://') > -1:
        results = get_find_url(keyword)
    else:
        for i in pagecounter:
            html_doc = requests.get("https://www.google.com/search?q=" + keyword + "&start=" + str(i)).text
            soup = BeautifulSoup(html_doc, 'html.parser')
            tags = soup.find_all('div', class_= 'kCrYT')
            for tag in tags:
                link = tag.select("a")
                if link:
                    link = query_string_remove(link[0].get("href").replace("/url?q=",""))
                    links.append(link)
                    title = get_title(link)
                    titles.append(title)
        results = zip(titles, links)
    return results

def get_find_url(url):
    titles = []
    urls = []
    title = get_title(url)
    titles.append(title)
    urls.append(url)
    results = zip(titles, urls)
    print('Search url!!' + title + url)
    return results


def get_aflinks(url, aflinks):
    urls = []
    # a8_link = "a8.net"
    print('second URL' + url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select("a")
    print(tags)
    for tag in tags:
        try:
            url = tag.get("href")
            if url is not None:
                for aflink in aflinks:
                    if url.find(aflink) > -1 :
                        urls.append(url)
                        # print(urls)
        except Exception as e:
            print('error')
            continue
    print('complite')

    return urls

def get_title(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').string
    if title.find('404') > -1 or title.find('400') > -1 or title.find('不適切なページ名') > -1 or title.find("can't be found.") > -1:
        print("404 error")
        return False
    else:
        print("get title")
        return title


def index(request):
    form = SearchForm(request.POST or None)
    titles = []
    links = []
    urls = {}
    if form.is_valid():
        keyword = form.cleaned_data['text']
        aflinks = form.cleaned_data['two']
        pagecounter = form.cleaned_data['pages']
        search_results = get_search_results(keyword, pagecounter)
        results = search_results
        for title, link in search_results:
            print('Therd link!' + link)
            titles.append(title)
            links.append(link)
            urls[title] = get_aflinks(link, aflinks)
            # print(urls[title])
        results = zip(titles, links)
        # print(titles)
        # print(links)
        # print(list(results))
        count = 1
        return render(request, 'index.html', {'form': form, 'results': results, 'urls': urls, 'count': count})
    return render(request, 'index.html', {'form': form})
