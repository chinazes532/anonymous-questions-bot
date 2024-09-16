# anonymous-questions-bot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

<h1>Описание бота</h1>

Данный чат-бот позволяет отправить анонимное сообщение пользователю при помощи реферальной ссылки.
Ссылка шифруется при помощи <a href="https://docs.aiogram.dev/en/latest/utils/deep_linking.html" target=_blank>aiogram.utils.deep_linking</a><br>
При отправке сообщения бот проверяет заблокировал ли его пользователь.

Также есть возможность предложить идею при помощи команды <code>/issue Тест...</code>
Сообщение с предложением отправляется администратору.

<h1>Установка и запуск</h1>
<ol>
    <li>Python 3.9 и выше</li>
    <li>Выбрать в главном меню "Get from VCS" и вставить данную ссылку: <code>https://github.com/chinazes532/anonymous-questions-bot.git</code></li>
    <li>Установить нужные зависиомсти, при помощи: <code>pip install -r requirements.txt</code></li>
    <li>Запустите скрипт при помощи <code>python3 main.py</code></li>
</ol>
