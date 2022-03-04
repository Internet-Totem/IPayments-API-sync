import telebot
from telebot import types

import api_help

TOKEN_TELEGRAM = ''
TOKEN_IPAYMENTS = ''

bot = telebot.TeleBot(token=TOKEN_TELEGRAM, parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start(message):
    if len(message.text.split('_')) == 1: # Стандартная комманда
        reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply.add(types.KeyboardButton(text='Купить товар'))
        bot.send_message(message.chat.id, '*Приветствую в Enot Shop!*', reply_markup=reply)

    else: # Команда с deep linking
        msg_type = message.text.split(' ')

        if 'newPay' in msg_type[1]: # Сообщение о новой оплате
            invoice_id = msg_type[1].split('_')[1]

            try:
                invoice = api_help.api(TOKEN_IPAYMENTS).checkInvoice(invoice_id)
            except:
                bot.send_message(message.chat.id, '*Произошла ошибка при попытке получить информацию о счете.* Скорее всего, где-то произошла ошибка -> счет был создан.')
                return 0

            if invoice['result']['status'] == 'PAID':
                # Необходимо проверить, не был ли выдан пользователю товар по этому счете ранее

                # На этом система подошла к концу, тут необходимо реализовать выдачу товара
                if invoice['result']['amount'] == 5500:
                    bot.send_message(message.chat.id, '*К сожалению, сейчас не удалось найти машину времени в наличии.*\n\nВся сумма была возвращена.')
                    api_help.api(TOKEN_IPAYMENTS).refundInvoice(invoice_id) # Отмена оплаченного счета

                elif invoice['result']['amount'] == 14200:
                    userEmail = invoice['result']['email']
                    bot.send_message(message.chat.id, '*Билеты были отправлены на почту:* ' + userEmail)

                elif invoice['result']['amount'] == 245.3:
                    bot.send_message(message.chat.id, '*Покупка оплачена успешно!*\n\nВсе оплаченные товары: карандаши, тетради, ручка и блокнот.')

            else:
                bot.send_message(message.chat.id, '*Не удалось найти оплату!*\nВозможно, кто-то пролил кофе на сервер.')



@bot.message_handler(content_types=['text'])
def text(message):
    reply = types.InlineKeyboardMarkup(row_width=1)
    replybtn1 = types.InlineKeyboardButton(text='Машина времени', callback_data='buy_TimeMachine')
    replybtn2 = types.InlineKeyboardButton(text='Билеты на луну', callback_data='buy_tickets')
    replybtn3 = types.InlineKeyboardButton(text='Канцтовары', callback_data='buy_stationery')
    reply.add(replybtn1, replybtn2, replybtn3)

    bot.send_message(message.chat.id, 'Выберите товар который хотите купить.', reply_markup=reply)


@bot.callback_query_handler(lambda call: True)
def callback(call):
    if call.message:
        call_type = call.data.split('_')[0]

        if call_type == 'buy': # Купить товар
            tovar = call.data.split('_')[1]

            if tovar == 'TimeMachine':
                amount = 5500
                product_list = '[{"name": "Машина времени", "number": 1, "amount": 5500}]'
                myBot = 'enotShopBot' # Ваш бот без @
                name = 'Счет на оплату в боте EnotShop'
                description = 'Тестовый счет с машиной времени! А здесь любой текст до 250 символов (кроме ссылки).'
                success_text = 'Спасибо за оплату! Перейдите в бота для получения товара!'

                invoice = api_help.api(TOKEN_IPAYMENTS).createInvoice(amount, product_list, name=name, description=description, success_btn_bot=myBot, success_text=success_text)

                reply = types.InlineKeyboardMarkup()
                reply.add(types.InlineKeyboardButton(text='Оплатить', url=invoice['result']['url']))

                bot.edit_message_text('Счет на оплату готов.\n\n*Машина времени\nКол-во:* 1 шт.\n*Цена:* 5500 RUB\n\nОплатите счет в течении 20 минут. \
*После оплаты перейдите по выданной кнопке.*',
                                      call.message.chat.id, call.message.message_id, reply_markup=reply)

            elif tovar == 'tickets':
                amount = 14200
                product_list = '[{"name": "Билет на луну (туда и назад)", "number": 2, "amount": 14200}]'
                success_btn = 'openURL'
                myURL = 'https://www.example.net/'  # Любая ссылка на получение товара
                name = 'Счет на оплату в боте EnotShop'
                success_text = 'Спасибо за оплату! Перейдите по ссылке для получения товара!'
                need_email = True # Нужен email чтобы выслать билеты !)

                invoice = api_help.api(TOKEN_IPAYMENTS).createInvoice(amount, product_list, success_btn, name=name, success_btn_url=myURL, success_text=success_text, need_email=need_email)

                reply = types.InlineKeyboardMarkup()
                reply.add(types.InlineKeyboardButton(text='Оплатить', url=invoice['result']['url']))

                bot.edit_message_text('Счет на оплату готов.\n\n*Билет на луну (туда и назад)\nКол-во:* 2 шт.\n*Цена:* 14200 RUB\n\nОплатите счет в течении 20 минут. \
*После оплаты перейдите по выданной кнопке.*',
                                      call.message.chat.id, call.message.message_id, reply_markup=reply)

            elif tovar == 'stationery':
                amount = 245.30
                product_list = '[{"name": "Ручка шариковая", "number": 1, "amount": 20}, {"name": "Карандаш", "number": 2, "amount": 35.30},' \
                               '{"name": "Тетрадь (24 листа)", "number": 3, "amount": 40}, {"name": "Блокнот", "number": 1, "amount": 150}]'
                myBot = 'enotShopBot'  # Ваш бот без @
                description = 'Тестовый счет с канцтоварами!'

                invoice = api_help.api(TOKEN_IPAYMENTS).createInvoice(amount, product_list, description=description, success_btn_bot=myBot)

                reply = types.InlineKeyboardMarkup()
                reply.add(types.InlineKeyboardButton(text='Оплатить', url=invoice['result']['url']))

                bot.edit_message_text('Счет на оплату готов.\n\n*Ручка шариковая\nКол-во:* 1 шт.\n*Цена:* 20 RUB\n\n*Карандаш\nКол-во:* 2 шт.\n*Цена:* 35.30 RUB\n\n\
*Тетрадь (24 листа)\nКол-во:* 3 шт.\n*Цена:* 40 RUB\n\n*Блокнот\nКол-во:* 1 шт.\n*Цена:* 150 RUB\n\n*Итоговая цена:* 245.30 RUB\
\n\nОплатите счет в течении 20 минут. \
*После оплаты перейдите по выданной кнопке.*',
                                      call.message.chat.id, call.message.message_id, reply_markup=reply)

bot.polling()