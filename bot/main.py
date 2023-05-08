import requests
import time

API_URL: str = 'https://api.telegram.org/bot'
API_FOX_URL: str = 'https://randomfox.ca/floof/'
BOT_TOKEN: str = '6094985598:AAE50dKeqOORC3nEuCxO2QHG4Z4UklRaunw'
ERROR_TEXT: str = 'Здесь должна была быть картинка :('

offset: int = -2
counter: int = 0
fox_response: requests.Response
fox_link: str
 

while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            fox_response = requests.get(API_FOX_URL)
            if fox_response.status_code == 200:
                fox_link = fox_response.json()['image']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={fox_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
 

    time.sleep(1)
    counter += 1
