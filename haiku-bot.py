import nltk
import requests
import random
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('cmudict', quiet=True)

d = cmudict.dict()

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1340337011764105216/zkcknnI6hz1fsBP0kH0V8n6hQWNK0jnVV2x714kZZIu_w11PbGVU9tVTv_JSZVYlg8am" 

def syllable_count(word):
    word = word.lower()
    if word in d:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word]])
    return 0

def generate_haiku(headline):
    words = word_tokenize(headline)
    valid_words = [word for word in words if syllable_count(word) > 0]
    
    if len(valid_words) < 5:
        return None  

    haiku = []
    syllable_target = [5, 7, 5]

    for target in syllable_target:
        line = []
        current_syllables = 0

        while current_syllables < target and valid_words:
            word = valid_words.pop(0)
            word_syllables = syllable_count(word)
            
            if current_syllables + word_syllables <= target:
                line.append(word)
                current_syllables += word_syllables
        
        if current_syllables != target:
            return None  

        haiku.append(" ".join(line))

    return "\n".join(haiku)

def fetch_headlines():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=90d47526d1d843d38d13863e52c93a74'
    response = requests.get(url)
    if response.status_code == 200:
        return [article['title'] for article in response.json()['articles']]
    return []

def send_to_discord(haiku):
    data = {"content": haiku}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def main():
    headlines = fetch_headlines()
    random.shuffle(headlines)  

    for headline in headlines:
        haiku = generate_haiku(headline)
        if haiku:
            send_to_discord(haiku)
            return  

if __name__ == "__main__":
    main()
