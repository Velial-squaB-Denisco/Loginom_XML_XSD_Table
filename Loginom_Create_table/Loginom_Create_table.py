import builtin_data
from builtin_data import InputTable, InputTables, InputVariables, OutputTable, DataType, DataKind, UsageType

import psycopg2
import xml.etree.ElementTree as ET
import pandas as pd
import builtin_data
import os
import requests
from builtin_pandas_utils import prepare_compatible_table, fill_table

def main():
    xml = SQL()
    if xml:
        xsd = XSDcre(xml)
        if xsd:
            table(xsd, xml)
    
def SQL(): # Заполните поля для подключения к БД
    db_params = {
        'dbname': "...",
        'user': "...",
        'password': "...",
        'host': "...",
        'port': "..."
    }

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        cursor.execute("SELECT x.* FROM yortable") # Изменить на свой SQL запрос
        rows = cursor.fetchone()

    except Exception as error:
        print(f"Error: {error}")
        rows = None

    finally:
        if connection:
            cursor.close()
            connection.close()

    return rows[0]

def XSDcre(xml):
    xml_data = xml

    # Парсинг XML данных
    root = ET.fromstring(xml_data)

    # Создание базового XSD
    xsd_elements = []

    def add_element(element, parent_name=None):
        element_name = element.tag
        element_type = f"{parent_name}_{element_name}" if parent_name else element_name
        xsd_elements.append(f'<xs:element name="{element_name}" type="{element_type}"/>')
        complex_type = [f'<xs:complexType name="{element_type}">', f'<xs:sequence>']
        for child in element:
            add_element(child, element_type)
        complex_type.append('</xs:sequence></xs:complexType>')
        xsd_elements.extend(complex_type)

    add_element(root)

    # Создание полного XSD
    xsd_data = f'''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
{''.join(xsd_elements)}
</xs:schema>'''

    return xsd_data

def table(xsd, xml):
    xsd_data = xsd
    xml_data = xml

    # Парсинг XSD
    xsd_root = ET.fromstring(xsd_data)

    # Парсинг XML
    xml_root = ET.fromstring(xml_data)

    # Пространства имен
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
        'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'
    }

    # Заголовки таблицы
    headers = []
    for element in xsd_root.iter():
        if 'name' in element.attrib and element.attrib['name'] not in headers:
            headers.append(element.attrib['name'])

    # Данные таблицы
    data = []
    for item in xml_root.findall('.//atom:entry', namespaces):
        row = []
        for header in headers:
            # Удаляем пространства имен из заголовков
            header_without_ns = header.split('}')[-1]
            element = item.find(f'.//d:{header_without_ns}', namespaces)
            row.append(element.text if element is not None else '')
        data.append(row)

    upload_url = 'output.xlsx' # Ваш путь в Loginom server
    

    # Создание DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Сохранение DataFrame в Excel файл
    filename = 'output.xlsx'
    df.to_excel(filename, index=False)

    # Загрузка файла на веб-сервер
    with open(filename, 'rb') as file:
        response = requests.put(upload_url, files={'file': file})

    if response.status_code == 200:
        print('Файл успешно загружен на сервер.')
    else:
        print(f'Ошибка при загрузке файла: {response.status_code}')
'''

from builtin_pandas_utils import to_data_frame, prepare_compatible_table, fill_table

# Входной порт необязательный
if InputTable:
    # Создать pd.DataFrame по входному набору №1
    input_frame = to_data_frame(InputTable)

# Здесь может быть код работы с данными

# Полученный выходной pd.DataFrame
output_frame = pd.DataFrame({"COL1": [1, 2], "COL2": ["a", "b"], "COL3": [np.datetime64("2020"), np.datetime64("nat")]})

# Если включена опция "Разрешить формировать выходные столбцы из кода", структуру выходного набора можно подготовить по pd.DataFrame
if isinstance(OutputTable, builtin_data.ConfigurableOutputTableClass):
    prepare_compatible_table(OutputTable, output_frame, with_index=False)
fill_table(OutputTable, output_frame, with_index=False)
'''

if __name__ == "__main__":
    main()