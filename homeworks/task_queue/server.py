import argparse
import socketserver
import re
from parse import parse
import datetime
import pickle


DUMP_FILENAME = "dump.txt"


RE_ADD = "^ADD \w+ \d+ .+$"
PATTERN_ADD = "ADD {} {} {}"

RE_GET = "^GET \w+$"
PATTERN_GET = "GET {}"

RE_ACK = "^ACK \w+ \w{1,128}$"
PATTERN_ACK = "ACK {} {}"

RE_IN = "^IN \w+ \w{1,128}$"
PATTERN_IN = "IN {} {}"

RE_SAVE = "^SAVE$"


class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class Task(LinkedListNode):
    def __init__(self, task_data, task_id):
        super().__init__(task_data)
        self.task_id = task_id
        self.last_time_taken = datetime.datetime.min

    def __str__(self):
        return f"{self.task_id} {len(self.data)} {self.data}"


class LinkedList:
    head_node: LinkedListNode

    def __init__(self):
        self.head_node = None
        self.tail_node = None
        self.__next_iter_node = None

    def __iter__(self):
        self.__next_iter_node = self.head_node
        return self

    def __next__(self):
        ret = self.__next_iter_node
        if self.__next_iter_node is not None:
            self.__next_iter_node = ret.next
        else:
            raise StopIteration
        return ret

    def add(self, node: LinkedListNode):
        if self.head_node is None:
            self.head_node = node
            self.tail_node = node
        else:
            self.tail_node.next = node
            node.prev = self.tail_node
            self.tail_node = node

    def delete(self, node: LinkedListNode, check=False):
        if check:
            if not self.has(node):
                raise KeyError
        if node is self.head_node:
            self.head_node = node.next
        if node is self.tail_node:
            self.tail_node = node.prev
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev

    def has(self, node):
        for list_node in self:
            if list_node is node:
                return True
        return False


class TaskQueue:
    def __init__(self, name, timeout):
        self.storage = LinkedList()
        self._last_id = 0
        self._name = name
        self.last_task = None
        self.timeout = timeout

    def _generate_id(self):
        self._last_id = self._last_id + 1
        return self._last_id

    def add(self, task_data):
        task_id = self._generate_id()
        self.storage.add(Task(task_data, task_id))
        return str(task_id)

    def get(self):
        for task in self.storage:
            if datetime.datetime.now() - task.last_time_taken > self.timeout:
                task.last_time_taken = datetime.datetime.now()
                return str(task)
        return None

    def acknowledge(self, task_id):
        for task in self.storage:
            if task.task_id == int(task_id):
                if datetime.datetime.now() - task.last_time_taken < self.timeout:
                    self.storage.delete(task)
                    return "YES"
                else:
                    return "NO"
        return "NO"

    def has(self, task_id):
        for task in self.storage:
            if task.task_id == int(task_id):
                return "YES"
        return "NO"


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1000000).strip()
        response = server.parse_command(data)
        if response is not None:
            self.request.sendall(bytes(response, "utf-8"))


class TaskQueueServer:
    def __init__(self, ip, port, path, timeout):
        self.ip = ip
        self.port = port
        self.path = path
        self.timeout = datetime.timedelta(seconds=timeout)
        try:
            self.load(path)
        except IOError:
            self.queues = {}

    def get_queue(self, name, create=True):
        if name not in self.queues:
            if create:
                self.queues[name] = TaskQueue(name, self.timeout)
            else:
                return None
        return self.queues[name]

    def parse_command(self, text):
        text = text.decode("utf-8").strip()
        if re.match(RE_SAVE, text):
            self.save(self.path)
        elif re.match(RE_ADD, text):
            queue_name, length, data = parse(PATTERN_ADD, text)
            queue = self.get_queue(queue_name)
            assert int(length) == len(data)
            return queue.add(data)
        elif re.match(RE_GET, text):
            queue_name = parse(PATTERN_GET, text)[0]
            queue = self.get_queue(queue_name, create=False)
            return queue.get()
        elif re.match(RE_ACK, text):
            queue_name, task_id = parse(PATTERN_ACK, text)
            queue = self.get_queue(queue_name, create=False)
            return queue.acknowledge(task_id)
        elif re.match(RE_IN, text):
            queue_name, task_id = parse(PATTERN_IN, text)
            queue = self.get_queue(queue_name)
            return queue.has(task_id)
        else:
            return "ERROR"

    def save(self, path):
        dump = pickle.dumps(self.queues)
        with open(path + DUMP_FILENAME, 'wb') as f:
            f.write(dump)

    def load(self, path):
        with open(path + DUMP_FILENAME, 'rb') as f:
            dump = f.read()
        self.queues = pickle.loads(dump)

    def run(self):
        with socketserver.TCPServer((self.ip, self.port), MyTCPHandler) as my_server:
            my_server.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip address')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
