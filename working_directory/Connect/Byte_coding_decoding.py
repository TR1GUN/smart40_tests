# В этом файле производится кодировка - декодировка нужной нам сущности в байт-код
# Решил вынести в отдельный скрипт. ХЗ зачем, но почему бы и нет
import re
# Перевод в байт код
def to_bytes(content):
    """
    Перевод в байт код
    :param content: что надо переводить
    :return: возвращает байт код
    """
    content = str(content)
    content_bytes = bytes(content, 'utf-8')
    return content_bytes


# Перевод из байткода
def from_bytes(content_bytes):
    """
    Перевод из байт кода
    :param content_bytes: что надо переводить
    :return: вовращает сам перевод в utf-8
    """
    content = content_bytes.decode('utf-8')
    # content_final = re.sub( r'$', '', content)
    # content_index = content.find('{')
    # if content_index == 0:
    #     content_index = 1
    # content_final = content[content_index-1:]
    # 'SQL error:(.+)$ '

    return content

