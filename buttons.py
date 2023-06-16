from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
import database


def get_username_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Взять из ТГ аккаунта')
    kb.add(btn)

    return kb


def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = KeyboardButton('Добавить товар')
    btn_client = KeyboardButton('Зайти как клиент')
    kb.add(btn_add, btn_client)

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
    button = KeyboardButton('Мужчина👨')
    button1 = KeyboardButton('Женщина👩‍🦰')
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
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    skoda = KeyboardButton('SKODA')
    vw = KeyboardButton('VOLKSWAGEN')
    order = KeyboardButton('Список заказов📄')
    cart = KeyboardButton('Корзина🗑')
    about = KeyboardButton('О нас')
    callback = KeyboardButton('Контакты☎️')

    kb.add(skoda, vw, order, cart, callback, about)

    return kb


def accessories_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.accessories_product()

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
    button = KeyboardButton('Очистить🆑')
    button1 = KeyboardButton('Оформить заказ✅')
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


def count_kb(category_id):

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад')
    all_products = database.get_name_product(category_id)

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)


def skoda_catalog():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    accessories = KeyboardButton('АКСЕССУАРЫ')
    xod_ch = KeyboardButton('ХОДОВАЯ ЧАСТЬ')
    mot_ch1 = KeyboardButton('МОТОРНАЯ ЧАСТЬ')
    filters = KeyboardButton('ФИЛЬТРА')
    chemical = KeyboardButton('АВТОХИМИЯ')
    other = KeyboardButton('ОСТАЛЬНОЕ')
    cart = KeyboardButton('Корзина🗑')
    back = KeyboardButton('Назад🔙')

    kb.add(xod_ch, mot_ch1, accessories, chemical, filters, other, back, cart)

    return kb


def vw_catalog():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    accessories = KeyboardButton('АКСЕССУАРЫ VW')
    xod_ch = KeyboardButton('ХОДОВАЯ ЧАСТЬ VW')
    mot_ch1 = KeyboardButton('МОТОРНАЯ ЧАСТЬ VW')
    filters = KeyboardButton('ФИЛЬТРА VW')
    chemical = KeyboardButton('АВТОХИМИЯ VW')
    other = KeyboardButton('ОСТАЛЬНОЕ VW')
    cart = KeyboardButton('Корзина🗑')
    back = KeyboardButton('Назад◀️')

    kb.add(accessories, xod_ch, mot_ch1, chemical, filters, other, back, cart)

    return kb


def search_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    search = KeyboardButton('Поиск')
    back = KeyboardButton('Назад⬅️')

    kb.add(search, back)

    return kb


def vw_accessories_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.vw_accessories_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_auto_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.auto_vw_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_motor_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.motor_vw_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_chemical_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.vw_chemical_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_filter_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.vw_filter_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb


def vw_other_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад')

    all_products = database.vw_other_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb

