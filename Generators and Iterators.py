nested_list = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f', 'h', False],
    [1, 2, None],
]

multi_nesting = ['lvl_0', 'lvl_0',
                 ['lvl1', 'lvl1', [['lvl3', 'lvl3'], 'lvl2', ['lvl3', 'lvl3', ['lvl4', 'lvl4', 'and so on']]]]]


class FlatList:

    def __init__(self, nested_list):
        self.nested_list = nested_list

    def __iter__(self):
        self.cursor = -1
        self.data_list = []
        return self

    def __next__(self):
        self.cursor += 1
        if len(self.nested_list) <= self.cursor:
            if len(self.data_list) == self.cursor:
                raise StopIteration
        else:
            self.data_list += nested_list[self.cursor]
        return self.data_list[self.cursor]


print('Итератор: варинат 1')
comprehension = [comprehension for comprehension in FlatList(nested_list)]
print(comprehension)
for items in FlatList(nested_list):
    print(items)

print('-------')


class Iteratorlist:

    def __init__(self, nested_list):
        self.nested_list = nested_list

    def __iter__(self):
        self.cursor = 0
        self.cursor_l2 = -1
        return self

    def __next__(self):
        self.cursor_l2 += 1
        if len(self.nested_list[self.cursor]) == self.cursor_l2:
            self.cursor += 1
            self.cursor_l2 = 0
            if len(self.nested_list) == self.cursor:
                raise StopIteration
        return self.nested_list[self.cursor][self.cursor_l2]


print('Итератор: варинат 2')
comprehension2 = [comprehension for comprehension in Iteratorlist(nested_list)]
print(comprehension2)
for i in Iteratorlist(nested_list):
    print(i)

print('---------')


class InfiniteNesting:

    def __init__(self, nested_list):
        self.nested_list = nested_list

    def __iter__(self):
        self.data_list = []
        self.temp_list = self.nested_list
        return self

    def __next__(self):
        if not self.temp_list:
            raise StopIteration
        else:
            if type(self.temp_list[0]) is not list:
                self.data_list.append(self.temp_list[0])
                self.temp_list.pop(0)
            else:
                self.temp_list.extend(self.temp_list[0])
                self.temp_list.pop(0)

        return self.data_list[-1]


print('Итератор: варинат c ꝏ вложенностью(type-list) ')
for items in InfiniteNesting(multi_nesting):
    print(items)


def generator_item(data_list):
    for items in data_list:
        for item in items:
            yield item


comprehension3 = [comprehension for comprehension in generator_item(nested_list)]
print('Генератор')
print(comprehension3)

print('---------')


def infinite_nesting(a_list):
    for items in a_list:
        if type(items) is not list:
            yield items
        else:
            for item in infinite_nesting(items):
                yield item


comprehension4 = [comprehension for comprehension in infinite_nesting(multi_nesting)]
print('Генератор с ꝏ вложенностью(type-list) ')
print(comprehension4)
