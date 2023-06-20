from aiogram import Dispatcher, executor, Bot, types
from states import Registration, GetProduct, Cart, Order
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
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

about = f'Ваш надежный партнер в Автозапчастях. \nШирокий выбор, конкурентные цены, высокое качество. \nПоможем поддерживать ваш автомобиль в отличном состоянии.'


@dp.message_handler(commands=['start'], state='*')
async def start_message(message):
    start_txt = f'{message.from_user.first_name}\nПриветствуем в боте'
    start_reg = f'Для начала пройдите простую регистрацию, чтобы в дальнейшем не было проблем с доставкой\n\nВведите Ваше имя или выберите поделиться👇:'

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    checker = database.check_user(user_id)

    if user_id == 1186132006:
        await message.answer('Приветствую Администратор',
                             reply_markup=btns.admin_kb())
        await states.Admin.get_status.set()

    elif checker:
        await message.answer('Выберите категорию',
                             reply_markup=btns.main_menu())

    else:
        await message.answer(start_txt)
        await message.answer(start_reg,
                             reply_markup=btns.get_username_kb())

        await states.Registration.getting_name_state.set()


# @dp.message_handler(commands=['show_users'])
# async def show_users(message: types.Message):
#     users = database.get_users()
#
#
#     if users:
#         response = "Список пользователей:\n"
#         for user in users:
#             response += f"ID: {user[1]}, Username: {user[0]}\n"
#     else:
#         response = "Список пользователей пуст."
#
#
#     await message.answer(response)


@dp.message_handler(commands=['show_users'])
async def show_users(message: types.Message):
    admin_id = 1186132006

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
                writer.writerow([user[0], user[1]])

        with open('users.csv', 'rb') as file:
            await message.bot.send_document(admin_id, file)

        response = "Список пользователей сохранен в файле users.csv и отправлен администратору."
    else:
        response = "Список пользователей пуст."

    await message.answer(response)


# import codecs
#
# @dp.message_handler(commands=['show_users'])
# async def show_users(message: types.Message):
#     admin_id = 1186132006
#
#     if message.from_user.id != admin_id:
#         response = "Команда доступна только администратору."
#         await message.answer(response)
#         return
#
#     users = database.get_users()
#
#     if users:
#         with codecs.open('users.csv', 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(["ID", "Username", "Number"])
#
#             for user in users:
#                 writer.writerow([user[0], user[1], user[2]])
#
#         with open('users.csv', 'rb') as file:
#             await message.bot.send_document(admin_id, file)
#
#         response = "Список пользователей сохранен в файле users.csv и отправлен администратору."
#     else:
#         response = "Список пользователей пуст."
#
#     await message.answer(response)


@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    if not args:
        await message.reply('Вы не указали название товара.')
        return

    products = database.search_product(args)

    if not products:
        await message.reply('Товары не найдены.')

    else:

        for product in products:
            await dp.current_state(user=user_id).update_data(pr_name=product[0], pr_count=1, price=product[2])

            await bot.send_photo(user_id,
                                 photo=product[4],
                                 caption=f'{product[0]}\n\nЦена: {product[2]} $\n\nОписание:\n {product[3]}',
                                 reply_markup=btns.choose_product_count())

        await states.GetProduct.getting_pr_count.set()

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
            start_reg = f'Для начала пройдите простую регистрацию, чтобы в дальнейшем не было проблем с доставкой\n\nВведите Ваше имя или выберите поделиться👇:'

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
    print(name)
    prd_id = all_info.get('id')
    price = all_info.get('price')
    description = all_info.get('description')
    photo_id = all_info.get('picture')
    nt = all_info.get('notes')
    picture = message.photo[-2].file_id
    print(picture)
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


@dp.message_handler(state=Registration.getting_phone_number, content_types=['contact'])
async def get_number(message, state=Registration.getting_phone_number):
    user_answer = message.contact.phone_number

    await state.update_data(number=user_answer)
    await message.answer('Номер сохранил!\nОтправьте локацию!📍',
                         reply_markup=btns.gender_kb())

    await Registration.getting_gender.set()


@dp.message_handler(state=Registration.getting_gender)
async def get_location(message, state=Registration.getting_gender):
    user_answer = message.text

    await message.answer('Успешно зарегистрирован📝!\nВыберите раздел!',
                         reply_markup=btns.main_menu())

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
    user_answer = message.text
    user_id = message.from_user.id

    user_data = await dp.current_state(user=user_id).get_data()
    category_id = user_data.get('category_id')

    actual_products = [i[0] for i in database.get_name_product(category_id)]

    if user_answer in actual_products:

        product_info = database.get_all_info_product(user_answer)
        # Сохраним продукт во временный словарь
        # call.data - значение нажатой кнопки(инлайн)
        await dp.current_state(user=user_id).update_data(pr_name=user_answer, pr_count=1, price=product_info[2])

        # await bot.send_photo(user_id, photo=product_info[4],
        #                      caption=f'{product_info[0]}\n\nЦена: {product_info[2]} $\n\nОписание:\n {product_info[3]}\n\nВыберите количество1️⃣2️⃣3️⃣',
        #                      reply_markup=btns.product_count())

        await bot.send_photo(user_id, photo=product_info[4],
                             caption=f'{product_info[0]}\n\nЦена: {product_info[2]} $\n\nОписание:\n {product_info[3]}\n\nВыберите количество1️⃣2️⃣3️⃣',
                             reply_markup=btns.choose_product_count())

        await dp.current_state(user=user_id).update_data(user_product=message.text, price=product_info[2])

        await states.GetProduct.getting_pr_count.set()

    elif user_answer == 'Назад':
        await message.answer('Выберите категорию🔽',
                             reply_markup=btns.skoda_catalog())
        await dp.current_state(user=user_id).finish()

    elif user_answer == 'Назад VW':
        await message.answer('Выберите категорию🔽',
                             reply_markup=btns.vw_catalog())
        await dp.current_state(user=user_id).finish()


# @dp.message_handler(state=GetProduct.getting_pr_count)
# async def text_message3(message, state=GetProduct.getting_pr_count):
#     product_count = message.text
#     user_data = await state.get_data()
#     user_product = user_data.get('user_product')
#     category_id = user_data.get('category_id')
#     pr_price = float(user_data.get('price'))
#     user_id = message.from_user.id
#
#     if product_count.isnumeric():
#         database.add_pr_to_cart(message.from_user.id, user_product, pr_price, int(product_count))
#         database.add_pr_to_cart2(message.from_user.id, user_product, pr_price, int(product_count))
#
#         await message.answer('Товар добавлен в корзину✅\n\nВыберите продукт🔽',
#                              reply_markup=btns.main_menu())
#         await state.finish()
#
#     # elif message.text != 'Главное меню':
#     #     await message.answer('Тест', reply_markup=btns.main_menu())
#
#     else:
#         await message.answer('Нажмите еще раз кнопку Назад🔽',
#                              reply_markup=btns.product_name_kb(category_id))
#         await states.GetProduct.getting_pr_name.set()


@dp.message_handler(state=Cart.waiting_for_product)
async def cart_function(message, state=Cart.waiting_for_product):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Назад':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽',
                             reply_markup=btns.main_menu())
        await dp.current_state(user=message.from_user.id).finish()


    elif user_answer == '🆑Очистить':

        database.delete_from_cart(user_id)
        await message.answer('Корзина очищена✅\n\n❗️❗️Нажмите кнопку Назад❗️❗️')

    if user_answer == 'Оформить заказ✅':

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
            result_answer = f'Ваш заказ №{order_id} :\n\n'
            admin_message = f'Новый заказ {order_id} ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n'
                admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}$\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:.2f}$'
            admin_message += f'Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$'

            await message.answer(result_answer, reply_markup=btns.main_menu())
            await message.answer('Успешно оформлен✅\n\n')
            await state.finish()
            await bot.send_message(admin_message)
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

        user_cart = database.get_user_cart(message.from_user.id)

        if user_cart:
            result_answer = 'Ваш заказ::\n\n'
            admin_message = 'Новый заказ✅✅:\n\n'
            total_price = 0

            for i in user_cart:
                result_answer += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}\n\n'
                admin_message += f'- {i[1]}: {i[-1]} шт = {i[3]:.2f}\n\n'
                total_price += i[3]

            result_answer += f' \nИтог: {total_price:.2f}$'
            admin_message += f'Номер телефона: {i[2]}\n\nИтог: {total_price:.2f}$'

            await message.answer(result_answer,
                                 reply_markup=btns.main_menu())

            await message.answer('Успешно оформлен✅\n\n')
            await bot.send_message(5928000362, admin_message)
            await dp.current_state(user=message.from_user.id).finish()
            database.delete_from_cart(user_id)


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


    elif user_answer == '🔙Назад':
        await message.answer('❗️Вы вернулись в Главное меню❗️\n\nВыберите раздел🔽',
                             reply_markup=btns.main_menu())
        await dp.current_state(user=user_id).finish()


    elif user_answer == 'ХОДОВАЯ ЧАСТЬ':
        await dp.current_state(user=user_id).update_data(category_id=15)
        await message.answer('Выберите продукт🔽',
                             reply_markup=btns.auto_skoda_kb())
        await states.GetProduct.getting_pr_name.set()


    elif user_answer == 'МОТОРНАЯ ЧАСТЬ':
        await dp.current_state(user=user_id).update_data(category_id=16)
        await message.answer('Выберите продукт🔽',
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
        await message.answer(f'📞 Телефон:\n+998990952992\n+998990902992 \n\nTelegram: @ms2992'
                             f'\n\n🚚 Доставка по городу: Бесплатно')


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


# Обработчик выбора количества
@dp.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'],
                           state=states.GetProduct.getting_pr_count)
async def get_user_product_count(call):
    # Сохраним айди пользователя
    user_id = call.message.chat.id

    # Если пользователь нажал на +
    if call.data == 'increment':
        user_data = await dp.current_state(user=user_id).get_data()
        actual_count = user_data['pr_count']

        # Обновим значение количества
        await dp.current_state(user=user_id).update_data(pr_count=user_data['pr_count'] + 1)

        # Меняем значение кнопки
        await bot.edit_message_reply_markup(chat_id=user_id,
                                            message_id=call.message.message_id,
                                            reply_markup=btns.choose_product_count('increment', actual_count))

    # decrement
    # Если пользователь нажал на -
    elif call.data == 'decrement':
        user_data = await dp.current_state(user=user_id).get_data()
        actual_count = user_data['pr_count']

        # Обновим значение количества
        await dp.current_state(user=user_id).update_data(pr_count=user_data['pr_count'] - 1)

        # Меняем значение кнопки
        await bot.edit_message_reply_markup(chat_id=user_id,
                                            message_id=call.message.message_id,
                                            reply_markup=btns.choose_product_count('decrement', actual_count))

    # back
    # Если пользователь нажал 'назад'
    elif call.data == 'back':
        # Получаем меню
        products = database.get_name_product()
        # меняем на меню
        await bot.edit_message_text('Выберите пункт меню',
                                    user_id,
                                    call.message.message_id,
                                    reply_markup=btns.main_menu())

    # Если нажал Добавить в корзину
    elif call.data == 'to_cart':
        # Получаем данные
        user_data = await dp.current_state(user=user_id).get_data()
        product_count = user_data['pr_count']
        user_product = user_data['pr_name']
        price = user_data['price']

        # Добавляем в базу(корзина пользователя)
        database.add_pr_to_cart(user_id, user_product, price, product_count)

        # Получаем обратно меню

        # меняем на меню
        await call.message.delete()
        await call.message.answer('Продукт добавлен в корзину\nЧто-нибудь еще?',
                                  reply_markup=btns.main_menu())

        await dp.current_state(user=user_id).finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
