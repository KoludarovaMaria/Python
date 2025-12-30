class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()

    def __next__(self):
        while True:
            item = next(self.items)

            if self.ignore_case and isinstance(item, str):
                check_item = item.lower()
            else:
                check_item = item

            if check_item not in self.seen:
                self.seen.add(check_item)
                return item

    def __iter__(self):
        return self


if __name__ == "__main__":
    print("Тест 1 - числа:")
    data = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    for item in Unique(data):
        print(item)

    print("\nТест 2 - строки без ignore_case:")
    data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    for item in Unique(data):
        print(item)

    print("\nТест 3 - строки с ignore_case=True:")
    for item in Unique(data, ignore_case=True):
        print(item)

    print("\nТест 4 - с генератором:")
    from gen_random import gen_random

    data = gen_random(10, 1, 3)
    for item in Unique(data):
        print(item)
