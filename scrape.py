from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

if __name__ == '__main__':
    hop_df = pd.DataFrame({'Hop':[], 'Property':[], 'Value':[]})
    index_url = 'https://ychhops.com/varieties'
    index_soup = BeautifulSoup(urlopen(index_url), 'html.parser')
    index_a_href = index_soup.find_all('a', href=True, attrs={'class':'card__button expanded-details blue', 'itemprop':'url'})

    hop_urls = [index_a_href[0]['href']]
    for i in range(1, len(index_a_href)):
        hop_urls.append(index_a_href[i]['href'])

    for i in range(0, len(hop_urls)):
        print('Scraping page %s of %s' % (i+1, len(hop_urls)))
        soup = BeautifulSoup(urlopen(hop_urls[i]), 'html.parser')
        hop = soup.title.text.split(" - ")[0]
        hop_composition_items = soup.find_all('div', attrs={'class': 'hop-composition__item'})
        hop_composition_values = soup.find_all('div', attrs={'class': 'hop-composition__value'})
        hop_description = soup.find('p', attrs={'itemprop': 'description'}).p.text
        hop_purpose = soup.find('div', attrs={'itemprop':'additionalProperty'}).text
        hop_origin = soup.h5.text
        for j in range(0, len(hop_composition_items)):
            hop_df = hop_df.append(
                pd.DataFrame({'Hop': [hop],
                              'Origin': [hop_origin],
                              'Property': [hop_composition_items[j].text],
                              'Value': [hop_composition_values[j].text]}),
                ignore_index = True)

        hop_df = hop_df.append(
            pd.DataFrame({'Hop': [hop]*2,
                          'Origin': [hop_origin]*2,
                          'Property': ['Description', 'Purpose'],
                          'Value': [hop_description, hop_purpose]}),
            ignore_index = True)
        sleep(1.0)

    hop_df.to_csv('raw_hops.csv')
