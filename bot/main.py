import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
API_DOGS_URL: str = 'https://random.dog/woof.json'
BOT_TOKEN: str = '5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0'
ERROR_TEXT: str = 'Здесь должна была быть картинка с собачкой :('

offset: int = -2
counter: int = 0
dog_response: requests.Response
dog_link: str


while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1