"""
    B-tree implementation.

    Core Functions:
        - Insert
        - Search
        - Delete
"""
from typing import Any, List, Union, Optional, Iterator, Tuple


class BTreeNode:
    def __init__(
        self, values: Union[Any, List[Any]], max_children: int = 2
    ) -> None:
        self._m = max_children
        self._k = self._m - 1

        if not isinstance(values, List):
            values = [values]
        self.values = values
        self.children = []

        assert (
            self._m > 2
        ), "Binary tree needs at least three children per node"

    def __repr__(self) -> str:
        return "%s: [%s]" % (
            ["Node", "Leaf"][int(self.is_leaf)],
            ", ".join([str(v) for v in self.values]),
        )

    def insert(self, value: Any):
        self.values.append(value)
        self.values.sort()

    def add_node(self, node: "BTreeNode"):
        if self.is_leaf:
            self.children.append(node)
        else:
            idx = 0
            while (
                idx < len(self.values) and self.values[idx] < node.values[-1]
            ):
                idx += 1

            self.children.insert(idx, node)

    def split(self, parent: Optional["BTreeNode"]) -> "BTreeNode":
        mid = len(self.values) // 2
        median = self.values[mid]

        left_v = self.values[0:mid]
        right_v = self.values[mid + 1 :]

        self.values = left_v
        new_node = BTreeNode(right_v, max_children=self._m)
        if not parent:
            parent = BTreeNode(median, max_children=self._m)
            parent.add_node(self)
        else:
            parent.insert(median)
        parent.add_node(new_node)

        return parent

    def inorder(self, depth: int) -> Iterator[Tuple[Any, int]]:
        idx = 0
        while idx < len(self.values):
            if not self.is_leaf:
                yield from self.children[idx].inorder(depth + 1)
            yield (self.values[idx], depth)
            idx += 1

        if not self.is_leaf and idx < len(self.children):
            yield from self.children[idx].inorder(depth + 1)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def is_full(self) -> bool:
        return len(self.values) == self._k

    @property
    def needs_rebalancing(self) -> bool:
        return len(self.values) > self._k


class BTree:
    def __init__(self, max_children: int = 3) -> None:
        self.root = None
        self._m = max_children
        self._k = self._m - 1

        assert (
            self._m > 2
        ), "Binary tree needs at least three children per node"

    def __repr__(self) -> str:
        out = ""
        for v, depth in self.root.inorder(0):
            out += "-" * depth + ">"
            out += str(v)
            out += "\n"

        return out

    def _new_node(self, value: Union[Any, List[Any]]) -> BTreeNode:
        return BTreeNode(value, max_children=self._m)

    def insert(self, value: Any):
        if not self.root:
            self.root = self._new_node(value)
        else:
            if self.root.is_leaf:
                self.root.insert(value)
                if self.root.needs_rebalancing:
                    new_root = self.root.split(None)
                    self.root = new_root
            else:
                self._insert(value, self.root)
                if self.root.needs_rebalancing:
                    mid = len(self.root.values) // 2
                    median = self.root.values[mid]
                    left = self.root.values[0:mid]
                    right = self.root.values[mid + 1 :]
                    left = self._new_node(left)
                    right = self._new_node(right)

                    self.root.values = [median]
                    left.children = self.root.children[0:mid]
                    right.children = self.root.children[mid:]
                    self.root.children = [left, right]

    def _insert(self, value: Any, node: BTreeNode):
        if node.is_leaf:
            node.insert(value)
        else:
            idx = 0
            while idx < len(node.values) and node.values[idx] < value:
                idx += 1
            self._insert(value, node.children[idx])
            if node.children[idx].needs_rebalancing:
                node.children[idx].split(node)

    def search(self, value: Any) -> Optional[BTreeNode]:
        if value in self.root.values:
            return self.root
        if self.root.is_leaf:
            return None

        return self._search(value, self.root)

    def _search(self, value: Any, node: BTreeNode) -> Optional[BTreeNode]:
        if value in node.values:
            return node
        if node.is_leaf:
            return None

        idx = 0
        while idx < len(node.values) and node.values[idx] < value:
            idx += 1
        return self._search(value, node.children[idx])

    def delete(self, value: Any):
        node = self.search(value)
        if not node:
            return

        if node.is_leaf:
            node.values.remove(value)
        else:
            pass
