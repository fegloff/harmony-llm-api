import logging
import requests
from res import config

class WebCrawling:

    def __init__(self):
        self.base_url = config.WEB_CRAWLER_HTTP 

    def get_web_content(self, url, username=None, password=None):
        if not url.startswith("https://"):
            url = "https://" + url
        credentials = f"&username={username}&password={password}" if username and password else ""
        request_url = f"{self.base_url}parse?url={url}{credentials}"
        logging.info(request_url)

        try:
            response = requests.get(request_url)
            response.raise_for_status()
            result = response.json()

            logging.info(
                f"Webcrawling {url} => Tags processed: {len(result['elements']) if 'elements' in result else 0}"
            )

            chunks = self.parse_web_content(result['elements'])
            return {
                "urlText": chunks,
                "elapsedTime": result.get("elapsedTime", 0),
                "networkTraffic": result.get("networkTraffic", 0),
                "fees": 0.5,
                "oneFees": 0.5,
            }
        except requests.exceptions.RequestException as e:
            raise e

    def clean_web_crawl(self, chunks):
        filter_chunks = [i for i in chunks if i['tagName'] != 'a' and i['tagName'] != 'code']
        return [i['text'] for i in filter_chunks]
    
    def parse_web_content(self, input_array):
        max_words = 24000
        concatenated_text = ''
        current_word_count = 0
        chunks = []
        no_duplicates = list(set(self.clean_web_crawl(input_array)))
        
        for item in no_duplicates:
            words = item.split()
            word_count = len(words)
            
            if current_word_count + word_count <= max_words:
                concatenated_text += item + ' '
                current_word_count += word_count
            else:
                chunks.append(concatenated_text)
                concatenated_text = ''
                current_word_count = 0

        if concatenated_text != '':
            chunks.append(concatenated_text)
        
        return chunks