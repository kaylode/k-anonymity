from queue import Queue


class Node:

    def __init__(self, data):

        self.data = data
        self.parent = None
        self.children = dict()
        """
        Dictionary whose values are the node children and whose keys are the corresponding nodes 
        data.
        """

    def add_child(self, child):

        child.parent = self
        self.children[child.data] = child


class Tree:

    def __init__(self, root: Node):

        self.root = root

    def bfs_search(self, data, depth=None):

        """
        Searches for a node, given its data. The search starts from the root.

        :param data:    Data of the node to find.
        :param depth:   Limits the search to nodes with the given depth.
        :return:        The node if it's found, None otherwise.
        """

        visited, queue = set(), Queue()
        # Each element of the queue is a couple (node, level):
        queue.put((self.root, 0))

        while not queue.empty():

            node, level = queue.get()

            if depth is not None and level > depth:
                break

            if depth is None:
                if node.data == data:
                    return node
            else:
                if level == depth and node.data == data:
                    return node

            for child in node.children.values():
                if child in visited:
                    continue
                queue.put((child, level + 1))

            visited.add(node)

        return None

    def _bfs_insert(self, child: Node, parent: Node) -> bool:

        node = self.bfs_search(parent.data)
        if node is not None:
            node.add_child(child)
            return True
        else:
            return False

    def insert(self, child: Node, parent: Node) -> bool:

        """
        Inserts a node given its parent. Note: insertion is done on the first node with the same
        data as the given parent node.

        :param child:   Node to insert.
        :param parent:  Parent node.
        :return:        True if the node has been inserted, False otherwise.
        """

        return self._bfs_insert(child, parent)

    def parent(self, data):

        """
        Gets the parent of a node, given the node data.

        :param data:    Data of the node to find.
        :return:        Parent node if found, None otherwise.
        """

        node = self.bfs_search(data)

        if node is not None:
            return node.parent
        else:
            return None
