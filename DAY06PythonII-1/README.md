# DAY 06 – Telegram-бот
## Командный проект

Сегодня мы будем писать телеграм-бота, который взаимодействует с базой данных.

## Оглавление

1. [Глава I](#глава-i) \
    1.1. [Преамбула](#преамбула)
2. [Глава II](#глава-ii) \
    2.1. [Общая инструкция](#общая-инструкция)
3. [Глава III](#глава-iii) \
    3.1. [Цели](#цели)
4. [Глава IV](#глава-iv) \
    4.1. [Задание](#задание)
5. [Глава V](#глава-v) \
    5.1. [Сдача работы и проверка](#сдача-работы-и-проверка)

## Глава I
### Преамбула

Допустим, мы хотим организовать книжную полку у себя в университете, куда можно будет добавлять книги, брать их почитать и возвращать. И нам хочется иметь базу данных этих книг, чтобы понимать, что сейчас происходит с нашими книгами. Поскольку пользоваться напрямую базой неудобно, обернем ее в телеграм-бот, где каждый пользователь сможет сделать отметку о том, что он взял книгу, вернул ее или принес новую. Проект будет состоять из трех частей: сервер, сам бот и модуль для работы с СУБД.


## Глава II
### Общая инструкция

Методология Школы 21 может быть не похожа на тот образовательный опыт, который с вами случался ранее. Ее отличает высокий уровень автономии: у вас есть задача, вы должны ее выполнить. По большей части вам нужно будет самим добывать знания для ее решения. Второй важный момент – это peer-to-peer обучение. В образовательном процессе нет преподавателей и экспертов, перед которыми вы защищаете свой результат. Вы это делаете перед таким же учащимися, как и вы сами. У них есть чек-лист, который поможет им выполнить приемку вашей работы качественно.

Роль Школы 21 заключается в том, чтобы обеспечить через последовательность заданий и оптимальный уровень поддержки такую траекторию обучения, при которой вы освоите не только hard skills, но и научитесь самообучаться.

* Не доверяйте слухам и предположениям о том, как должно быть оформлено ваше решение. Этот документ является единственным источником, к которому стоит обращаться по большинству вопросов.
* Ваше решение будет оцениваться другими учащимися бассейна.
* Подлежат оцениванию только те файлы, которые вы выложили в GIT.
* В вашей папке не должно быть лишних файлов – только те, что были указаны в задании.
* Есть вопрос? Спросите коллегу справа. Не помогло? Спросите коллегу слева.
* Не забывайте, что у вас есть доступ к интернету и поисковым системам.
* Обсуждение заданий можно вести и в Slack бассейна.
* Будьте внимательные к примерам, указанным в этом документе – они могут иметь важные детали, которые не были оговорены другим способом.
* И да пребудет с вами Сила!

Примечание. В папке src хранятся блокноты с конспектами и заданиями. В некоторых из них используются картинки, и чтобы они отображались, в той же папке лежат папки с ними, которые вам нет необходимости просматривать.



## Глава III
### Цели

Наша цель - научиться подключать СУБД к реальному проекту.

## Глава IV
### Задание

Требуется описать код проекта в соответствии с ТЗ, приведенным в блокноте src/TelegramBot.ipynb. Должна быть соблюдена структура проекта:

1. telegram.py - файл, где описана логика взаимодействия с телеграмом
2. app.py - файл, где разворачивается сервер, который выдает файлы со статистикой использования книг
3. database/models.py - файл с описанием моделей Book и Borrow, которые используются для хранения данных о книгах
4. database/dbapi.py - файл с функциями, позволяющими подключаться и работать с моделями данных и СУБД

Также требуется создать базу данных (или схему) в postgres, состоящую из двух таблиц Books и Borrows, с которой будет взаимодействовать бот.

## Глава V
### Сдача работы и проверка

Вам нужно загрузить все файлы с кодом проекта в репозиторий в папку src. Также загрузите файл с кодом создания таблиц (это может быть питоновский скрипт с созданием структуры БД через sqlalchemy, а может быть скрипт SQL).

>Пожалуйста, оставьте обратную связь по проекту в [форме обратной связи.](https://forms.gle/s5Sv9wQwaUYiLbwr6) 
