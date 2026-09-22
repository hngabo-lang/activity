import unittest
from stack_queue import Stack, Queue


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(len(self.stack), 0)

    def test_push_adds_item(self):
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)

    def test_push_multiple_items(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.size(), 3)

    def test_pop_returns_last_pushed_item(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_stack_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_does_not_remove_item(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.size(), 2)

    def test_peek_empty_stack_raises(self):
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_lifo_order_with_many_items(self):
        for i in range(100):
            self.stack.push(i)
        for i in reversed(range(100)):
            self.assertEqual(self.stack.pop(), i)

    def test_mixed_push_and_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())

    def test_repr(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(repr(self.stack), "Stack([1, 2])")


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()

    def test_new_queue_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(len(self.queue), 0)

    def test_enqueue_adds_item(self):
        self.queue.enqueue(1)
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 1)

    def test_enqueue_multiple_items(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.size(), 3)

    def test_dequeue_returns_first_enqueued_item(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_empty_queue_raises(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    def test_peek_does_not_remove_item(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.peek(), 10)
        self.assertEqual(self.queue.size(), 2)

    def test_peek_empty_queue_raises(self):
        with self.assertRaises(IndexError):
            self.queue.peek()

    def test_fifo_order_with_many_items(self):
        for i in range(100):
            self.queue.enqueue(i)
        for i in range(100):
            self.assertEqual(self.queue.dequeue(), i)

    def test_mixed_enqueue_and_dequeue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertTrue(self.queue.is_empty())

    def test_repr(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(repr(self.queue), "Queue([1, 2])")


if __name__ == '__main__':
    unittest.main()