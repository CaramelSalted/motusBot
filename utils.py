from random import choice

from clarifai.rest import ClarifaiApp
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases = True)
        return user_data['emo']

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact = True)
    location_button = KeyboardButton('Прислать локацию', request_location = True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Сменить эмоджи'],
                                        [contact_button, location_button],
                                        ['Заполнить анкету'] 
                                       ], resize_keyboard=True)
    return my_keyboard

def is_cat(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)

    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                return True
    return False

if __name__ == "__main__":
    print(is_cat('img/pink.jpg'))