from classes import User, Unit, Flow
import config
import telebot
from telebot import types
import os


def load_data(file_data, file_users):
    flow = Flow()
    bd = open(file_data, 'r')
    data = bd.readlines()
    for l in data:
        s = l.split(' ')
        img = s[5:]
        if len(l) >= 5:
            flow.add_unit(Unit(int(s[0]), s[1], s[2], int(s[3]), float(s[4]), img))
    bd.close()
    f = open(file_users, 'r')
    line = f.readlines()
    for l in line:
        s = l.split(' ')
        flow.add_user(User(int(s[1]), s[0], False, False))
    f.close()
    return flow


def save_data(file, flow):
    bd = open(file, 'w')
    lines = str()
    for unit in flow.find_all():
        s = f'{unit.get_id()} {unit.get_type()} {unit.get_name()} {unit.get_number()} {unit.get_status()}'
        for img in unit.get_images():
            s = s + ' ' + img
        lines = lines + s + '\n'
    bd.write(lines[0:-1])
    bd.close()


STATUS_LIST = {'ecn': {0: 'комплектация',
                       1: 'скомплектован',
                       2: 'сборка',
                       3: 'собран',
                       4: 'испытание',
                       5: 'испытан'},
               'ped': {1: 'Комплектация',
                       2: 'Сборка',
                       3: 'Испытание'}}
CHANGE_LIST = {'ecn': {0: 'Завершить компектацию',
                       1: 'Начать сборку',
                       2: 'сборка',
                       2.1: 'Проверка теплового зазора',
                       2.2: 'Проверка вылетов вала',
                       3: 'Начать испытание',
                       4: 'Завершить испытание',
                       5: 'испытан'}}
bot = telebot.TeleBot(config.token)
upload = False
new = False
id_upload = int()
fl = load_data('bd.txt', 'users.txt')


# fl = Flow()
# fl.add_unit(Unit(1, 'ecn', 'ВНН5-25-700/03-023', 190345610, 0,
#             ['AgACAgIAAxkBAAIB0GDYXrKc9D85pfAdp8rNvfWvPF_fAAJntTEbV1vASjokvvNorOVqAQADAgADbQADIAQ',
#              'AgACAgIAAxkBAAIB4GDYYT7pz3xj6-xhFEt1xTl1W9eiAAJrtTEbV1vASr1qHI4AAWC6WwEAAwIAA20AAyAE',
#              'AgACAgIAAxkBAAIB7WDYY3BWMUgwdLMPvvcMgc141MccAAJBtjEbQUHBSh56GLB05C2kAQADAgADbQADIAQ',
#              'AgACAgIAAxkBAAIBnmDYWP2wiT6iGvbxZF5Yv0BpFLZWAAIlszEb2pPBSvfZNQHX2R5QAQADAgADbQADIAQ'
#              ]))
# fl.add_unit(Unit(2, 'ecn', 'ВНН5-25-800/03-023', 190345611, 0, list()))
# fl.add_unit(Unit(5, 'ped', 'ПЭДН63-117-1100/071', 185245215, 0, list()))
# fl.add_unit(Unit(5, 'ped', 'ПЭДН45-117-900/071', 200245151, 0, list()))
# fl.add_unit(Unit(6, 'gz', 'ГЗНМ-92/030', 190254654, 0, list()))
# save_data(file, fl)

@bot.message_handler(commands=['start'])
def start(message):
    start_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start_key = types.KeyboardButton('Главное меню')
    start_key.add(button_start_key)
    bot.send_message(message.from_user.id, 'Для начала работы войдите в главное меню', reply_markup=start_key)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global upload
    global fl
    global id_upload
    global new
    global file
    global STATUS_LIST
    global CHANGE_LIST
    # print(call.from_user.first_name + ' ' + str(call.from_user.id))
    if fl.find_user(call.from_user.id) is not None:
        pass
    data = call.data.split('.')
    print(data)

    # Главное Меню
    if call.data == 'main':
        upload = False
        new = False
        key = types.InlineKeyboardMarkup(row_width=1)
        butt1 = types.InlineKeyboardButton('Операционный контроль', callback_data=f'oper_list')
        butt2 = types.InlineKeyboardButton('Статус ремонта', callback_data='status_all')
        butt3 = types.InlineKeyboardButton('История ремонта', callback_data='history')
        key.add(butt1, butt2, butt3)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Главное меню',
                              reply_markup=key)

    # Операционный контроль
    elif data[0] == 'oper_list':
        upload = False
        new = False
        key = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            if int(unit.get_status()) in STATUS_LIST[unit.get_type()] \
                    and STATUS_LIST[unit.get_type()][int(unit.get_status())] != 'испытан':
                key.add(
                    types.InlineKeyboardButton(
                        f'{unit.get_name()} '
                        f'{unit.get_number()} '
                        f'{STATUS_LIST[unit.get_type()][int(unit.get_status())]}',
                        callback_data=f'oper_change.{unit.get_id()}')
                )
        butt_add = types.InlineKeyboardButton('Новая сборка',
                                              callback_data='new')
        butt_dell = types.InlineKeyboardButton('Убрать узел со сбоки',
                                               callback_data='list_dell')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main')
        key.add(butt_add, butt_dell, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите узел:',
                              reply_markup=key)
    elif data[0] == 'oper_change':
        upload = False
        new = False
        key = types.InlineKeyboardMarkup(row_width=1)
        unit = fl.find_by_id(int(data[1]))
        status = unit.get_status()
        if int(status) == 2:
            if status == 2:
                unit.set_status(2.1)
            if unit.get_status() in CHANGE_LIST[unit.get_type()]:
                key.add(types.InlineKeyboardButton(
                    f'{CHANGE_LIST[unit.get_type()][unit.get_status()]}',
                    callback_data=f'change.{unit.get_id()}'))
            else:
                key.add(types.InlineKeyboardButton(
                    f'Завершить сборку',
                    callback_data=f'change.{unit.get_id()}'))
        else:
            key.add(types.InlineKeyboardButton(
                f'{CHANGE_LIST[unit.get_type()][unit.get_status()]}',
                callback_data=f'change.{unit.get_id()}'))
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='oper_list')
        key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'{unit}',
                              reply_markup=key)
    elif data[0] == 'change':
        upload = False
        new = False
        key = types.InlineKeyboardMarkup(row_width=1)
        unit = fl.find_by_id(int(data[1]))
        if int(unit.get_status()) == 2 and unit.get_status() in CHANGE_LIST[unit.get_type()]:
            key.add(types.InlineKeyboardButton(
                f'Загрузить фотоотчет',
                callback_data=f'upload.{unit.get_id()}'))
            key.add(types.InlineKeyboardButton(
                f'Завершить операцию',
                callback_data=f'end.{unit.get_id()}'))
        else:
            unit.set_status(int(unit.get_status() + 1))
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data=f'oper_list.{unit.get_id()}')
        key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Статус изменен',
                              reply_markup=key)
    elif data[0] == 'upload':
        upload = True
        new = False
        id_upload = int(data[1])
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        butt_start = types.KeyboardButton('Главное меню')
        key.add(butt_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=key)
    elif data[0] == 'end':
        upload = False
        new = False
        unit = fl.find_by_id(int(data[1]))
        unit.set_status(unit.get_status() + 0.1)
        key = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data=f'oper_list.{unit.get_id()}')
        key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Статус изменен',
                              reply_markup=key)
    # Новая сборка
    elif call.data == 'new':
        new = True
        upload = False
        bot.send_message(chat_id=call.message.chat.id,
                         text='Введите наименование и номер узла без знака "№", например ВНН5-25-700/03-043 190260321 После ввода вернитесь в Главное меню')


    # Список для удаления
    elif call.data == 'list_dell':
        upload = False
        new = False
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            keyboard.add(
                types.InlineKeyboardButton(f'{unit.get_name()} {unit.get_number()}',
                                           callback_data=f'del.{unit.get_id()}')
            )
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        keyboard.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вуберите узел для удаления:',
                              reply_markup=keyboard)
    # Удаление узла
    elif data[0] == 'del':
        upload = False
        new = False
        rsl = fl.delete(int(data[1]))
        save_data('bd.txt', fl)
        gs_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='list_dell')
        gs_main_key.add(butt_back)
        if rsl:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Узел удален',
                                  reply_markup=gs_main_key)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Не удалось удалить узел',
                                  reply_markup=gs_main_key)

    # Статус ремонта
    elif call.data == 'status_all':
        upload = False
        new = False
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            keyboard.add(
                types.InlineKeyboardButton(
                    f'{unit.get_name()} '
                    f'{unit.get_number()} '
                    f'{STATUS_LIST[unit.get_type()][int(unit.get_status())]}',
                    callback_data=f'show.{unit.get_id()}')
            )
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main')
        keyboard.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите узел:',
                              reply_markup=keyboard)

    # Выгрузка фотографий узла
    elif data[0] == 'show':
        upload = False
        new = False
        unit = fl.find_by_id(int(data[1]))
        for img in unit.get_images():
            file = open(f'photos/{img}.jpg', 'rb')
            bot.send_photo(call.message.chat.id, file)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='status_all')
        keyboard.add(butt_back)
        bot.send_message(chat_id=call.message.chat.id,
                         text=
                         f'Загружены фото контроля сбоки {unit}',
                         reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global upload
    global new
    global fl
    global file
    upload = False

    # Добавление нового узла
    if new:
        new_unit = message.text.split(' ')
        if new_unit[0][0:3] == 'ЭЦН' or new_unit[0][0:3] == 'ВНН':
            fl.add_unit(Unit(1, 'ecn', new_unit[0], int(new_unit[1]), 0, list()))
            bot.send_message(chat_id=message.chat.id,
                             text=f'{new_unit[0]} {new_unit[1]} поставлен на сборку')
        elif new_unit[0][0:3] == 'ПЭД' or new_unit[0][0:3] == 'ПВЭ':
            fl.add_unit(Unit(1, 'ped', new_unit[0], int(new_unit[1]), 0, list()))
            bot.send_message(chat_id=message.chat.id,
                             text=f'{new_unit[0]} {new_unit[1]} поставлен на сборку')
        elif new_unit[0][0:2] == 'ГЗ':
            fl.add_unit(Unit(1, 'gz', new_unit[0], int(new_unit[1]), 0, list()))
            bot.send_message(chat_id=message.chat.id,
                             text=f'{new_unit[0]} {new_unit[1]} поставлен на сборку')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Неудалось добавить узел')
    print('Пользователь ' + message.from_user.first_name + ' сообщение ' + message.text)
    if message.text == 'ID':
        bot.send_message(message.from_user.id, f'Your ID: {message.from_user.id}')
    elif message.text == 'Name':
        bot.send_message(message.from_user.id, f'Your ID: {message.from_user.first_name}')
    elif message.text == 'Главное меню':
        save_data('bd.txt', fl)
        upload = False
        new = False
        key = types.InlineKeyboardMarkup(row_width=1)
        butt1 = types.InlineKeyboardButton('Операционный контроль', callback_data='oper_list')
        butt2 = types.InlineKeyboardButton('Статус ремонта', callback_data='status_all')
        butt3 = types.InlineKeyboardButton('История ремонта', callback_data='history')
        key.add(butt1, butt2, butt3)
        bot.send_message(message.from_user.id, 'Главное меню', reply_markup=key)


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    global fl
    global upload
    global id_upload
    global new
    new = False
    if upload:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        filename, file_extension = os.path.splitext(file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'photos/' + message.photo[1].file_id + file_extension
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")
        fl.find_by_id(id_upload).add_image(message.photo[1].file_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
