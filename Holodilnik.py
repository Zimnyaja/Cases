from decimal import Decimal
from datetime import date, datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'

goods = {}  # сначала создаем пустой словарь
goods['Вода'] = [{'amount': Decimal('1.5'), 'expiration_date': None}]  # потом его наполняем
goods['Пельмени Универсальные'] = [{'amount': Decimal('0.5'), 'expiration_date': date(2023, 7, 15)},
                                   {'amount': Decimal('2'), 'expiration_date': date(2023, 8, 1)}]


def add(items, title, amount, expiration_date=None):  # функция добавляет данные в словарь
    if title in items:
        if not expiration_date:
            items[title].append({'amount': Decimal(amount), 'expiration_date': None})
        else:
            items[title].append({'amount': Decimal(amount),
                                 'expiration_date': datetime.date(datetime.strptime(expiration_date, DATE_FORMAT))})
    if title not in items:
        new_list = []
        if not expiration_date:
            new_list.append({'amount': Decimal(amount), 'expiration_date': None})
        else:
            new_list.append({'amount': Decimal(amount),
                             'expiration_date': datetime.date(datetime.strptime(expiration_date, DATE_FORMAT))})
        items[title] = new_list


add(goods, 'Шмода', 8, '2013-05-03')


def add_by_note(items, note):           # функция добавляет данные в словарь из заметки
    splited = str.split(note)
    if any([c == '-' for c in splited[-1]]):
        expiration_date = splited[-1]
        amount = Decimal(splited[-2])
        title_list = []
        for a in range(len(splited) - 2):
            title_list.append(splited[a])
        title = str.join(' ', title_list)
    else:
        expiration_date = None
        amount = Decimal(splited[-1])
        title_list = []
        for a in range(len(splited) - 1):
            title_list.append(splited[a])
        title = str.join(' ', title_list)
    add(items, title, amount, expiration_date)


add_by_note(goods, 'Яйца гусиные привозные 4.5 2024-07-15')
add_by_note(goods, 'Яйца гусиные 14')

print(goods)


def find(items, needle):  # ищет есть ли среди ключей словаря продукты с заданной фразой, выдает список продуктов
    find_list = []  # задаем пустой список, сюда будем складывать ключи, содержащие нужное
    for key in items:
        if str.find(key.lower(), needle.lower()) >= 0:
            find_list.append(key)
    return find_list


find(goods, 'ода')
find(goods, 'яй')


def amount(items, needle):  # выдает количество запрошенного продукта.
    product_amount = Decimal(str(0))
    for key in find(items, needle):
        value = items.get(key)
        for small_dict in value:
            product_amount += small_dict.get("amount")
    return product_amount


amount(goods, 'ю')
find(goods, 'яй')


def expire(items, in_advance_days=0):  # возвращает список просроченных продуктов.
    today = date.today()
    deadline = today + timedelta(in_advance_days)
    result = []
    for item in items:
        count = 0
        for list_1 in items[item]:
            if list_1['expiration_date'] is None:
                continue
            elif list_1['expiration_date'] <= deadline:
                count = count + list_1['amount']
        if count > 0:
            result.append((item, count))
    return result


expire(goods, -1)
