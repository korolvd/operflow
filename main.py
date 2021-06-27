import telebot
from telebot import types
import config
import os

bot = telebot.TeleBot(config.token)
upload = False


@bot.message_handler(commands=['start'])
def start(message):
    start_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start_key = types.KeyboardButton('Главное меню')
    start_key.add(button_start_key)
    bot.send_message(message.from_user.id, 'Для начала работы войдите в главное меню', reply_markup=start_key)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global upload
    # Главное Меню
    if call.data == 'main_menu':
        upload = False
        main_key = types.InlineKeyboardMarkup()
        butt_ecn = types.InlineKeyboardButton('ЭЦН', callback_data='main_ecn')
        butt_ped = types.InlineKeyboardButton('ПЭД', callback_data='main_ped')
        butt_gz = types.InlineKeyboardButton('Гидрозащита', callback_data='main_gz')
        butt_gs = types.InlineKeyboardButton('ГС/ГД/МВ', callback_data='main_gs')
        butt_kl = types.InlineKeyboardButton('Каб. линия', callback_data='main_kl')
        butt_dop = types.InlineKeyboardButton('Доп. оборудование', callback_data='main_dop')
        main_key.add(butt_ecn, butt_ped, butt_gz, butt_gs, butt_kl, butt_dop)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Выберите узел:',
                              reply_markup=main_key)
    # Верхнее меню ЭЦН
    elif call.data == 'main_ecn':
        upload = False
        ecn_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_1 = types.InlineKeyboardButton('1. Визуальный контроль состояния деталей',
                                            callback_data='ecn_sub1')
        butt_2 = types.InlineKeyboardButton('2. Контроль состояния вала',
                                            callback_data='ecn_sub2')
        butt_3 = types.InlineKeyboardButton('3. Контроль момента проворачивания вала',
                                            callback_data='ecn_sub3')
        butt_4 = types.InlineKeyboardButton('4. Контроль вылетов вала',
                                            callback_data='ecn_sub4')
        butt_5 = types.InlineKeyboardButton('5. Контроль радиального и торцевого биений',
                                            callback_data='ecn_sub5')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        ecn_main_key.add(butt_1, butt_2, butt_3, butt_4, butt_5, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Контроль ЭЦН',
                              reply_markup=ecn_main_key)
    # Меню ЭЦН 1. Визуальный контроль состояния деталей
    elif call.data == 'ecn_sub1':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 2. Контроль состояния вала
    elif call.data == 'ecn_sub2':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 3. Контроль момента проворачивания вала
    elif call.data == 'ecn_sub3':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 4. Контроль вылетов вала
    elif call.data == 'ecn_sub4':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ЭЦН 5. Контроль радиального и торцевого биений
    elif call.data == 'ecn_sub5':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Верхнее меню ПЭД
    elif call.data == 'main_ped':
        upload = False
        ped_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_1 = types.InlineKeyboardButton('1. Контроль качества мойки и правки вала',
                                            callback_data='ped_sub1')
        butt_2 = types.InlineKeyboardButton('2. Проверка наружней поверхности статора',
                                            callback_data='ped_sub2')
        butt_3 = types.InlineKeyboardButton('3. Контроль момента проворачивания вала',
                                            callback_data='ped_sub3')
        butt_4 = types.InlineKeyboardButton('4. Проверка теплового зазора',
                                            callback_data='ped_sub4')
        butt_5 = types.InlineKeyboardButton('5. Контроль состояния нулевого провода',
                                            callback_data='ped_sub5')
        butt_6 = types.InlineKeyboardButton('6. Фактическое сопротивление изоляции',
                                            callback_data='ped_sub6')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        ped_main_key.add(butt_1, butt_2, butt_3, butt_4, butt_5, butt_6, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Контроль ПЭД',
                              reply_markup=ped_main_key)
    # Меню ПЭД 1. Контроль качества мойки и правки вала
    elif call.data == 'ped_sub1':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 2. Проверка наружней поверхности статора
    elif call.data == 'ped_sub2':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 3. Контроль момента проворачивания вала
    elif call.data == 'ped_sub3':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 4. Проверка теплового зазора
    elif call.data == 'ped_sub4':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 5. Контроль состояния нулевого провода
    elif call.data == 'ped_sub5':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ПЭД 6. Фактическое сопротивление изоляции
    elif call.data == 'ped_sub6':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)

    # Верхнее меню ГЗ
    elif call.data == 'main_gz':
        upload = False
        gz_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_1 = types.InlineKeyboardButton('1. Контроль вала и теплового зазора',
                                            callback_data='gz_sub1')
        butt_2 = types.InlineKeyboardButton('2. Опресовка торцевого уплотнения',
                                            callback_data='gz_sub2')
        butt_3 = types.InlineKeyboardButton('3. Опресовка клапанов',
                                            callback_data='gz_sub3')
        butt_4 = types.InlineKeyboardButton('4. Контроль момента вращения вала',
                                            callback_data='gz_sub4')
        butt_5 = types.InlineKeyboardButton('5. Контроль заглубления и вылетов',
                                            callback_data='gz_sub5')
        butt_6 = types.InlineKeyboardButton('6. Контроль радиального и торцевого биений',
                                            callback_data='gz_sub6')
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        gz_main_key.add(butt_1, butt_2, butt_3, butt_4, butt_5, butt_6, butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Контроль Гидрозащиты',
                              reply_markup=gz_main_key)
    # Меню ГЗ 1. Контроль вала и теплового зазора
    elif call.data == 'gz_sub1':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 2. Опресовка торцевого уплотнения
    elif call.data == 'gz_sub2':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 3. Опресовка клапанов
    elif call.data == 'gz_sub3':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 4. Контроль момента вращения вала
    elif call.data == 'gz_sub4':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 5. Контроль заглубления и вылетов
    elif call.data == 'gz_sub5':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)
    # Меню ГЗ 6. Контроль радиального и торцевого биений
    elif call.data == 'gz_sub6':
        upload = True
        ecn_sub1_key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton('Главное меню')
        ecn_sub1_key.add(button_start)
        bot.send_message(call.message.chat.id,
                         'Загрузите фото проверки. После завершения вернитесь в Главное меню',
                         reply_markup=ecn_sub1_key)

    # Верхнее меню Приемного устройства
    elif call.data == 'main_gs':
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
        dop_main_key = types.InlineKeyboardMarkup(row_width=1)
        butt_back = types.InlineKeyboardButton('<- Назад',
                                               callback_data='main_menu')
        dop_main_key.add(butt_back)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Раздел в разработке',
                              reply_markup=dop_main_key)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global upload
    upload = False
    print('Пользователь ' + message.from_user.first_name + ' сообщение ' + message.text)
    if message.text == 'photo':
        file = open('f1.jpg', 'rb')
        bot.send_photo(message.from_user.id, file)
    elif message.text == 'up':
        upload = True
    elif message.text == 'ID':
        bot.send_message(message.from_user.id, f'Your ID: {message.from_user.id}')
    elif message.text == 'Name':
        bot.send_message(message.from_user.id, f'Your ID: {message.from_user.first_name}')
    elif message.text == 'Главное меню' or message.text == 'Завершить':
        main_key = types.InlineKeyboardMarkup()
        butt_ecn = types.InlineKeyboardButton('ЭЦН', callback_data='main_ecn')
        butt_ped = types.InlineKeyboardButton('ПЭД', callback_data='main_ped')
        butt_gz = types.InlineKeyboardButton('Гидрозащита', callback_data='butt_gz')
        butt_gs = types.InlineKeyboardButton('ГС/ГД/МВ', callback_data='main_gs')
        butt_kl = types.InlineKeyboardButton('Каб. линия', callback_data='main_kl')
        butt_dop = types.InlineKeyboardButton('Доп. оборудование', callback_data='main_dop')
        main_key.add(butt_ecn, butt_ped, butt_gz, butt_gs, butt_kl, butt_dop)
        bot.send_message(message.from_user.id, 'Выберите узел:', reply_markup=main_key)
    # else:
    #     bot.send_message(message.from_user.id, message.content_type)


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    global upload
    if upload:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        filename, file_extension = os.path.splitext(file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'photos/' + message.photo[1].file_id + file_extension
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")
        # file = open(src, 'rb')


if __name__ == '__main__':
    bot.polling(none_stop=True)

# @bot.message_handler(content_types=["text"])
# def any_msg(message):
#     keyboardmain = types.InlineKeyboardMarkup(row_width=2)
#     first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
#     second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
#     keyboardmain.add(first_button, second_button)
#     bot.send_message(message.chat.id, "testing kb", reply_markup=keyboardmain)
#
# @bot.callback_query_handler(func=lambda call:True)
# def callback_inline(call):
#     if call.data == "mainmenu":
#
#         keyboardmain = types.InlineKeyboardMarkup(row_width=2)
#         first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
#         second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
#         keyboardmain.add(first_button, second_button)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="menu",reply_markup=keyboardmain)
#
#     if call.data == "first":
#         keyboard = types.InlineKeyboardMarkup()
#         rele1 = types.InlineKeyboardButton(text="1t", callback_data="1")
#         rele2 = types.InlineKeyboardButton(text="2t", callback_data="2")
#         rele3 = types.InlineKeyboardButton(text="3t", callback_data="3")
#         backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
#         keyboard.add(rele1, rele2, rele3, backbutton)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)
#
#     elif call.data == "second":
#         keyboard = types.InlineKeyboardMarkup()
#         rele1 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
#         backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
#         keyboard.add(rele1,backbutton)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)
#
#     elif call.data == "1" or call.data == "2" or call.data == "3":
#         bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
#         keyboard3 = types.InlineKeyboardMarkup()
#         button = types.InlineKeyboardButton(text="lastlayer", callback_data="ll")
#         keyboard3.add(button)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="last layer",reply_markup=keyboard3)
