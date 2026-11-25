"""Завдання 1. Однозв'язний список: реверсування, сортування злиттям, об'єднання двох відсортованих списків."""


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    @classmethod
    def from_iterable(cls, values):
        llist = cls()
        for value in values:
            llist.insert_at_end(value)
        return llist

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def __str__(self):
        return " -> ".join(str(x) for x in self.to_list()) or "(порожній)"

    # --- 1. Реверсування: змінюємо посилання next між вузлами ---
    def reverse(self):
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next   # запам'ятовуємо наступний вузол
            cur.next = prev  # розвертаємо посилання
            prev = cur
            cur = nxt
        self.head = prev

    # --- 2. Сортування злиттям (merge sort) для однозв'язного списку ---
    def sort(self):
        self.head = _merge_sort(self.head)


def _split(head):
    """Ділить список навпіл (повільний/швидкий вказівник). Повертає голову другої половини."""
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    middle = slow.next
    slow.next = None
    return middle


def _merge_nodes(a, b):
    """Зливає два відсортовані ланцюжки вузлів в один (без створення нових вузлів)."""
    dummy = Node()
    tail = dummy
    while a and b:
        if a.data <= b.data:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next


def _merge_sort(head):
    if head is None or head.next is None:
        return head
    middle = _split(head)
    left = _merge_sort(head)
    right = _merge_sort(middle)
    return _merge_nodes(left, right)


# --- 3. Об'єднання двох відсортованих списків в один відсортований ---
def merge_sorted_lists(list1, list2):
    """Повертає новий LinkedList. Вхідні списки мають бути відсортовані.
    Вузли переносяться (не копіюються), тому вхідні списки після виклику стають порожніми."""
    merged = LinkedList()
    merged.head = _merge_nodes(list1.head, list2.head)
    list1.head = None
    list2.head = None
    return merged


if __name__ == "__main__":
    llist = LinkedList.from_iterable([5, 1, 9, 3, 7, 2])
    print("Початковий список:     ", llist)

    llist.reverse()
    print("Після реверсування:    ", llist)
    assert llist.to_list() == [2, 7, 3, 9, 1, 5]

    llist.sort()
    print("Після сортування:      ", llist)
    assert llist.to_list() == [1, 2, 3, 5, 7, 9]

    a = LinkedList.from_iterable([1, 4, 6, 10])
    b = LinkedList.from_iterable([2, 3, 8, 11, 12])
    print("Список A:              ", a)
    print("Список B:              ", b)
    merged = merge_sorted_lists(a, b)
    print("Об'єднаний (A + B):    ", merged)
    assert merged.to_list() == [1, 2, 3, 4, 6, 8, 10, 11, 12]

    # граничні випадки
    empty = LinkedList()
    empty.reverse()
    empty.sort()
    assert empty.to_list() == []
    assert merge_sorted_lists(LinkedList(), LinkedList.from_iterable([1])).to_list() == [1]
    print("Усі перевірки пройдено.")
