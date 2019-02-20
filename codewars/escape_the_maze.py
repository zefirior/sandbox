from enum import Enum

# +-----------> x
# |
# |
# |
# v y


class Direct(Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"

    @classmethod
    def directs(cls):
        for direct in cls.__members__.values():
            yield direct.value


class Command(Enum):
    FORWARD = "F"
    LEFT = "L"
    RIGHT = "R"
    BACK = "B"


class Node:
    def __init__(self, x, y):
        self.color = False
        self.x = x
        self.y = y
        self.neibors = []

    def __repr__(self):
        return "<{self.__class__.__name__} x={self.x}, y={self.y}>".format(self=self)

    def add_neibor(self, node):
        self.neibors.append(node)


class Exit(Node):
    pass


class Start(Node):
    def __init__(self, x, y, marker):
        for direct in Direct.__members__.values():
            if marker == direct.value:
                self.direct = direct

        self.marker = marker
        super().__init__(x, y)


class Graph:
    def __init__(self):
        self.start = None
        self.nodes = {}

    def add_node(self, node: Node):
        if isinstance(node, Start):
            self.start = node
        self.nodes[(node.x, node.y)] = node

    def fill_node(self, data):
        size_x, size_y = len(data[0]), len(data)
        for y, row in enumerate(data):
            for x, ch in enumerate(row):
                if (y in (0, size_y - 1) or x in (0, size_x - 1)) and ch == " ":
                    self.add_node(Exit(x, y))
                elif ch == " ":
                    self.add_node(Node(x, y))
                elif ch in Direct.directs():
                    self.add_node(Start(x, y, ch))
        return self

    def fill_neibor(self):
        """For each node find down node and right node, then link self and found nodes."""
        for node in self.nodes.values():
            for coord in ((node.x + 1, node.y), (node.x, node.y + 1)):
                neibor = self.nodes.get(coord)
                if neibor:
                    neibor.add_neibor(node)
                    node.add_neibor(neibor)
        return self


def dfs(stack: list, node: Node):
    if node.color:
        return False

    node.color = True
    stack.append(node)
    if isinstance(node, Exit):
        return True

    for neibor in node.neibors:
        if dfs(stack, neibor):
            return True

    stack.pop()
    return False


class PathBuilder:
    rotate_map = {
        (Direct.LEFT, Direct.UP): Command.RIGHT,
        (Direct.LEFT, Direct.RIGHT): Command.BACK,
        (Direct.LEFT, Direct.DOWN): Command.LEFT,

        (Direct.UP, Direct.RIGHT): Command.RIGHT,
        (Direct.UP, Direct.DOWN): Command.BACK,
        (Direct.UP, Direct.LEFT): Command.LEFT,

        (Direct.RIGHT, Direct.DOWN): Command.RIGHT,
        (Direct.RIGHT, Direct.LEFT): Command.BACK,
        (Direct.RIGHT, Direct.UP): Command.LEFT,

        (Direct.DOWN, Direct.LEFT): Command.RIGHT,
        (Direct.DOWN, Direct.UP): Command.BACK,
        (Direct.DOWN, Direct.RIGHT): Command.LEFT,
    }

    def __init__(self, start):
        self.start = start
        self.nodes = []
        self.commands = []

    def build(self):
        if not self.nodes:
            return

        current_direct = self.start.direct
        for start, finish in zip(self.nodes[:-1], self.nodes[1:]):
            next_direct = self.direct_from_node(start, finish)
            rotate = self.rotate(current_direct, next_direct)
            if rotate:
                self.commands.append(rotate)
            self.commands.append(Command.FORWARD)
            current_direct = next_direct

    @staticmethod
    def direct_from_node(start: Node, finish: Node):
        if start.x != finish.x:
            return [Direct.LEFT, Direct.RIGHT][start.x < finish.x]
        elif start.y != finish.y:
            return [Direct.UP, Direct.DOWN][start.y < finish.y]
        else:
            raise Exception("Nodes are not neibors")

    def rotate(self, current: Direct, next: Direct):
        if current == next:
            return
        return self.rotate_map[(current, next)]

    def get_commands(self):
        return [command.value for command in self.commands]


def escape(maze):
    graph = Graph().fill_node(maze).fill_neibor()
    builder = PathBuilder(graph.start)
    dfs(builder.nodes, graph.start)
    builder.build()
    return builder.get_commands()

