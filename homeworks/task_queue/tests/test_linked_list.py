from unittest import TestCase

from server import LinkedListNode, LinkedList


class LinkedListBaseTest(TestCase):
    def test_add(self):
        a = LinkedListNode("a")
        b = LinkedListNode("b")
        c = LinkedListNode("c")

        l = LinkedList()

        self.assertIsNone(l.head_node)
        self.assertIsNone(l.tail_node)

        l.add(a)

        self.assertEqual(l.head_node, a)
        self.assertEqual(l.tail_node, a)
        self.assertIsNone(a.prev)
        self.assertIsNone(a.next)

        l.add(b)

        self.assertEqual(l.head_node, a)
        self.assertEqual(l.tail_node, b)
        self.assertIsNone(a.prev)
        self.assertEqual(a.next, b)
        self.assertEqual(b.prev, a)
        self.assertIsNone(b.next)

        l.add(c)
        self.assertEqual(l.head_node, a)
        self.assertIsNone(a.prev)
        self.assertEqual(a.next, b)
        self.assertEqual(b.prev, a)
        self.assertEqual(b.next, c)
        self.assertEqual(c.prev, b)
        self.assertIsNone(c.next)

    def test_iter(self):
        a = LinkedListNode("a")
        b = LinkedListNode("b")
        c = LinkedListNode("c")

        l = LinkedList()

        l.add(a)
        l.add(b)
        l.add(c)

        iterator = iter(l)
        self.assertEqual(next(iterator), a)
        self.assertEqual(next(iterator), b)
        self.assertEqual(next(iterator), c)
        # self.assertIsNone(next(iterator))

        iterator = iter(l)
        self.assertEqual(next(iterator), a)
        self.assertEqual(next(iterator), b)
        self.assertEqual(next(iterator), c)
        # self.assertIsNone(next(iterator))

        c = 0
        for node in l:
            c += 1
        self.assertEqual(c, 3)

    def test_delete(self):
        a = LinkedListNode("a")
        b = LinkedListNode("b")
        c = LinkedListNode("c")
        d = LinkedListNode("d")
        e = LinkedListNode("e")

        l = LinkedList()
        l.add(a)
        l.add(b)
        l.add(c)
        l.add(d)
        l.add(e)

        l.delete(c)
        l.delete(a)
        l.delete(e)

        self.assertEqual(l.head_node, b)
        self.assertEqual(l.head_node.next, d)
        self.assertIsNone(b.prev)
        self.assertEqual(b.next, d)
        self.assertEqual(d.prev, b)
        self.assertIsNone(d.next)
