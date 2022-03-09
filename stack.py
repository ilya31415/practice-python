class Stack:

    def __init__(self):
        self.items_box = []

    def isEmpty(self):
        """Проверка стека на пустоту.Метод возвращает True или False."""
        if len(self.items_box) == 0:
            return True
        else:
            return False

    def push(self, item):
        """Добавляет новый элемент на вершину стека.
        Метод ничего не возвращает."""
        self.items_box.append(item)

    def pop(self):
        """Удаляет верхний элемент стека.
        Стек изменяется.
        Метод возвращает верхний элемент стека"""
        return self.items_box.pop()

    def peek(self):
        """возвращает верхний элемент стека, но не удаляет его.
        Стек не меняется."""
        return self.items_box[-1]

    def size(self):
        """Возвращает количество элементов в стеке."""
        return len(self.items_box)


if __name__ == '__main__':
    not_balance = "{{[(])]}}"
    balance = "[([])((([[[]]])))]{()}"

    stek_1 = Stack()


    def balance_or_not(bracket: str):
        for item in bracket:
            if item in "({[":
                stek_1.push(item)
            elif item in ")}]":
                if stek_1.isEmpty() == True:
                    return print("Несбалансированно")
                else:
                    item_pop = stek_1.pop()
                    if item_pop == '(' and item == ')':
                        continue
                    if item_pop == '{' and item == '}':
                        continue
                    if item_pop == '[' and item == ']':
                        continue
                    return print("Несбалансированно")
        if stek_1.isEmpty() == True:
            return print("Cбалансированно")
        else:
            return print("Несбалансированно")


    balance_or_not(balance)
    balance_or_not(not_balance)