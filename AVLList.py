import math
import random

import HelpMethods as HF
from AVLNode import AVLNode

"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor.
    """

    def __init__(self):
        self.size = 0
        self.root = None
        # add your fields here
        self.virtual = AVLNode("")  # dummy node for the list
        self.firstItem = None
        self.lastItem = None

    """returns whether the list is empty
    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    """retrieves the *value) of the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    Time Complexity: O(logn)
    """

    def retrieve(self, i):
        res = self.retrieveNode(i)
        if res is not None:
            return res.value
        return None

    """retrieves the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: AVLNode
    @returns: the i'th item in the list
    Time Complexity: O(logn)
    """

    def retrieveNode(self, i):
        if self.size == 0:
            return None
        node = HF.treeSelect(self.root, i + 1)
        if node is None:
            return None
        return node

    """inserts val at position i in the list
    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    Time Complexity: O(logn)
    """

    def insert(self, i, val):
        # insert as usual
        node = HF.insertNode(self, i, val)
        ret = 0

        # rebalancing
        HF.updatePath(node)
        x = node.parent
        while x is not None:
            bf = x.getBF()
            if bf == 0:
                break
            else:
                if bf == 1 or bf == -1:
                    x = x.parent
                else:
                    ret = HF.rotateAndUpdate(x, self)

        # check if last/ first node has changed
        if i == 0:
            self.firstItem = node
        if i == self.length() - 1:
            self.lastItem = node

        return ret

    """deletes the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    Time Complexity: O(logn)
    """

    def delete(self, i):
        node = HF.treeSelect(self.root, i + 1)
        parent = HF.BSTdelete(self, node, i)
        self.size = self.size - 1

        # rebalance tree
        cntRotations = HF.rebalanceLoop(self, parent)

        # check if last/ first node has changed
        if self.length() == 0:
            self.firstItem = None
            self.lastItem = None
        else:
            if i == 0:
                self.firstItem = HF.treeSelect(self.root, 1)
            if i == self.length():
                self.lastItem = HF.treeSelect(self.root, self.length())

        return cntRotations

    """returns the value of the first item in the list
    @rtype: str
    @returns: the value of the first item, None if the list is empty
    Time Complexity: O(1)
    """

    def first(self):
        if self.size == 0:
            return None
        return self.firstItem.value

    """returns the value of the last item in the list
    @rtype: str
    @returns: the value of the last item, None if the list is empty
    Time Complexity: O(1)
    """

    def last(self):
        if self.size == 0:
            return None
        return self.lastItem.value

    """returns an array representing list 
    @rtype: list
    @returns: a list of strings representing the data structure
    Time Complexity: O(n)
    """

    def listToArray(self):
        def in_order_insert(node, lst):
            if node is None or node.height == -1:
                return
            in_order_insert(node.left, lst)
            lst.append(node.value)
            in_order_insert(node.right, lst)

        lst = []
        in_order_insert(self.root, lst)
        return lst

    """returns the size of the list 
    @rtype: int
    @returns: the size of the list
    Time Complexity: O(1)
    """

    def length(self):
        return self.size

    """sort the info values of the list
    @rtype: list
    @returns: an AVLTreeList where the values are sorted by the info of the original list.
    Time Complexity: O(nlogn)
    """

    def sort(self):
        # ------ help functions----------
        def merge(A, B):
            """ merging two lists into a sorted list
                A and B must be sorted! """
            n = len(A)
            m = len(B)
            C = [None for i in range(n + m)]

            a = 0
            b = 0
            c = 0
            while a < n and b < m:
                if A[a] < B[b]:
                    C[c] = A[a]
                    a += 1
                else:
                    C[c] = B[b]
                    b += 1
                c += 1

            C[c:] = A[a:] + B[b:]
            return C

        def mergesort(lst):
            """ recursive mergesort """
            n = len(lst)
            if n <= 1:
                return lst
            else:  # two recursive calls, then merge
                return merge(mergesort(lst[0:n // 2]),
                             mergesort(lst[n // 2:n]))

        # ----------------------------------
        sortedLst = self.listToArray()
        mergesort(sortedLst)
        retAvl = AVLTreeList()
        for i in range(sortedLst):
            retAvl.insert(i, retAvl[i])
        return retAvl

    """permute the info values of the list 
    @rtype: list
    @returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
    Time Complexity: O(n)
    """

    def permutation(self):
        def recursiveAVLTree(T, arr, start, end, firstLast):
            if start - end == 0:
                leaf = AVLNode(arr[start])
                leaf.left = T.virtual
                leaf.right = T.virtual
                HF.updateExNode(leaf)
                # keep first/last fields
                if start == 0:
                    firstLast[0] = leaf
                if start == len(arr) - 1:
                    firstLast[1] = leaf
                # end of keeping fields
                return leaf

            if end - start == -1:
                return T.virtual

            median = math.floor(start + ((end - start) / 2))

            # building the trees
            tmpRoot = AVLNode(arr[median])
            leftSubTree = recursiveAVLTree(T, arr, start, median - 1, firstLast)
            rightSubTree = recursiveAVLTree(T, arr, median + 1, end, firstLast)

            # connecting the trees
            tmpRoot.left = leftSubTree
            leftSubTree.setParent(tmpRoot)
            tmpRoot.right = rightSubTree
            rightSubTree.setParent(tmpRoot)

            # updating fields
            HF.updateExNode(tmpRoot)

            return tmpRoot

        def shuffleArray(lst):
            for i in range(len(lst)):
                randNum = random.randint(0, len(lst) - 1)
                # swap
                keepNum = lst[randNum]
                lst[randNum] = lst[i]
                lst[i] = keepNum

        # --------------implementation------------
        result = AVLTreeList()
        if self.size == 0:
            return result
        arr = self.listToArray()
        shuffleArray(arr)
        firstLast = [None, None]
        resRoot = recursiveAVLTree(self, arr, 0, len(arr) - 1, firstLast)
        result.root = resRoot
        result.size = result.root.size
        result.firstItem = firstLast[0]
        result.lastItem = firstLast[1]
        return result

    """searches for a *value* in the list
    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    Time Complexity: O(n)
    """

    def search(self, val):
        # -------help function--------------
        def searchRec(x, parentRank, value, arr):
            if not x.isRealNode():
                return
            if x.parent.right == x:
                xRank = parentRank + x.left.size + 1
            else:
                xRank = parentRank - 1 - x.right.size
            searchRec(x.left, xRank, value, arr)
            if x.value == value and arr[0] == -1:
                arr[0] = xRank
            searchRec(x.right, xRank, value, arr)

        # ----------------------------------------

        indexArr = [-1]
        if self.length() == 0 or val is None:
            return -1
        searchRec(self.root.left, self.root.left.size + 1, val, indexArr)
        if indexArr[0] == -1:
            if self.root.value == val:
                return self.root.left.size
            searchRec(self.root.right, self.root.left.size + 1, val, indexArr)
        indexArr[0] = -1 if indexArr[0] == -1 else indexArr[0] - 1

        return indexArr[0]

    """returns the root of the tree representing the list
    @rtype: AVLNode
    @returns: the root, None if the list is empty
    Time Complexity: O(1)
    """

    def getRoot(self):
        return self.root

    """ create node and initialize children as virtual
    @type val: str
    @param val: value of the node we want to create
    @rtype: AVLNode
    @returns: the node we created
    Time Complexity: O(1)
    """

    def createNode(self, val):
        node = AVLNode(val)
        node.height = 0
        node.left = self.virtual
        node.right = self.virtual
        node.size = 1
        return node

    """ copy lst into self
        @type lst: AVLTreeList
        @param lst: tree to copy into self
        Time Complexity: O(1)
        """

    def reassign(self, lst):
        self.root = lst.root
        self.size = lst.size
        self.firstItem = lst.firstItem
        self.lastItem = lst.lastItem
