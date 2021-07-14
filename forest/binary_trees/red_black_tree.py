"""
- Every node is either red or black
- The root is black
- Every leaf is black
- If a node is red, then both of its children are black
- All the path of each node from the node to leaves contains the same number of black nodes
"""

import enum
from dataclasses import dataclass
from typing import Any, Union, Optional

from forest.tree_exceptions import DuplicateKeyError


class Color(enum.Enum):
    RED = enum.auto()
    BLACK = enum.auto()


@dataclass
class Leaf:
    color = Color.BLACK


@dataclass
class Node:
    """Red-Black Tree non-leaf node definition."""

    key: Any
    data: Any
    left: Union["Node", Leaf] = Leaf()
    right: Union["Node", Leaf] = Leaf()
    parent: Union["Node", Leaf] = Leaf()
    color: Color = Color.RED


class RBTree:
    def __init__(self):
        self._NIL: Leaf = Leaf()
        self.root: Union[Node, Leaf] = self._NIL

    def __repr(self) -> str:
        """Provie the tree representation to visualize its layout."""
        if self.root:
            return (
                f"{type(self)}, root={self.root}, "
                f"tree_height={str(self.get_height(self.root))}"
            )
        return "empty tree"

    def search(self, key: Any) -> Optional[Node]:
        pass

    def insert(self, key: Any, data: Any) -> None:
        new_node = Node(key=key, data=data, color=Color.RED)
        parent: Union[Node, Leaf] = self._NIL
        current: Union[Node, Leaf] = self.root
        while isinstance(current, Node):
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise DuplicateKeyError(key=new_node.key)
        new_node.parent = parent
        if isinstance(parent, Leaf):
            new_node.color = Color.BLACK
            self.root = new_node
        else:
            if new_node.key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node

            self._insert_fixup(new_node)

    def delete(self, key: Any) -> None:
        pass

    @staticmethod
    def get_leftmost(node: Node) -> Node:
        pass

    @staticmethod
    def get_rightmost(node: Node) -> Node:
        pass

    @staticmethod
    def get_successor(node: Node) -> Union[Node, Leaf]:
        pass

    @staticmethod
    def get_predecessor(node: Node) -> Union[Node, Leaf]:
        pass

    @staticmethod
    def get_height(node: Union[Leaf, Node]) -> int:
        pass

    def inorder_traverse(self) -> traversal.Pairs:
        pass

    def preorder_traverse(self) -> traversal.Pairs:
        pass

    def postorder_traverse(self) -> traversal.Pairs:
        pass

    def _transplant(
        self, deleting_node: Node, replacing_node: Union[Node, Leaf]
    ) -> None:
        pass

    def _left_rotate(self, node_x: Node) -> None:
        pass

    def _right_rotate(self, node_x: Node) -> None:
        pass

    def _insert_fixup(self, fixing_node: Node) -> None:
        pass

    def _delete_fixup(self, fixing_node: Union[Leaf, Node]) -> None:
        pass
