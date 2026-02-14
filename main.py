import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    filename='scraper_log.log', 
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s',
    encoding='utf-8'
)
news1= 'https://www.bbc.com/sport/articles/cly2jknym20o'
newschannel2= 'https://edition.cnn.com/climate/vela-wind-cargo-ship-spc-c2e'
channel3 ='https://www.nytimes.com/2026/02/12/climate/what-to-know-epa-endangerment-finding.html'
with open('links.txt' , 'w') as link:
    link.write(f"{news1}\n{newschannel2}\n{channel3}")
def get_article_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        sup = BeautifulSoup(response.text, 'html.parser')
        
        header = sup.find('h1').text.strip() if sup.find('h1') else 'No title found'
        
        for script in sup(["script", "style"]):
            script.decompose()
            
        paragraph = sup.find_all('p')
        full_text = " ".join([p.text.strip() for p in paragraph])
        
        logging.info(f"Successfully done: {url}")
        return header, full_text
    except Exception as e:
        logging.error(f"Error ocurred ({url}): {e}")
        return None, None 
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
    # Bura çox sadə bir sentiment təxmini əlavə edirik
    positive_words = ["win", "success", "breakthrough", "growth", "new", "efficient"]
    negative_words = ["climate", "crisis", "threat", "risk", "danger", "heavy"]
    
    score = 0
    for w in words:
        if w in positive_words: score += 1
        if w in negative_words: score -= 1
        
    sentiment = "Positive" if score > 2 else ("Negative" if score < -2 else "Neutral")
    
    return word_count, reading_time, top_5, sentiment
    return word_count, reading_time, top_5

latest_result = []
with open('links.txt' , 'r') as f:
    links = f.read().splitlines()
    for link in links:
        print(f'{link} is processing...') 
        header, text = get_article_data(link)
        
        if text:
            wordcount, time, keys, sent = analyze_text(text) 
            information = {
                'Header': header,
                'Word count': wordcount,
                'Reading time (min)': time,
                'Key words': keys,
                'Sentiment': sent,
                'URL': link 
            }
            latest_result.append(information)
        else:
            print(f'Error: No text found for {link}')

print('All links have been processed')

df = pd.DataFrame(latest_result)
df.to_csv('Articles.report.csv' , index=False, encoding='utf-8-sig')
print("Report has been written to 'Articles.report' file")
