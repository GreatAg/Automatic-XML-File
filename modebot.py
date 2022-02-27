import telebot
from telebot import types
import modedatabase
import xml.etree.ElementTree as ET
import os
from tenacity import retry, wait_fixed, stop_after_attempt

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    start(message)


def process_first_step(message):
    try:
        user_id = message.chat.id
        info = message.text
        if info == '🔆ساختن مود🔆':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
            markup.add('🔹بازگشت🔹')
            msg = bot.reply_to(message, '❕اسم مود خود را وارد کنید❕',reply_markup=markup)
            bot.register_next_step_handler(msg, process_second_step)
        elif info == '🔆ویرایش پروژه🔆':
            load_projects(message)
        elif info == '🔆دریافت فایل مود🔆':
            selectname(message)
        elif info == '🔆حذف پروژه🔆':
            selectfile(message)
        elif info == '/start':
            start(message)
        else:
            bot.send_message(user_id, '❕لطفا از دکمه ها استفاده کنید❕')
            start(message)
    except:
        bot.reply_to(message, 'oooops')


def process_second_step(message):
    try:
        user_id = message.chat.id
        info = message.text
        load = modedatabase.load_pj(user_id)
        if info == '🔹بازگشت🔹':
            start(message)
        elif info == '/start':
            start(message)
        elif info in load:
            bot.send_message(user_id,'❕اين اسم قبلا ثبت شده❕')
            start(message)
        else:
            modedatabase.insert_information(user_id, info)
            bot.send_message(user_id, '⚜️پروژه شما با موفقیت ساخته شد⚜️')
            build_xml(user_id, info)
            start(message)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def removepj(message):
    user_id = message.chat.id
    name = message.text
    if name == '🔹بازگشت🔹':
        start(message)
    elif name == '/start':
        start(message)
    else:
        try:
            modedatabase.delete_project(user_id, name)
            os.remove(f'{user_id}-{name}.xml')
            os.renames()
            bot.send_message(user_id, '⚜️پروژه شما با موفقیت حذف شد⚜️')
            start(message)
        except:
            bot.send_message(user_id, '❕لطفا از دكمه هاي موجود استفاده كنيد❕')
            selectfile(message)


def build_mark(load):
    li = []
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    for e, i in enumerate(load,start=1):
        li.append(i)
        if e % 3 == 0 and e:
            markup.add(telebot.types.KeyboardButton(li[0]), telebot.types.KeyboardButton(li[1]),
                       telebot.types.KeyboardButton(li[2]))
            li = []
    if li:
        if len(li) == 1:
            markup.add(telebot.types.KeyboardButton(li[0]))
        else:
            markup.add(telebot.types.KeyboardButton(li[0]), telebot.types.KeyboardButton(li[1]))
    return markup


def start(message):
    message_id = message.message_id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
    markup.add('🔆ساختن مود🔆', '🔆ویرایش پروژه🔆')
    markup.add('🔆حذف پروژه🔆', '🔆دریافت فایل مود🔆')
    msg = bot.reply_to(message, '🔥لطفا انتخاب كنيد🔥', reply_markup=markup)
    if msg.message_id == message_id + 1:
        bot.register_next_step_handler(msg, process_first_step)


def selectname(message):
    user_id = message.chat.id
    loads = modedatabase.load_pj(user_id)
    markup = build_mark(loads)
    markup.add('🔹بازگشت🔹')
    msg = bot.reply_to(message, '❕پروژه مورد نظر خود را انتخاب کنید❕', reply_markup=markup)
    bot.register_next_step_handler(msg, sendfile)


def selectfile(message):
    user_id = message.chat.id
    loads = modedatabase.load_pj(user_id)
    markup = build_mark(loads)
    markup.add('🔹بازگشت🔹')
    msg = bot.reply_to(message, '❕پروژه مورد نظر خود را انتخاب کنید❕', reply_markup=markup)
    bot.register_next_step_handler(msg, removepj)


def sendfile(message):
    user_id=message.chat.id
    name=message.text
    if name == '🔹بازگشت🔹':
        start(message)
    elif name == '/start':
        start(message)
    else:
        try:
            with open(f'{user_id}-{name}.xml') as file:
                bot.send_document(user_id, file)
                start(message)
        except:
            bot.send_message(user_id, '❕لطفا از دكمه هاي موجود استفاده كنيد❕')
            selectname(message)


def load_projects(message):
    user_id = message.chat.id
    loads = modedatabase.load_pj(user_id)
    markup = build_mark(loads)
    markup.add('🔹بازگشت🔹')
    msg = bot.reply_to(message, '❕پروژه مورد نظر خود را انتخاب کنید❕', reply_markup=markup)
    bot.register_next_step_handler(msg, load_roles)


def load_rols(message,name):
    load = modedatabase.load_types()
    load.remove('')
    markup = build_mark(load)
    markup.add('🔹بازگشت🔹','تغییر اسم مود')
    msg = bot.reply_to(message, '⚜️انتخاب کنید⚜️', reply_markup=markup)
    bot.register_next_step_handler(msg, load_text, name)


def load_roles(message):
    name = message.text
    user_id = message.chat.id
    load = modedatabase.load_pj(user_id)
    if name == '🔹بازگشت🔹':
        start(message)
    elif name == '/start':
        start(message)
    elif name not in load:
        bot.send_message(user_id,'❕لطفا از دکمه های موجود استفاده کنید❕')
        load_projects(message)
    else:
        load_rols(message,name)


def load_text(message,name):
    info = message.text
    user_id = message.chat.id
    load = modedatabase.load_types()
    if info == '🔹بازگشت🔹':
        load_projects(message)
    elif info == '/start':
        start(message)
    elif info == 'تغییر اسم مود':
        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
            markup.add('↪️برگشت↪️')
            msg = bot.reply_to(message, '❕اسم جدید مود خود را وارد کنید❕', reply_markup=markup)
            bot.register_next_step_handler(msg, changename, name)
        except:
            bot.send_message(user_id,'error❕')
            start(message)
    elif info not in load:
        bot.send_message(user_id,'❕لطفا از دکمه های موجود استفاده کنید❕')
        load_projects(message)
    else:
        user_id = message.chat.id
        load = modedatabase.load_text(info)
        markup = build_mark(load)
        markup.add('↩️برگشت↩️')
        msg = bot.reply_to(message, '⚜️انتخاب کنید⚜️', reply_markup=markup)
        bot.register_next_step_handler(msg, load_user_text, name)


def changename(message,name):
    user_id = message.chat.id
    newname = message.text
    if newname == '↪️برگشت↪️':
        load_rols(message, name)
    elif newname == '/start':
        start(message)
    else:
        modedatabase.changename(user_id, name, newname)
        tree = ET.parse(f'{user_id}-{name}.xml')
        root = tree.getroot()
        tree.write(f'{user_id}-{newname}.xml')
        os.remove(f'{user_id}-{name}.xml')
        bot.send_message(user_id, '⚜️اسم مود با موفقیت تعویض شد⚜️')
        load_projects(message)


def load_user_text(message,name):
    try:
        info = message.text
        user_id = message.chat.id
        if info == '↩️برگشت↩️':
            load_rols(message,name)
        elif info == '/start':
            start(message)
        else:
            text_ids = info.split(':')
            text_id = text_ids[0]
            main_text = text_ids[1]
            user_id = message.chat.id
            id = modedatabase.load_text_id(info)
            load = modedatabase.load_user_text(id, user_id, name)
            if load is None:
                bot.send_message(user_id, '🔅متن فعلی شما🔅\n' + info)
                text = main_text
            else:
                bot.send_message(user_id, '🔅متن فعلی شما🔅\n' + load[0])
                text = load[0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=2)
            markup.add('🔸بازگشت🔸')
            msg = bot.reply_to(message, '❕متن خود را وارد کنید❕',reply_markup = markup)
            bot.register_next_step_handler(msg, edit, name, text_id, text)
    except:
        bot.send_message(user_id,'❕لطفا از دکمه های موجود استفاده کنید❕')
        load_user_text(message,name)


def edit(message,name,id,main):
    text = message.text
    if text == '🔸بازگشت🔸':
        load_rols(message,name)
    elif text == '/start':
        start(message)
    else:
        user_id = message.chat.id
        id = int(id)
        modedatabase.update_text(text, name, id, user_id)
        change(main, text, user_id, name)
        bot.send_message(user_id, '⚜️با موفقیت ویرایش شد⚜️')
        load_rols(message,name)


def change(text,change,user_id,name):
    tree = ET.parse(f'{user_id}-{name}.xml')
    root = tree.getroot()
    for elem in root:
        for subelem in elem:
            if text == subelem.text:
                subelem.text = subelem.text.replace(text, change)
    tree.write(f'{user_id}-{name}.xml')


def build_xml(user_id,name):
    tree = ET.parse('Persian Normal.xml')
    root = tree.getroot()
    tree.write(f'{user_id}-{name}.xml')


@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def poll():
    if __name__ == "__main__":
        try:
            bot.enable_save_next_step_handlers(delay=2)

            bot.load_next_step_handlers()

            bot.polling(none_stop=True,timeout=123)
        except Exception as e:
            bot.send_message(chat_id=, text=e)
            raise e


poll()

while True:
    pass
