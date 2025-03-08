import xml.etree.ElementTree as ET
import pandas as pd
import xml.dom.minidom as minidom
from io import BytesIO

def process_xml_data(input_file):
    # ======== 1. Форматирование XML в памяти ========
    def prettify_xml(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        return minidom.parseString(rough_string).toprettyxml(indent="  ")

    tree = ET.parse(input_file)
    formatted_xml = prettify_xml(tree.getroot())

    # ======== 2. Парсинг XML данных ========
    def parse_node(node, path=''):
        data = {}
        tag = node.tag.split('}')[-1]
        current_path = f"{path}{tag}_" if path else f"{tag}_"
        
        # Атрибуты
        for attr, value in node.attrib.items():
            data[f"{current_path[:-1]}@{attr}"] = value
            
        # Дочерние элементы
        if len(node) > 0:
            for child in node:
                data.update(parse_node(child, current_path))
        else:
            data[current_path[:-1]] = node.text.strip() if node.text else None
        return data

    xml_data = []
    try:
        root = ET.parse(BytesIO(formatted_xml.encode())).getroot()
        for item in root:
            xml_data.append(parse_node(item))
    except Exception as e:
        print(f"XML parsing failed: {e}")
        return []

    # ======== 3. Сохранение результатов ========
    final_files = []
    
    if xml_data:
        df = pd.DataFrame(xml_data)
        df.to_excel('xml_data.xlsx', index=False)
        df.to_csv('xml_data.csv', index=False)
        final_files.extend(['xml_data.xlsx', 'xml_data.csv'])

    return final_files

# Запуск обработки
result_files = process_xml_data('input.xml')
print(f"Created files: {', '.join(result_files)}")