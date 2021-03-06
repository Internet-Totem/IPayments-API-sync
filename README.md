# IPayments API (синхронный)


Пример Telegram бота для взамодействия с [IPayments API](https://telegra.ph/IPayments-API-02-09).

## Введение

Пример полностью готового и рабочего Telegram бота работающего на синхронном коде (pyTelegramBotAPI) для взаимодействия с IPayments API (создание, оплата и отмена счетов).

### Асинхронный код

Точно такой же пример, но написанный на асинхронном коде (pyTelegramBotAPI -> **aiogram**; requests -> **aiohttp**) можно посмотреть [здесь](https://github.com/Internet-Totem/IPayments-API-async).


## Начало работы

Для того, чтобы использовать создайте своего Telegram бота и приложение в IPayments (подробно о том, как создать приложение [написано здесь](https://telegra.ph/Lets-Start-02-17)).
После получения токенов вставьте их в соответствующие поля в main.py.

### Необходимые библиотеки

- pyTelegramBotAPI
- requests


### Запуск

```
python3 main.py
```

## Где посмотреть код в действии

Помимо того, что вы можете запустить этот код у себя, вы можете посмотреть как он работает в нашем [Demo Shop](http://t.me/IPayments_demoshop_bot).

> Все средства потраченные в Demo Shop будут обратно зачислены на баланс в IPayments


## Заключение

Это простой бот, в котором можно посмотреть как работают основные методы [IPayments API](https://telegra.ph/IPayments-API-02-09).
