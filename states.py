from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    getting_name_state = State()
    getting_phone_number = State()
    getting_location = State()
    getting_gender = State()


class Order(StatesGroup):
    waiting_location = State()
    waiting_pay_type = State()
    waiting_accept = State()


class Add_product(StatesGroup):
    get_name = State()
    get_id = State()
    get_price = State()
    get_info = State()
    get_photo = State()


class Search(StatesGroup):
    search_product = State()


class Admin(StatesGroup):
    get_status = State()


class GetProduct(StatesGroup):
    getting_pr_name = State()
    getting_pr_count = State()


class Cart(StatesGroup):
    waiting_for_product = State()
    waiting_new_count = State()



