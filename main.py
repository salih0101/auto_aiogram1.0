import sqlite3
from aiogram import Dispatcher, executor, Bot, types
from aiogram.dispatcher import FSMContext
from states import Registration, GetProduct, Cart, Order, Settings, Search
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import buttons as btns
import database
import logging
import states
import csv
import os


load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())


delivery = f'Обратите внимание\n\n' \
           f''


about = f'Мы - ваш надежный союзник в мире автозапчастей.\n' \
        f'Огромный ассортимент, цены, от которых задыхается конкуренция, и безупречное качество - вот наши основные козыри.\n' \
        f'Доверьте нам заботу о вашем автомобиле, и он будет всегда в идеальном состоянии.\n'\
        f'Адрес: Узбекистан. Ташкент. 2020 - 2023\n' \

contacts = f'📞 Наш номер телефона:\n +998990952992 и +998990902992\n\n'\
            f'Присоединяйтесь к нам в Telegram: @SKODAVWXpress\n\n' \
            f'Администратор: @ms2992\n\n'\
            f'🚚 Мы также предлагаем бесплатную доставку по городу.\n\n'\
            f'Не стесняйтесь обращаться к нам, мы всегда готовы оказать помощь и поддержку в вопросах автозапчастей.'\


@dp.message_handler(commands=['start'], state='*')
async def start_message(message):
    start_txt = f'{message.from_user.first_name}\nДобро пожаловать в бот SKODA VW PartsXpress!'
    start_reg = f'Для начала пройдите простую регистрацию, чтобы в дальнейшем не было проблем с доставкой\n\nВведите Ваше имя:'

    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if user_id == 5928000362:
        await message.answer('Приветствую Администратор',
                             reply_markup=btns.admin_kb())
        await states.Admin.get_status.set()

    elif checker:
        await message.answer('\nДобро пожаловать в бот SKODA VW PartsXpress!\n\nЧтобы начать, выберите категорию, которая вас интересует.',
                             reply_markup=btns.main_menu())

    else:
        await message.answer(start_txt)
        await message.answer(start_reg,
                             reply_markup=btns.ReplyKeyboardMarkup())

        await states.Registration.getting_name_state.set()


@dp.message_handler(commands=['show_users'])
async def show_users(message: types.Message):
    admin_id = 5928000362

    if message.from_user.id != admin_id:
        response = "Команда доступна только администратору."
        await message.answer(response)
        return

    users = database.get_users()

    if users:

        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username"])

            for user in users:
                writer.writerow([user[0], user[1], user[2]])

        with open('users.csv', 'rb') as file:
            await message.bot.send_document(admin_id, file)

        response = "Список пользователей сохранен в файле users.csv и отправлен администратору."
    else:
        response = "Список пользователей пуст."

    await message.answer(response)


@dp.message_handler(state=Search.search_product, content_types=['text'])
async def search(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text:
        await message.reply('Вы не указали название товара.\n\n'
                            'Для поиска товара сперва напишите /search (Название товара)')
        return

    products = database.search_product(text)

    if not products:
        await message.reply('Товары не найдены.', reply_markup=btns.main_menu())

    else:
        matching_products = []

        for product in products:

            product_name = product[0].lower() + product[0]
            search_terms = text.lower().split()  # Приводим поисковый запрос к нижнему регистру

            if all(term in product_name for term in search_terms):
                matching_products.append(product)

        if not matching_products:
            await message.reply('Товары не найдены.', reply_markup=btns.main_menu())

            return

        else:
            for product in matching_products:
                await dp.current_state(user=user_id).update_data(pr_name=product[0], pr_count=1, price=product[2])

                await bot.send_photo(user_id,
                                     photo=product[4],
                                     caption=f'{product[0]}\n\nЦена: {product[2]} $\n\nОписание:\n {product[3]}',
                                     reply_markup=btns.send_admin_kb())



async def broadcast_message(message_text):

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()


    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text=message_text)

@dp.message_handler(commands=['broadcast'])
async def broadcast_command(message: types.Message):

    command_args = message.text.split(' ', maxsplit=1)
    if len(command_args) == 2:
        message_text = command_args[1]
        await broadcast_message(message_text)
        await message.reply(f'Сообщение успешно отправлено всем пользователям.')
    else:
        await message.reply('Неверный формат команды. Используйте /broadcast message_text')


@dp.message_handler(state=states.Admin.get_status)
async def get_name(message, state=states.Admin.get_status):
    if message.text == 'Добавить товар':

        await message.answer('Введите наименование товара')
        await states.Add_product.get_name.set()

    elif message.text == 'Меню клиента':

        user_id = message.from_user.id
        checker = database.check_user(user_id)

        if checker:

            await state.finish()
            await message.answer('Выберите продукт',
                                 reply_markup=btns.main_menu())

        else:

            start_txt = f'{message.from_user.first_name}\nПриветствуем в боте'
            start_reg = f'Для начала пройдите простую регистрацию, чтобы в дальнейшем не было проблем с доставкой\n\nВведите Ваше имя!:'

            await message.answer(start_txt)
            await message.answer(start_reg)

            await states.Registration.getting_name_state.set()


@dp.message_handler(state=states.Add_product.get_name)
async def product_name(message, state=states.Add_product.get_name):
    name = message.text

    await state.update_data(name=name)
    await message.answer(f'Теперь введите ID продукта {name}:>>')
    await states.Add_product.get_id.set()


@dp.message_handler(state=states.Add_product.get_id)
async def get_id(message, state=states.Add_product.get_id):
    name = message.text

    await state.update_data(id=name)
    await message.answer(f'Теперь введите стоимость:')
    await states.Add_product.get_price.set()


@dp.message_handler(state=states.Add_product.get_price)
async def product_price(message, state=states.Add_product.get_price):
    price = message.text

    await state.update_data(price=price)
    await message.answer('Теперь введите описание товара:>>')
    await states.Add_product.get_info.set()


@dp.message_handler(state=states.Add_product.get_info)
async def product_info1(message, state=states.Add_product.get_info):
    info_pr = message.text

    await state.update_data(description=info_pr)
    await message.answer('Теперь загрузите фото товара>>')
    await states.Add_product.get_photo.set()


@dp.message_handler(content_types=['photo'], state=states.Add_product.get_photo)
async def product_photo(message, state=states.Add_product.get_photo):

    all_info = await state.get_data()
    name = all_info.get('name')
    prd_id = all_info.get('id')
    price = all_info.get('price')
    description = all_info.get('description')
    photo_id = all_info.get('picture')
    nt = all_info.get('notes')
    picture = message.photo[-2].file_id
    await state.update_data(photo=photo_id)

    database.add_products_to_db(name, prd_id, price, description, picture, nt)

    await message.answer('Товар добавлен', reply_markup=btns.admin_kb())
    await states.Admin.get_status.set()


@dp.message_handler(state=Registration.getting_name_state)
async def get_name(message, state=Registration.getting_name_state):
    user_answer = message.text

    await state.update_data(name=user_answer)
    await message.answer('Имя сохранил!\nОтправьте номер телефона!',
                         reply_markup=btns.phone_number_kb())

    await Registration.getting_phone_number.set()


@dp.message_handler(state=Registration.getting_phone_number, content_types=['text', 'contact'])
async def get_number(message: types.Message, state: FSMContext):
    global user_answer

    if message.content_type == 'text':
        user_answer = message.text

        if not user_answer.replace('+', '').isdigit():
            await message.answer('Отправьте номер телефона')
            return

    elif message.content_type == 'contact':
        user_answer = message.contact.phone_number

    await state.update_data(number=user_answer)
    await message.answer('Номер сохранил!\n\nВы успешно прошли регистрацию!\n\nВыберите категорию.', reply_markup=btns.main_menu())

    await Registration.getting_gender.set()


    all_info = await state.get_data()
    name = all_info.get('name')
    phone_number = all_info.get('number')
    latitude = all_info.get('latitude')
    longitude = all_info.get('longitude')
    gender = user_answer
    user_id = message.from_user.id
    database.add_user(user_id, name, phone_number, latitude, longitude, gender)

    await state.finish()


@dp.message_handler(state=GetProduct.getting_pr_name, content_types=['text'])
async def choose_count(message):
    user_answerr = message.text
    user_id = message.from_user.id


    user_data = await dp.current_state(user=user_id).get_data()
    category_id = user_data.get('category_id')

    actual_products = [i[0] for i in database.get_name_product(category_id)]

    if user_answerr == 'Назад':
        await message.answer('Выберите категорию🔽',
                             reply_markup=btns.skoda_catalog())
        await dp.current_state(user=user_id).finish()


    elif user_answerr in actual_products:

        product_info = database.get_all_info_product(user_answerr)

        await dp.current_state(user=user_id).update_data(pr_name=user_answerr,
                                                         pr_count=1,
                                                         price=product_info[2]
                                                         )

        await bot.send_photo(user_id, photo=product_info[4],
                             caption=f'{product_info[0]}\n\n'
                                     f'Цена: {product_info[2]} $\n\n'
                                     f'Описание:\n {product_info[3]}\n\n'
                                     f'@VW_Skoda_Bot',
                             reply_markup=btns.product_count())
        await message.answer('Выберите количество1️⃣2️⃣3️⃣')

        await dp.current_state(user=user_id).update_data(user_product=message.text,
                                                         price=product_info[2])

        await states.GetProduct.getting_pr_count.set()



    elif user_answerr == 'Назад VW':
        await message.answer('Выберите категорию🔽',
                             reply_markup=btns.vw_catalog())
        await dp.current_state(user=user_id).finish()


@dp.message_handler(state=GetProduct.getting_pr_count)
async def text_message3(message, state=GetProduct.getting_pr_count):
    product_count = message.text
    user_data = await state.get_data()
    user_product = user_data.get('user_product')
    category_id = user_data.get('category_id')
    pr_price = float(user_data.get('price'))


    if product_count.isnumeric():
        database.add_pr_to_cart(message.from_user.id, user_product, pr_price, int(product_count))
        database.add_pr_to_cart2(message.from_user.id, user_product, pr_price, int(product_count))

        await message.answer('Товар добавлен в корзину✅\n\nВыберите продукт🔽',
                             reply_markup=btns.main_menu())
        await state.finish()


    else:
        await message.answer('Нажмите еще раз кнопку Назад🔽',
                             reply_markup=btns.product_name_kb(category_id))
        await states.GetProduct.getting_pr_name.set()


@dp.message_handler(state=Cart.waiting_for_product)
async def cart_function(message, state=Cart.waiting_for_product):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\n'
                             'Выберите раздел🔽',
                             reply_markup=btns.main_menu())

        await dp.current_state(user=message.from_user.id).finish()


    elif user_answer == '🆑Очистить':

        database.delete_from_cart(user_id)
        await message.answer('Корзина очищена✅\n\n❗️❗️Нажмите кнопку Назад❗️❗️')

    if user_answer == '✅Оформить заказ':

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ::\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
                admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:.2f}$'
        await message.answer('Раздел оформления заказа🔽',
                             reply_markup=btns.confirmation_kb())


    elif user_answer == 'Подтвердить':

        order_id = datetime.now().microsecond
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:
            result_answer = f'Ваш заказ № {order_id} :\n\n'
            admin_message = f'Новый заказ № {order_id}:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
                admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:.2f}$\n\n'
            admin_message += f' Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$\n\n'

            delivery_date = datetime.now() + timedelta(days=14)
            result_answer += f'Дата доставки: {delivery_date.strftime("%d.%m.%Y")}'
            admin_message += f'Дата доставки: {delivery_date.strftime("%d.%m.%Y")}'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            await message.answer('Успешно оформлен✅\n\n')
            await state.finish()
            await bot.send_message(5928000362, admin_message)
            database.delete_from_cart(user_id)


@dp.message_handler(state=Order.waiting_accept)
async def accept_order(message):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽',
                             reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()


    elif user_answer == 'Оформить заказ':
        order_id = datetime.now().microsecond
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:
            result_answer = f'Ваш заказ № {order_id}:\n\n'
            admin_message = f'Новый заказ № {order_id}:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                total_price += i[3]

            result_answer += f'\nИтог: {total_price:.2f}$\n\n'
            admin_message += f'Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$\n\n'

            delivery_date = datetime.now() + timedelta(days=14)
            result_answer += f'Дата доставки: {delivery_date.strftime("%d.%m.%Y")}'
            admin_message += f'Дата доставки: {delivery_date.strftime("%d.%m.%Y")}'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            await message.answer('Успешно оформлен✅\n\n')
            await bot.send_message(5928000362, admin_message)
            await dp.current_state(user=message.from_user.id).finish()
            database.delete_from_cart(user_id)



@dp.message_handler(state=Settings.set_setting, content_types=['text'])
async def set_name(message):
    user_answer = message.text
    user_id = message.from_user.id
    try:
        match user_answer:
            case 'Изменить имя':
                await message.answer('Отправьте имя')
                await Settings.set_name.set()

            case 'Изменить номер':
                await message.answer('Отправьте номер')
                await Settings.set_number.set()

    except Exception as e:
        print(e)
        await message.answer('Неверный ввод')

    try:
        match user_answer:
            case 'НАЗАД':
                await message.answer('Вы вернулись в Главное меню', reply_markup=btns.main_menu())
                await dp.current_state(user=user_id).reset_state()

    except Exception as e:
        print(e)
        await message.answer('Неверный ввод')


@dp.message_handler(state=states.Settings.set_name)
async def change_name_db(message, state=Settings.set_name):
    user_answer = message.text

    await state.update_data(name=user_answer)

    ch_name = await state.get_data()
    user_id = message.from_user.id
    database.change_name(user_id, ch_name)
    await state.finish()
    await message.answer('Имя пользователя "Успешно изменен"', reply_markup=btns.main_menu())


@dp.message_handler(state=Settings.set_number)
async def change_number_db(message, state=Settings.set_number):
    user_answer = message.text

    await state.update_data(phone_number=user_answer)

    ch_number = await state.get_data()
    user_id = message.from_user.id
    database.change_number(user_id, ch_number)
    await state.finish()
    await message.answer('Номер Успешно изменен', reply_markup=btns.main_menu())



@dp.message_handler(content_types=['text'])
async def main_menu(message):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == '🛒Корзина':
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:
            result_answer = 'Ваша корзина🗑:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:.2f}$'

            await message.answer(result_answer, reply_markup=btns.cart_kb())
            await Cart.waiting_for_product.set()

        else:
            await message.answer('Ваша корзина пустая🗑')

    if user_answer == 'SKODA':
        await message.answer('Выберите категорию🔽',
                             reply_markup=btns.skoda_catalog())


    elif user_answer == '🔍Поиск':
        await message.answer('Отправьте название товара', reply_markup=btns.ReplyKeyboardRemove())
        await states.Search.search_product.set()


    elif user_answer == '👤Профиль':
        await message.answer('Выберите что хотите изменить', reply_markup=btns.change_data_kb())
        await states.Settings.set_setting.set()


    elif user_answer == '🔙Назад':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽',
                             reply_markup=btns.main_menu())
        await dp.current_state(user=user_id).finish()


    elif user_answer == 'ХОДОВАЯ ЧАСТЬ':
        await dp.current_state(user=user_id).update_data(category_id=15)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.auto_skoda_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'ЭЛЕКТРИКА':
        await dp.current_state(user=user_id).update_data(category_id=17)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.electrics_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'МОТОРНАЯ ЧАСТЬ':
        await dp.current_state(user=user_id).update_data(category_id=16)
        await message.answer('Скоро...',
                             reply_markup=btns.motor_skoda_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'АКСЕССУАРЫ':
        await dp.current_state(user=user_id).update_data(category_id=22)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.accessories_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'ФИЛЬТРА':
        await dp.current_state(user=user_id).update_data(category_id=44)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.filter_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'АВТОХИМИЯ':
        await dp.current_state(user=user_id).update_data(category_id=33)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.chemical_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'ОСТАЛЬНОЕ':
        await dp.current_state(user=user_id).update_data(category_id=55)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.other_kb())
        await states.GetProduct.getting_pr_name.set()

    if user_answer == 'VOLKSWAGEN':
        await message.answer('Выберите категорию🔽',
                             reply_markup=btns.vw_catalog())


    elif user_answer == 'ЭЛЕКТРИКА VW':
        await dp.current_state(user=user_id).update_data(category_id=77)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.electrics_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'АКСЕССУАРЫ VW':
        await dp.current_state(user=user_id).update_data(category_id=33)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.vw_accessories_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'ХОДОВАЯ ЧАСТЬ VW':
        await dp.current_state(user=user_id).update_data(category_id=11)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.vw_auto_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'МОТОРНАЯ ЧАСТЬ VW':
        await dp.current_state(user=user_id).update_data(category_id=22)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.vw_motor_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'ФИЛЬТРА VW':
        await dp.current_state(user=user_id).update_data(category_id=55)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.vw_filter_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'АВТОХИМИЯ VW':
        await dp.current_state(user=user_id).update_data(category_id=44)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.vw_chemical_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'ОСТАЛЬНОЕ VW':
        await dp.current_state(user=user_id).update_data(category_id=66)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.vw_other_kb())
        await states.GetProduct.getting_pr_name.set()


    if user_answer == '◀️Назад':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽',
                             reply_markup=btns.main_menu())
        await dp.current_state(user=user_id).finish()


    elif user_answer == 'О нас':
        await message.answer(about)


    elif user_answer == '☎️Контакты':
        await message.answer(contacts)

    elif user_answer == '📄Список заказов':
        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:

            result_answer = 'Ваш заказ:\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:.2f}$'
            admin_message += f' Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$'

            await message.answer(result_answer,
                                 reply_markup=btns.order_kb())

            await Order.waiting_accept.set()

        else:
            await message.answer('Ваша корзина пустая🗑\n\n'
                                 'Для выбора продукта нажмите одну из кнопок ниже')


@dp.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'],
                           state=states.GetProduct.getting_pr_count)
async def get_user_product_count(call):

    user_id = call.message.chat.id


    if call.data == 'increment':
        user_data = await dp.current_state(user=user_id).get_data()
        actual_count = user_data['pr_count']


        await dp.current_state(user=user_id).update_data(pr_count=user_data['pr_count'] + 1)


        await bot.edit_message_reply_markup(chat_id=user_id,
                                            message_id=call.message.message_id,
                                            reply_markup=btns.choose_product_count('increment', actual_count))


    elif call.data == 'decrement':
        user_data = await dp.current_state(user=user_id).get_data()
        actual_count = user_data['pr_count']


        await dp.current_state(user=user_id).update_data(pr_count=user_data['pr_count'] - 1)


        await bot.edit_message_reply_markup(chat_id=user_id,
                                            message_id=call.message.message_id,
                                            reply_markup=btns.choose_product_count
                                            ('decrement', actual_count))



    elif call.data == 'back':

        await call.message.answer('Выберите пункт меню',
                                  reply_markup=btns.skoda_catalog())
        await dp.current_state(user=user_id).finish()


    elif call.data == 'to_cart':

        user_data = await dp.current_state(user=user_id).get_data()
        product_count = user_data['pr_count']
        user_product = user_data['pr_name']
        price = user_data['price']


        database.add_pr_to_cart(user_id, user_product, price, product_count)


        await call.message.delete()
        await call.message.answer('Продукт добавлен в корзину\nЧто-нибудь еще?',
                                  reply_markup=btns.main_menu())

        await dp.current_state(user=user_id).finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
