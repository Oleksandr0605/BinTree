"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from random import shuffle
from math import log
import time



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of source_collection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            sss = ""
            if node is not None:
                sss += recurse(node.right, level + 1)
                sss += "| " * level
                sss += str(node.data) + "\n"
                sss += recurse(node.left, level + 1)
            return sss

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_maxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_maxinleftsubtreetotop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not  None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return max(height1(self._root) - 1, 0)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def count_vert(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            else:
                return 1 + count_vert(top.left) + count_vert(top.right)
        return self.height() < 2 * log(count_vert(self._root) + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [elm for elm in self.inorder() if low <= elm <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build_list(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return []
            else:
                return build_list(top.left) + [top.data] + build_list(top.right)

        def build_tree(tree):
            '''
            Helper function
            :param tree:
            '''
            if len(tree) == 0:
                return None
            else:
                self.add(tree[len(tree) // 2])
                build_tree(tree[:len(tree) // 2])
                build_tree(tree[len(tree) // 2 + 1:])
        tree_list = build_list(self._root)
        self.clear()
        build_tree(tree_list)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def find_items(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return []
            else:
                return find_items(top.left) + [top.data] + find_items(top.right)

        items = find_items(self._root)
        try:
            if item in items:
                items.sort()
                return items[items.index(item) + 1]
            else:
                items.append(item)
                items.sort()
                return items[items.index(item) + 1]
        except:
            return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def find_items(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return []
            else:
                return find_items(top.left) + [top.data] + find_items(top.right)

        items = find_items(self._root)
        try:
            if item in items:
                items.sort()
                return items[items.index(item) - 1] if items.index(item) -1 != -1 else None
            else:
                items.append(item)
                items.sort()
                return items[items.index(item) - 1] if items.index(item) -1 != -1 else None
        except:
            return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = read_file('words(1).txt')
        random_words = words
        shuffle(random_words)
        create_tree(self, words)

        start_time = time.time()
        for _ in range(10000):
            elm = random_words[_]
            for word in words:
                if elm == word:
                    break
        end_time = time.time()
        print("Time taken for list searching:", end_time - start_time)

        start_time = time.time()
        for _ in range(10000):
            self.find(random_words[_])
        end_time = time.time()
        print("Time taken for searching in alphabet tree:", end_time - start_time)

        self.clear()
        create_tree(self, random_words)

        start_time = time.time()
        for _ in range(10000):
            self.find(words[_])
        end_time = time.time()
        print("Time taken for searching in random tree:", end_time - start_time)

        self.clear()
        create_tree(self, words)
        self.rebalance()

        start_time = time.time()
        for _ in range(10000):
            self.find(random_words[_])
        end_time = time.time()
        print("Time taken for searching in rebalabced tree:", end_time - start_time)


def read_file(path):
    """
    read file
    """
    with open(path, 'r', encoding="utf-8") as file:
        return file.read().split('\n')

def create_tree(tree, words):
    """
    create tree
    """
    for word in words:
        tree.add(word)

if __name__ == '__main__':
    bst = LinkedBST()
    bst.demo_bst('words(1).txt')
    