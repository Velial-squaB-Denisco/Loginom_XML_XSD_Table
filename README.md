# XML Parser to Excel/CSV Converter

Утилита для преобразования XML-файлов в структурированные таблицы Excel/CSV с сохранением иерархии данных и атрибутов.

## Особенности

- 🚀 Автоматическое определение структуры XML
- 📌 Сохранение вложенных элементов и атрибутов
- 💾 Экспорт в:
  - Microsoft Excel (.xlsx)
  - CSV-файлы (.csv)
- 🔍 Рекурсивный парсинг многоуровневых структур
- 🛠 Автоматическое форматирование имен столбцов

## Требования

- Python 3.7+
- Установленные пакеты:
  ```bash
  pip install pandas lxml xmltoxsd openpyxl

## Использование

1. Поместите XML-файл в корневую директорию (по умолчанию `input.xml`)
2. Запустите скрипт:
   ```bash
   python xml_parser.py
   ```
3. Результаты будут сохранены в:
   - `xml_data.xlsx` - Excel-файл
   - `xml_data.csv` - CSV-файл

## Пример XML-файла

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
  <book id="101">
    <title lang="en">The Great Adventure</title>
    <author>John Smith</author>
    <price currency="USD">24.99</price>
    <categories>
      <category>Fiction</category>
      <category>Adventure</category>
    </categories>
  </book>
</bookstore>
```

## Пример выходных данных

### Структура CSV:
```csv
book@id,title@lang,title,author,price@currency,price,categories_category,categories_category_1
101,en,The Great Adventure,John Smith,USD,24.99,Fiction,Adventure
```

### Особенности именования:
- `element@attribute` - атрибуты элементов
- `parent_child` - вложенные элементы
- `element_N` - повторяющиеся элементы

## Лицензия

Этот проект распространяется под лицензией [MIT](LICENSE).

---

**Автор**: [Ваше имя]  
**Версия**: 1.0.0  
**Дата**: 2023-10-15
```

Для использования:
1. Замените `yourusername` в ссылке для клонирования
2. Добавьте информацию об авторе
3. При необходимости отредактируйте раздел лицензии
4. Сохраните как `README.md` в корне проекта

Документация включает:
- Badges для быстрого понимания статуса
- Четкие инструкции по установке и использованию
- Примеры входных/выходных данных
- Описание системы именования столбцов
- Информацию о лицензии и авторе
