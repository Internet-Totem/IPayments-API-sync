import requests


def send_request(request_url, method, params=None):
    request = requests.get(request_url + method, params=params)

    if not request.ok:
        raise Exception('Сервер ответил ошибкой (или не ответил). Возможно нестабильное соединение с сетью')

    else:
        request = request.json()

    if request['fatalError']:
        raise Exception(request['description'])

    return request


class api:
    def __init__(self, token):
        self.token = token
        self.request_url = 'http://127.0.0.1/' + token + '/'

        send_request(self.request_url, 'getMe')

    def createInvoice(self,
                      amount,
                      product_list,
                      success_btn='openBot',
                      name=None,
                      description=None,
                      success_btn_bot=None,
                      success_btn_url=None,
                      success_text=None,
                      need_email=False,
                      expires_in=None):
        """
        Создайте новый счет на оплату.

        :param amount: сумма счета (float)
        :param product_list: массив JSON с товарами
        :param success_btn: openBot или openURL
        :param name: Название счета
        :param description: Описание счета
        :param success_btn_bot: Бот куда необходимо переслать пользователя после оплаты
        :param success_btn_url: Сайт куда необходимо переслать пользователя после оплаты
        :param success_text: Текст который будет выслан пользователю после успешной оплаты
        :param need_email: Передайте True если нужен email от пользователя
        :param expires_in: Время в секундах в течении которого будет действовать счет
        :return: Вернет объект Invoice
        """
        method = 'createInvoice'
        params = {"amount": amount, "product_list": product_list, "success_btn": success_btn, "name": name, "description": description,
                  "success_btn_bot": success_btn_bot, "success_btn_url": success_btn_url, "success_text": success_text, "need-email": need_email, "expires_in": expires_in}

        return send_request(self.request_url, 'createInvoice', params)


    def checkInvoice(self,
                     invoice_id):
        """
        Проверьте состояние счета.

        :param invoice_id: ID счета (будет в ответе на createInvoice, параметр 'invoice_id')
        :return: Вернет объект Invoice
        """

        method = 'checkInvoice'
        params = {"invoice_id": invoice_id}

        return send_request(self.request_url, method, params)

    def refundInvoice(self,
                      invoice_id):
        """
        Отмените оплаченный счет. Это вернет средства пользователя в полном объеме.

        :param invoice_id: ID счета (будет в ответе на createInvoice, параметр 'invoice_id')
        :return:
        """

        method = 'refundInvoice'
        params = {"invoice_id": invoice_id}

        return send_request(self.request_url, method, params)