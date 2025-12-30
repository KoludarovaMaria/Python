def field(items, *args):
    assert len(args) > 0

    if len(args) == 1:
        key = args[0]
        for item in items:
            if key in item and item[key] is not None:
                yield item[key]
    else:
        for item in items:
            result = {}
            has_values = False
            for key in args:
                if key in item and item[key] is not None:
                    result[key] = item[key]
                    has_values = True
            if has_values:
                yield result


if __name__ == "__main__":
    # Тестовые данные
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'},
        {'title': None, 'price': 5000},
        {'color': 'blue'}
    ]

    print("Тест 1 - один аргумент:")
    for item in field(goods, 'title'):
        print(f"'{item}'")

    print("\nТест 2 - несколько аргументов:")
    for item in field(goods, 'title', 'price'):
        print(item)
