```markdown
# Документация для модуля в Loginom

## Введение

Этот модуль в Loginom предназначен для автоматизации процесса отправки электронных писем пользователям на основе данных из Excel таблиц. Модуль состоит из четырех сценариев, каждый из которых выполняет определенную задачу в общем процессе.

## Сценарии

### Сценарий 1: Чтение данных пользователей

Этот сценарий загружает данные пользователей из Excel таблицы. Таблица содержит следующие столбцы:

- **mail**: Электронная почта пользователя
- **user**: Имя пользователя

### Сценарий 2: Чтение сообщений

Этот сценарий загружает сообщения из другой Excel таблицы. Таблица содержит следующие столбцы:

- **SMS**: Текст сообщения

### Сценарий 3: Объединение таблиц

Этот сценарий объединяет таблицы из первых двух сценариев, создавая единую таблицу, содержащую информацию о пользователях и сообщениях.

### Сценарий 4: Отправка электронных писем

Этот сценарий содержит Python код, который отправляет электронные письма пользователям на основе объединенной таблицы.

## Python код

### Импорт библиотек
```python
import builtin_data
from builtin_data import InputTable, InputTables, InputVariables, OutputTable, DataType, DataKind, UsageType

import numpy as np
import pandas as pd
from builtin_pandas_utils import to_data_frame, prepare_compatible_table, fill_table

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
```
- **builtin_data**: Встроенная библиотека Loginom, которая позволяет работать с входными и выходными данными.
- **numpy (np)**: Библиотека для работы с массивами данных.
- **pandas (pd)**: Библиотека для работы с таблицами данных (DataFrame).
- **builtin_pandas_utils**: Вспомогательные функции для работы с pandas в Loginom.
- **smtplib**: Библиотека для отправки электронных писем.
- **email.mime.multipart и email.mime.text**: Библиотеки для создания и форматирования электронных писем.

### Функция отправки электронной почты
```python
def send_email(subject, body, to_email, from_email, app_password):
    # Создаем объект сообщения
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Добавляем тело письма
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Устанавливаем соединение с сервером
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Логинимся на сервере
        server.login(from_email, app_password)

        # Отправляем письмо
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        print(f'Email successfully sent to {to_email}')

    except Exception as e:
        print(f'Failed to send email to {to_email}: {e}')

    finally:
        # Закрываем соединение с сервером
        server.quit()
```
- **send_email**: Функция для отправки электронного письма.
- **subject**: Тема письма.
- **body**: Тело письма.
- **to_email**: Электронная почта получателя.
- **from_email**: Электронная почта отправителя.
- **app_password**: Пароль приложения для доступа к почтовому серверу.

### Основная функция
```python
def main():
    # Чтение входных данных
    input_frame = to_data_frame(InputTable)

    # Вывод первых нескольких строк DataFrame
    print("Первые несколько строк DataFrame:")
    print(input_frame.head())

    # Вывод названий столбцов
    print("Столбцы в DataFrame:", input_frame.columns)

    # Выбор письма для отправки
    for index, row in input_frame.iterrows():
        print(f"{index}: {row['SMS']}")

    choice = 0  # Выбор индекса сообщения

    if choice not in input_frame.index:
        print("Неверный выбор.")
        return

    selected_email = input_frame.loc[choice]
    subject = "Рассылка"  # Замените на вашу тему
    body = selected_email['SMS']
    from_email = "..."  # Введите вашу почту
    app_password = "..."  # Введите ваш пароль от почты

    # Создание DataFrame для выходных данных
    output_data = []

    # Отправка писем всем адресатам
    for index, row in input_frame.iterrows():
        to_email = row['mail']
        send_email(subject, body, to_email, from_email, app_password)
        output_data.append({'mail': to_email, 'Статус': 'Отправлено'})

    # Создание выходного DataFrame
    output_frame = pd.DataFrame(output_data)

    # Подготовка выходного набора данных
    if isinstance(OutputTable, builtin_data.ConfigurableOutputTableClass):
        prepare_compatible_table(OutputTable, output_frame, with_index=False)
    fill_table(OutputTable, output_frame, with_index=False)

if __name__ == "__main__":
    main()
```
- **main**: Основная функция, которая выполняет основную логику модуля.
- **to_data_frame(InputTable)**: Преобразует входные данные в DataFrame.
- **input_frame.head()**: Выводит первые несколько строк DataFrame.
- **input_frame.columns**: Выводит названия столбцов DataFrame.
- **input_frame.iterrows()**: Итерирует по строкам DataFrame.
- **choice**: Индекс выбранного сообщения.
- **selected_email**: Выбранное сообщение.
- **output_data**: Список для хранения данных о статусе отправки писем.

## Описание работы модуля

1. **Чтение данных**: Модуль считывает данные из двух Excel таблиц, содержащих информацию о пользователях и сообщениях.
2. **Объединение таблиц**: Данные из двух таблиц объединяются в одну.
3. **Отправка электронных писем**: На основе объединенной таблицы формируются электронные письма, которые отправляются пользователям.

## Заключение

Этот модуль автоматизирует процесс отправки электронных писем пользователям, используя данные из Excel таблиц. Он включает в себя чтение данных, их объединение и отправку писем с помощью Python кода.
```