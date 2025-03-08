from lxml import etree
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from xmltoxsd import XSDGenerator  # Убедитесь, что этот модуль установлен и доступен

def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def format_xml_file(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    pretty_xml = prettify_xml(root)
    return pretty_xml  # Возвращаем отформатированную строку XML

input_xml_file = 'input.xml'

# Форматируем XML и выводим его
formatted_xml = format_xml_file(input_xml_file)

# Генерируем XSD схему
generator = XSDGenerator()
xsd_schema = generator.generate_xsd(input_xml_file)  # Предположим, что это строка

def remove_duplicates(xsd_string):
    # Преобразуем строку XSD в XML-дерево
    xsd_tree = etree.fromstring(xsd_string.encode('utf-8'))
    root = xsd_tree

    # Словарь для хранения уникальных элементов
    unique_elements = {}
    for elem in root.findall(".//{http://www.w3.org/2001/XMLSchema}element"):
        name = elem.get('name')
        if name not in unique_elements:
            unique_elements[name] = elem
        else:
            # Удаляем повтор - используем родительский элемент для удаления
            elem.getparent().remove(elem)

    # Возвращаем измененное дерево в виде строки
    return etree.tostring(root, pretty_print=True, encoding='unicode')

# Удаляем дубликаты
cleaned_xsd = remove_duplicates(xsd_schema)
print(cleaned_xsd)