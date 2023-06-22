import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN
from utils import *
from weatherShow import WeatherShow
from citysList import citysList

citys = citysList()

bot = telebot.TeleBot(TOKEN)
weath = WeatherShow()

usualKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [KeyboardButton("добавить город"),
        KeyboardButton("удалить город"),
        KeyboardButton("установить город по умолчанию"),
        KeyboardButton("посмотреть погоду(город по умолчанию)"),
        KeyboardButton("помощь")]
usualKeyboard.add(*buttons)

@bot.message_handler(commands=['start'])
def say_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте, это бот для слежения за погодой. Для справки введите /help\nв клавиатуре Telegramm также хранятся кнпочки :^)", reply_markup=usualKeyboard)
    # bot.register_next_step_handler(message, nextStep)

@bot.message_handler(commands=['help'])
def help(msg: Message):
    text = '''
    /addcity <город> - добавить город\n
    /delcity <город>- удалить город\n
    /setdefault <город> - устанавливает город по умолчанию\n
    /wrd - погазывает погоду по городу по умолчанию\n
    /wr <город> - показывает погоду по определённому городу\n
    '''
    bot.send_message(msg.chat.id, text)

# @bot.message_handler(content_types='text')
# def cencel(msg: Message):
#     if ( msg.text == '/cencel'):
#         bot.clear_reply_handlers(msg)

@bot.message_handler(commands=['addcity'])
def addCity(message: Message):

    city = getMesCom(message.text, 'addcity')
    errs = citys.addCity(city)
    if ( errs ):
        bot.send_message(message.chat.id, errs[0]+" err")
        return
    
    bot.send_message(message.chat.id, f'город {city} добавлен')

@bot.callback_query_handler(func=lambda call: call.data == "добавить город")
def addCityKey(msg: Message):
    try:
        city = getMesCom(msg.text)
        errs = citys.addCity(city)
        if ( errs ):
            bot.send_message(msg.chat.id, errs[0])
            return
        
        bot.send_message(msg.chat.id, f'город {city} добавлен')
    except AttributeError:
        nextStep(msg)

    
@bot.message_handler(commands=['delcity'])
def delCity(message: Message):

    city = getMesCom(message.text, 'delcity')
    errs = citys.delCity(city)
    if ( errs ):
        bot.send_message(message.chat.id, errs[0])
        return
    
    bot.send_message(message.chat.id, f'город {city} удалён')

@bot.callback_query_handler(func=lambda call: call.message.text == "выберите какой город удалить")
def delCityKey(msg: CallbackQuery):

    try:
        city = getMesCom(msg.data)
        errs = citys.delCity(city)
        if ( errs ):
            bot.send_message(msg.message.chat.id, errs[0])
            return

        bot.send_message(msg.message.chat.id, f'город {msg.data} удалён')
    except AttributeError:
        nextStep(msg)

###############
@bot.message_handler(commands=['setdefault'])
def setDefault(message: Message):
    city = getMesCom(message.text, 'setdefault')
    errs = citys.setdefault(city)
    
    if ( errs ):
        bot.send_message(message.chat.id, errs[0])
        return
    
    bot.send_message(message.chat.id, f"город {city} установлен как 'по умолчанию'")
    return

@bot.callback_query_handler(func=lambda call: call.message.text == "какой город установить по умолчанию?")
def setDefaultKey(call: CallbackQuery):
    try:
        city = getMesCom(call.data)
        errs = citys.setdefault(city)
        
        if ( errs ):
            bot.send_message(call.message.chat.id, errs[0])
            return
        
        bot.send_message(call.message.chat.id, f"город {city} установлен как 'по умолчанию'")
    except AttributeError:
        nextStep(call)

#########weather get city
@bot.message_handler(commands=['wr'])
def wr(message: Message):
    city = getMesCom(message.text, 'wr')
    
    if ( len(city) == 0):
        bot.send_message(message.chat.id, "вы не ввели город")
        return
    
    data = getCityData(city)
    if ( data == None):
        bot.send_message(message.chat.id, "такого города нету")
        return
    
    bot.send_message(message.chat.id, weath.getWeather(data[0]))
#########weather get city

########weather default
@bot.message_handler(commands=['wrd'])
def wrd(message: Message):
    
    city = citys.getDefaultCity()
    print (str(city) + " default act")
    if ( city == None):
        bot.send_message(message.chat.id, "город 'по умолчанию' не установлен")
        return
    wr = weath.getWeather(city[1])
    bot.send_message(message.chat.id, wr)


@bot.message_handler(content_types='text')
# @bot.callback_query_handler(lambda call: True)
def nextStep(msg: Message):
    text = msg.text
    if ( text == 'добавить город'):
        bot.send_message(msg.chat.id, 'введите название города')
        bot.register_next_step_handler(msg,callback=addCityKey)
        
        
    elif ( text == 'удалить город'):
        keyboard = InlineKeyboardMarkup()
        try:
            keyboard.add(*[InlineKeyboardButton(i, callback_data=i) for i in citys.getSaveCitys()])
        except TypeError:
            bot.send_message(msg.chat.id, "в списке нуте сохранённых городов")
            return
        
        bot.send_message(msg.chat.id, 'выберите какой город удалить', reply_markup=keyboard)
        bot.register_next_step_handler(msg, callback=delCityKey)
        
        
    elif ( text == 'установить город по умолчанию'):
        keyboard = InlineKeyboardMarkup()
        try:
            keyboard.add(*[InlineKeyboardButton(i, callback_data=i) for i in citys.getSaveCitys()])
        except TypeError:
            bot.send_message(msg.chat.id, "в списке нуте сохранённых городов")
            return
        
        bot.send_message(msg.chat.id, 'какой город установить по умолчанию?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, callback=setDefaultKey)
        
    elif ( text == 'посмотреть погоду(город по умолчанию)'):
        wrd(msg)
    elif ( text == 'помощь'):
        help(msg)
        
    # elif ( text == 'посмотреть погоду'):
    #     keyboard = InlineKeyboardMarkup()
    #     keyboard.add(*[InlineKeyboardButton(i, callback_data=i) for i in citys.getSaveCitys()])
        
    #     bot.send_message(msg.chat.id, 'введите название города или нажмите на клавиатуре', reply_markup=keyboard)
    #     bot.register_next_step_handler(msg, callback=wrKey)
        
    else:
        pass



bot.infinity_polling()

# addC = KeyboardButton("добавить город")
# delC = KeyboardButton("удалить город")
# default = KeyboardButton("установить город по умолчанию")
# wrd = 