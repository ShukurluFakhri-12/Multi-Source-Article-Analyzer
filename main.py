import pandas as pd
import requests
from bs4 import BeautifulSoup
news1= 'https://www.bbc.com/sport/articles/cly2jknym20o'
newschannel2= 'https://edition.cnn.com/climate/vela-wind-cargo-ship-spc-c2e'
channel3 ='https://www.nytimes.com/2026/02/12/climate/what-to-know-epa-endangerment-finding.html'
with open('links.txt' , 'w') as link:
    link.write(f"{news1}\n{newschannel2}\n{channel3}")
def get_article_data(url):
    try:
        response = requests.get(url, timeout=5)
        sup = BeautifulSoup(response.text , 'html.parser')
        header = sup.find('h1').text.strip() if sup.find('h1') else 'No title found'
        paragraph = sup.find_all('p')
        full_text = " ".join([p.text.strip() for p in paragraph])
        return header, full_text
    except Exception as e:
        print(f'Error occurred; {e}')
def analyze_text(text):
    words = text.lower().split()
    word_count = len(words)
    stopwords = ["with", "this", "an", "a", "the", "and", "that"]
    word_counts = {}
    for x in words:
        if x not in stopwords:
            if x in word_counts:
                word_counts[x]+=1
            else:
                word_counts[x]=1
    sorted_keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_keywords[:5]
    reading_time = round(word_count/200)
    return word_count, reading_time, top_5

latest_result =[]
with open('links.txt' , 'r') as f:
    links=f.read().splitlines()
    for link in links:
        print(f'{link} is processed')
        header, text = get_article_data(link)
        if text:
            wordcount, time, keys = analyze_text(text)
            information = {'Header' : header,
                           'Word count' : wordcount,
                           'Reading time' : time,
                           'Key words' : keys,
                           'URL' : link }
            latest_result.append(information)
        else:
            print(f'Error: No text found for {link}')
print('All links have been processed')

df = pd.DataFrame(latest_result)
df.to_csv('Articles.report.csv' , index=False, encoding='utf-8-sig')
print("Report has been written to 'Articles.report' file")
