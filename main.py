import telebot
from telebot import types
import config
import os


class Unit:
    def __init__(self, id, type, name, number, status, images):
        self.__id = id
        self.__name = name
        self.__number = number
        self.__status = status
        self.__type = type
        self.__images = images

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_number(self):
        return self.__number

    def set_number(self, number):
        self.__number = number

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_images(self):
        return self.__images

    def set_images(self, images):
        self.__images = images

    def add_image(self, image):
        self.__images.append(image)

    def __str__(self) -> str:
        return f'{self.__name} №{self.__number}'


class Flow:
    __units = list()
    __ids = 1

    def add(self, unit):
        unit.set_id(self.__ids)
        self.__units.append(unit)
        self.__ids += 1

    def index_of(self, id):
        rsl = -1
        for i in range(len(self.__units)):
            if self.__units[i].get_id() == id:
                rsl = i
                break
        return rsl

    def find_by_id(self, id):
        index = self.index_of(id)
        return self.__units[index] if index != -1 else None

    def find_all(self):
        return self.__units

    def delete(self, id):
        index = self.index_of(id)
        rsl = index != -1
        if rsl:
            self.__units.pop(index)
        return rsl


def load_data(file):
    flow = Flow()
    bd = open(file, 'r')
    data = bd.readlines()
    for l in data:
        s = l.split(' ')
        img = s[5:]
        if len(l) >= 5:
            flow.add(Unit(int(s[0]), s[1], s[2], int(s[3]), int(s[4]), img))
    bd.close()
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


bot = telebot.TeleBot(config.token)
upload = False
new = False
id_upload = int()
file = 'bd.txt'
fl = load_data(file)

# fl = Flow()
# fl.add(Unit(1, 'ecn', 'ВНН5-25-700/03-023', 190345610, 0,
#             ['AgACAgIAAxkBAAIB0GDYXrKc9D85pfAdp8rNvfWvPF_fAAJntTEbV1vASjokvvNorOVqAQADAgADbQADIAQ',
#              'AgACAgIAAxkBAAIB4GDYYT7pz3xj6-xhFEt1xTl1W9eiAAJrtTEbV1vASr1qHI4AAWC6WwEAAwIAA20AAyAE',
#              'AgACAgIAAxkBAAIB7WDYY3BWMUgwdLMPvvcMgc141MccAAJBtjEbQUHBSh56GLB05C2kAQADAgADbQADIAQ',
#              'AgACAgIAAxkBAAIBnmDYWP2wiT6iGvbxZF5Yv0BpFLZWAAIlszEb2pPBSvfZNQHX2R5QAQADAgADbQADIAQ'
#              ]))
# fl.add(Unit(2, 'ecn', 'ВНН5-25-800/03-023', 190345611, 0, list()))
# fl.add(Unit(5, 'ped', 'ПЭДН63-117-1100/071', 185245215, 0, list()))
# fl.add(Unit(5, 'ped', 'ПЭДН45-117-900/071', 200245151, 0, list()))
# fl.add(Unit(6, 'gz', 'ГЗНМ-92/030', 190254654, 0, list()))
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
    data = call.data.split('.')
    # Главное Меню
    if call.data == 'main_menu':
        upload = False
        new = False
        main_key = types.InlineKeyboardMarkup()
        butt_ecn = types.InlineKeyboardButton('ЭЦН', callback_data='list_ecn')
        butt_ped = types.InlineKeyboardButton('ПЭД', callback_data='list_ped')
        butt_gz = types.InlineKeyboardButton('Гидрозащита', callback_data='list_gz')
        butt_gs = types.InlineKeyboardButton('ГС/ГД/МВ', callback_data='main_gs')
        butt_kl = types.InlineKeyboardButton('Каб. линия', callback_data='main_kl')
        butt_dop = types.InlineKeyboardButton('Доп. оборудование', callback_data='main_dop')
        butt_all = types.InlineKeyboardButton('Просмотр статуса сборки', callback_data='list_all')
        main_key.add(butt_ecn, butt_ped, butt_gz, butt_gs, butt_kl, butt_dop, butt_all)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите узел:',
                              reply_markup=main_key)
    # Список всех узлов на сборке
    elif call.data == 'list_all':
        upload = False
        new = False
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            keyboard.add(
                types.InlineKeyboardButton(f'{unit.get_name()} {unit.get_number()}',
                                           callback_data=f'show.{unit.get_id()}')
            )
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        butt_dell = types.InlineKeyboardButton('Убрать со сбоки узел',
                                               callback_data='list_dell')
        keyboard.add(butt_dell, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите узел:',
                              reply_markup=keyboard)
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
                                               callback_data='list_all')
        keyboard.add(butt_back)
        bot.send_message(chat_id=call.message.chat.id,
                         text=
                         f'Загружены фото контроля сбоки {unit}',
                         reply_markup=keyboard)

    # Список ЭЦН на сборке
    elif call.data == 'list_ecn':
        upload = False
        new = False
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            if unit.get_type() == 'ecn':
                keyboard.add(
                    types.InlineKeyboardButton(f'{unit.get_name()} {unit.get_number()}',
                                               callback_data=f'main_ecn.{unit.get_id()}')
                )
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        butt_new = types.InlineKeyboardButton('Новая сборка',
                                              callback_data='new')
        keyboard.add(butt_new, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите секцию:',
                              reply_markup=keyboard)
    # Верхнее меню ЭЦН
    elif data[0] == 'main_ecn':
        new = False
        upload = False
        ecn_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_1 = types.InlineKeyboardButton('1. Визуальный контроль состояния деталей',
                                            callback_data=f'ecn_sub1.{data[1]}')
        butt_2 = types.InlineKeyboardButton('2. Контроль состояния вала',
                                            callback_data=f'ecn_sub2.{data[1]}')
        butt_3 = types.InlineKeyboardButton('3. Контроль момента проворачивания вала',
                                            callback_data=f'ecn_sub3.{data[1]}')
        butt_4 = types.InlineKeyboardButton('4. Контроль вылетов вала',
                                            callback_data=f'ecn_sub4.{data[1]}')
        butt_5 = types.InlineKeyboardButton('5. Контроль радиального и торцевого биений',
                                            callback_data=f'ecn_sub5.{data[1]}')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='list_ecn')
        ecn_main_key.add(butt_1, butt_2, butt_3, butt_4, butt_5, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Контроль {fl.find_by_id(int(data[1]))}',
                              reply_markup=ecn_main_key)
    # Меню ЭЦН 1. Визуальный контроль состояния деталей
    elif data[0] == 'ecn_sub1':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 2. Контроль состояния вала
    elif data[0] == 'ecn_sub2':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 3. Контроль момента проворачивания вала
    elif data[0] == 'ecn_sub3':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 4. Контроль вылетов вала
    elif data[0] == 'ecn_sub4':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 5. Контроль радиального и торцевого биений
    elif data[0] == 'ecn_sub5':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)

    # Список ПЭД на сборке
    elif call.data == 'list_ped':
        upload = False
        new = False
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            if unit.get_type() == 'ped':
                keyboard.add(
                    types.InlineKeyboardButton(f'{unit.get_name()} {unit.get_number()}',
                                               callback_data=f'main_ped.{unit.get_id()}')
                )
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        butt_new = types.InlineKeyboardButton('Новая сборка',
                                              callback_data='new')
        keyboard.add(butt_new, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите секцию:',
                              reply_markup=keyboard)
    # Верхнее меню ПЭД
    elif data[0] == 'main_ped':
        upload = False
        new = False
        ped_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_1 = types.InlineKeyboardButton('1. Контроль качества мойки и правки вала',
                                            callback_data=f'ped_sub1.{data[1]}')
        butt_2 = types.InlineKeyboardButton('2. Проверка наружней поверхности статора',
                                            callback_data=f'ped_sub2.{data[1]}')
        butt_3 = types.InlineKeyboardButton('3. Контроль момента проворачивания вала',
                                            callback_data=f'ped_sub3.{data[1]}')
        butt_4 = types.InlineKeyboardButton('4. Проверка теплового зазора',
                                            callback_data=f'ped_sub4.{data[1]}')
        butt_5 = types.InlineKeyboardButton('5. Контроль состояния нулевого провода',
                                            callback_data=f'ped_sub5.{data[1]}')
        butt_6 = types.InlineKeyboardButton('6. Фактическое сопротивление изоляции',
                                            callback_data=f'ped_sub6.{data[1]}')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='list_ped')
        ped_main_key.add(butt_1, butt_2, butt_3, butt_4, butt_5, butt_6, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Контроль {fl.find_by_id(int(data[1]))}',
                              reply_markup=ped_main_key)
    # Меню ПЭД 1. Контроль качества мойки и правки вала
    elif data[0] == 'ped_sub1':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 2. Проверка наружней поверхности статора
    elif data[0] == 'ped_sub2':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 3. Контроль момента проворачивания вала
    elif data[0] == 'ped_sub3':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 4. Проверка теплового зазора
    elif data[0] == 'ped_sub4':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 5. Контроль состояния нулевого провода
    elif data[0] == 'ped_sub5':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 6. Фактическое сопротивление изоляции
    elif data[0] == 'ped_sub6':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)

    # Список ГЗ на сборке
    elif call.data == 'list_gz':
        upload = False
        new = False
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for unit in fl.find_all():
            if unit.get_type() == 'gz':
                keyboard.add(
                    types.InlineKeyboardButton(f'{unit.get_name()} {unit.get_number()}',
                                               callback_data=f'main_gz.{unit.get_id()}')
                )
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        butt_new = types.InlineKeyboardButton('Новая сборка',
                                              callback_data='new')
        keyboard.add(butt_new, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите секцию:',
                              reply_markup=keyboard)
    # Верхнее меню ГЗ
    elif data[0] == 'main_gz':
        upload = False
        new = False
        gz_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_1 = types.InlineKeyboardButton('1. Контроль вала и теплового зазора',
                                            callback_data=f'gz_sub1.{data[1]}')
        butt_2 = types.InlineKeyboardButton('2. Опресовка торцевого уплотнения',
                                            callback_data=f'gz_sub2.{data[1]}')
        butt_3 = types.InlineKeyboardButton('3. Опресовка клапанов',
                                            callback_data=f'gz_sub3.{data[1]}')
        butt_4 = types.InlineKeyboardButton('4. Контроль момента вращения вала',
                                            callback_data=f'gz_sub4.{data[1]}')
        butt_5 = types.InlineKeyboardButton('5. Контроль заглубления и вылетов',
                                            callback_data=f'gz_sub5.{data[1]}')
        butt_6 = types.InlineKeyboardButton('6. Контроль радиального и торцевого биений',
                                            callback_data=f'gz_sub6.{data[1]}')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='list_gz')
        gz_main_key.add(butt_1, butt_2, butt_3, butt_4, butt_5, butt_6, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'Контроль {fl.find_by_id(int(data[1]))}',
                              reply_markup=gz_main_key)
    # Меню ГЗ 1. Контроль вала и теплового зазора
    elif data[0] == 'gz_sub1':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 2. Опресовка торцевого уплотнения
    elif data[0] == 'gz_sub2':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 3. Опресовка клапанов
    elif data[0] == 'gz_sub3':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 4. Контроль момента вращения вала
    elif data[0] == 'gz_sub4':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 5. Контроль заглубления и вылетов
    elif data[0] == 'gz_sub5':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 6. Контроль радиального и торцевого биений
    elif data[0] == 'gz_sub6':
        upload = True
        new = False
        id_upload = int(data[1])
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)

    # Верхнее меню Приемного устройства
    elif call.data == 'main_gs':
        upload = False
        new = False
        gs_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        gs_main_key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Раздел в разработке',
                              reply_markup=gs_main_key)
    # Верхнее меню Кабельных линий
    elif call.data == 'main_kl':
        upload = False
        new = False
        kl_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        kl_main_key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Раздел в разработке',
                              reply_markup=kl_main_key)
    # Верхнее меню Доп оборудования
    elif call.data == 'main_dop':
        upload = False
        new = False
        dop_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        dop_main_key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Раздел в разработке',
                              reply_markup=dop_main_key)

    # Новая сборка
    elif call.data == 'new':
        new = True
        upload = False
        bot.send_message(chat_id=call.message.chat.id,
                         text='Введите наименование и номер узла без знака "№", например ВНН5-25-700/03-043 190260321 После ввода вернитесь в Главное меню')


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
            fl.add(Unit(1, 'ecn', new_unit[0], int(new_unit[1]), 0, list()))
            bot.send_message(chat_id=message.chat.id,
                             text=f'{new_unit[0]} {new_unit[1]} поставлен на сборку')
        elif new_unit[0][0:3] == 'ПЭД' or new_unit[0][0:3] == 'ПВЭ':
            fl.add(Unit(1, 'ped', new_unit[0], int(new_unit[1]), 0, list()))
            bot.send_message(chat_id=message.chat.id,
                             text=f'{new_unit[0]} {new_unit[1]} поставлен на сборку')
        elif new_unit[0][0:2] == 'ГЗ':
            fl.add(Unit(1, 'gz', new_unit[0], int(new_unit[1]), 0, list()))
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
        main_key = types.InlineKeyboardMarkup()
        butt_ecn = types.InlineKeyboardButton('ЭЦН', callback_data='list_ecn')
        butt_ped = types.InlineKeyboardButton('ПЭД', callback_data='list_ped')
        butt_gz = types.InlineKeyboardButton('Гидрозащита', callback_data='list_gz')
        butt_gs = types.InlineKeyboardButton('ГС/ГД/МВ', callback_data='main_gs')
        butt_kl = types.InlineKeyboardButton('Каб. линия', callback_data='main_kl')
        butt_dop = types.InlineKeyboardButton('Доп. оборудование', callback_data='main_dop')
        butt_all = types.InlineKeyboardButton('Просмотр статуса сборки', callback_data='list_all')
        main_key.add(butt_ecn, butt_ped, butt_gz, butt_gs, butt_kl, butt_dop, butt_all)
        bot.send_message(message.from_user.id, 'Выберите узел:', reply_markup=main_key)


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
