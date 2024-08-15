import xml.etree.ElementTree as ET

# 解析XML文件
tree = ET.parse('example.xml')
root = tree.getroot()

# 输出根元素的标签
print(f"根元素: {root.tag}")

# 遍历所有的Book元素
for book in root.findall('Book'):
    book_id = book.get('ID')
    title = book.find('Title').text
    author = book.find('Author').text
    year = book.find('Year').text
    genre = book.find('Genre').text

    print(f"书籍 ID: {book_id}, 标题: {title}, 作者: {author}, 年份: {year}, 类型: {genre}")
