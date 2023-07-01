from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
import database


def get_username_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Взять из ТГ аккаунта')
    kb.add(btn)

    return kb


def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_add = KeyboardButton('Добавить товар')
    btn_client = KeyboardButton('Меню клиента')
    btn_client1 = KeyboardButton('/show_users')
    kb.add(btn_add, btn_client, btn_client1)

    return kb


def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Отправить номер телефона', request_contact=True)
    kb.add(button)

    return kb


def location_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Отправить локацию', request_location=True)
    kb.add(button)

    return kb


def gender_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('👨Мужчина')
    button1 = KeyboardButton('👩‍🦰Женщина')
    kb.add(button, button1)

    return kb


def product_count():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [KeyboardButton(i) for i in range(1, 5)]
    back = KeyboardButton('Назад')
    kb.add(*buttons)
    kb.add(back)

    return kb


def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('SKODA')
    keyboard.add('VOLKSWAGEN')
    keyboard.add('📄Список заказов', '👤Профиль')
    keyboard.add('🔍Поиск', '🛒Корзина')
    keyboard.add('☎️Контакты', 'О нас')

    return keyboard

def change_data_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    ch_name = KeyboardButton('Изменить имя')
    ch_number = KeyboardButton('Изменить номер')
    back = KeyboardButton('НАЗАД')
    kb.add(ch_name, ch_number, back)

    return kb

def accessories_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.accessories_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def electrics_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.electrics_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def auto_skoda_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.auto_skoda_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def motor_skoda_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.motor_skoda_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def chemical_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.chemical_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def filter_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.filter_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def other_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад')

    all_products = database.other_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def catalog_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад')

    all_products = database.get_product_id_from_db()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def cart_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = KeyboardButton('🆑Очистить')
    button1 = KeyboardButton('✅Оформить заказ')
    back = KeyboardButton('Назад')
    kb.add(button1, button, back)

    return kb


def order_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Оформить заказ')
    back = KeyboardButton('Назад')
    kb.add(button1, back)

    return kb


def confirmation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Подтвердить')
    button1 = KeyboardButton('Отменить')
    button2 = KeyboardButton('Назад')
    kb.add(button, button1, button2)

    return kb


def product_name_kb(category_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад')
    all_products = database.get_name_product(category_id)

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)


def skoda_catalog():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('АКСЕССУАРЫ', 'АВТОХИМИЯ')
    keyboard.add('ЭЛЕКТРИКА')
    keyboard.add('ХОДОВАЯ ЧАСТЬ', 'МОТОРНАЯ ЧАСТЬ')
    keyboard.add('ФИЛЬТРА', 'ОСТАЛЬНОЕ')
    keyboard.add('🛒Корзина', '🔙Назад')

    return keyboard


def vw_catalog():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('АКСЕССУАРЫ VW')
    keyboard.add('АВТОХИМИЯ VW', 'ЭЛЕКТРИКА VW')
    keyboard.add('ХОДОВАЯ ЧАСТЬ VW', 'МОТОРНАЯ ЧАСТЬ VW')
    keyboard.add('ФИЛЬТРА VW', 'ОСТАЛЬНОЕ VW')
    keyboard.add('🛒Корзина', '◀️Назад')

    return keyboard


def search_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton('🏠Главное меню')

    kb.add(back)

    return kb


def vw_accessories_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад VW')
    all_products = database.vw_accessories_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_auto_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад VW')
    all_products = database.auto_vw_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_motor_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад VW')
    all_products = database.motor_vw_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_chemical_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад VW')
    all_products = database.vw_chemical_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_filter_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад VW')
    all_products = database.vw_filter_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_electrics_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.electrics_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_other_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад VW')

    all_products = database.vw_other_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def choose_product_count(plus_or_minus='', current_amount=1):

    kb = InlineKeyboardMarkup(row_width=3)


    back = InlineKeyboardButton(text='Отправить администратору', url='https://t.me/activebee_tashkent')
    plus = InlineKeyboardButton(text='+', callback_data='increment')
    minus = InlineKeyboardButton(text='-', callback_data='decrement')
    count = InlineKeyboardButton(text=str(current_amount),
                                 callback_data=str(current_amount))
    add_to_cart = InlineKeyboardButton(text='Добавить в корзину',
                                       callback_data='to_cart')

    if plus_or_minus == 'increment':
        new_amount = int(current_amount) + 1

        count = InlineKeyboardButton(text=str(new_amount),
                                     callback_data=str(new_amount))

    elif plus_or_minus == 'decrement':
        if int(current_amount) > 1:
            new_amount = int(current_amount) - 1

            count = InlineKeyboardButton(text=str(new_amount),
                                         callback_data=str(new_amount))


    kb.add(minus, count, plus)
    kb.row(add_to_cart)

    return kb


def send_admin_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    send = InlineKeyboardButton(text='Отправить администратору', url='https://t.me/activebee_tashkent')

    kb.add(send)
    return kb
