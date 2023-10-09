# username - saradorfman
# id1      - 211881552
# name1    - Sara Dorfman
# id2      - 314829714
# name2    - Almog Patashnik


"""A class represnting a node in an AVL tree"""
import math
import random


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @type key: int
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1  # Balance factor

        # Added fields
        self.size = 0

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the child by direrciton
    
    @type dir: string
    @param dir: left/right child
    @rtype: AVLNode
    @returns: child by direction
    """

    def getChild(self, dir):
        if dir == "right":
            node = self.right
        else:
            node = self.left
        return node

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        if self.isRealNode():
            return self.value
        return None

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height


    # -----------delete!----------
    """get size of node

    @rtype: int
    @returns: the size of self
    """
    def getSize(self):
        return self.size

    # -----------------------

    """sets left child

    @type node: AVLNode
    @param node: a node
    """
    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets child by direction

    @type node: AVLNode
    @type dir: string
    @param node: a node
    @param dir: left/right child
    """

    def setChild(self, dir, node):
        if dir == "left":
            self.setLeft(node)
        else:
            self.setRight(node)

    """sets parent, if self is real node

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        if (self.isRealNode()):
            self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        return self.height != -1

    """returns BF

    @rtype: int
    @returns: BF
    """

    def getBF(self):
        return self.left.height - self.right.height


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.size = 0
        self.root = None

        # add your fields here
        self.virtual = AVLNode("")
        self.firstItem = None
        self.lastItem = None

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.size == 0

    """retrieves the value of the i'th item in the list

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
        # delete later - just to pass some tests
        if i < 0 or i >= self.length():
            return -1
        # ----------------------------------------
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

        # --------------implementation------------
        result = AVLTreeList()
        if self.size == 0:
            return result
        arr = self.listToArray()
        HF.shuffleArray(arr)
        firstLast = [None, None]
        resRoot = recursiveAVLTree(self, arr, 0, len(arr) - 1, firstLast)
        result.root = resRoot
        result.size = result.root.size
        result.firstItem = firstLast[0]
        result.lastItem = firstLast[1]
        return result

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    Time Complexity: O(logn)
    """

    def concat(self, lst):
        heightSelf = 0 if self.root is None else self.root.height
        heightLst = 0 if lst.root is None else lst.root.height
        ret = abs(heightSelf - heightLst)
        # if one list is empty, update self to be that list and return
        if lst.root is None:
            return ret
        if self.root is None:
            self.reassign(lst)
            return ret
        # lst is heigher
        if self.root.height < lst.root.height:
            HF.concatT1Low(self, lst)
        else:
            # self is heigher
            if self.root.height > lst.root.height:
                HF.concatT1High(self, lst)
            # same heights
            else:
                HF.cocatSameHeights(self, lst)

        # set properties of lst
        HF.updateExNode(self.root)
        self.size = self.root.size
        self.firstItem = self.retrieveNode(0)
        self.lastItem = self.retrieveNode(self.length() - 1)

        return ret

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
        if (self.length() == 0 or val is None):
            return -1
        searchRec(self.root.left, self.root.left.size + 1, val, indexArr)
        if (indexArr[0] == -1):
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


# ---------------- Help Functions Class ---------------------------#

class HF:

    """swaps nodes node1 and node2 (swaps all pointers )

    @type node1, node2: AVLNode
    @param node1, node2: nodes to swap

    Time Complexity: O(1)
    """
    @staticmethod
    def swapNodes(node1, node2):
        tmp1 = node1
        tmp2 = node2
        # node1 is heigher than node2
        node1 = tmp1 if tmp1.height >= tmp2.height else tmp2
        node2 = tmp2 if tmp1.height >= tmp2.height else tmp1
        node1NotParent = node2.parent != node1
        temp = AVLNode("Temp")
        temp.left = node1.left
        temp.right = node1.right
        temp.parent = node1.parent


        node1parent = node1.parent
        dir1 = None
        if node1.parent != None:
            dir1 = "left" if node1.parent.left == node1 else "right"

        dir2 = None
        node2parent = node2.parent if node1NotParent else node2
        if node1NotParent:
            node2parent = node2.parent
            if node2.parent != None:
                dir2 = "left" if node2.parent.left == node2 else "right"
        else:
            node2parent = node2
            if node1.parent != None:
                dir2 = "left" if node1.parent.left == node1 else "right"


        #config node1 - here there is no problem of node1 is a child of mode2
        node1.left = node2.left
        node1.right = node2.right
        node2.left.setParent(node1)
        node2.right.setParent(node1)

        # if node2 is child of node1, fix manually using if statement
        if temp.left != node2:
            node2.left = temp.left
            temp.left.setParent(node2)
        else:
            node2.left = node1
            temp.left.setParent(temp.parent)

        if temp.right != node2:
            node2.right = temp.right
            temp.right.setParent(node2)
        else:
            node2.right = node1
            temp.right.setParent(temp.parent)

        HF.updateExNode(node1)
        HF.updateExNode(node2)

        if dir1 is not None:
            node1.parent = node2parent
            if node1NotParent: # already happened if node2 is child of node1
                node2parent.setChild(dir1, node1)
        if dir2 is not None:
            node2.parent = node1parent
            node1parent.setChild(dir2, node2)



    @staticmethod
    # T1 is lower than T2, concat T2 to T1
    def concatT1Low(T1, T2):
        h = T1.root.height
        # node x s.t. T1<x<T2
        x = AVLNode("Dummy")
        realRoot = T2.firstItem

        # find first node with height h/h-1
        b = T2.firstItem
        while b.height < h - 1:
            b = b.parent
        if b!= T2.root and b.parent.height == h:
            b = b.parent
        c = b.parent

        # connecting x to both trees
        x.left = T1.root
        x.right = b
        b.parent = x
        T1.root.parent = x
        # connecting x to b's previous parent
        c.left = x
        x.parent = c

        HF.updateExNode(x)

        #swap to real node
        HF.swapNodes(x, realRoot)

        # set new properties of T1
        T1.root = T2.root
        T1.size = T1.size + T2.size + 1
        HF.updateExNode(realRoot)

        # rebalance tree
        HF.rebalanceLoop(T1, c)
        T1.delete(realRoot.left.size + 1)

    @staticmethod
    # T1 is higher than T2, concat T2 to T1
    def concatT1High(T1, T2):
        h = T2.root.height
        # node x s.t. T2<x<T1
        x = AVLNode("Dummy")
        realRoot = T1.lastItem
        deleteIdx = T1.size - 1

        # find first node with height h/h-1
        b = T1.lastItem
        while b.height < h - 1:
            b = b.parent
        if b != T1.root and b.parent.height == h:
            b = b.parent
        c = b.parent

        # connecting x to both trees
        x.left = b
        x.right = T2.root
        b.parent = x
        T2.root.parent = x
        # connecting x to b's previous parent
        c.right = x
        x.parent = c

        HF.updateExNode(x)
        # swap to real node
        HF.swapNodes(x, realRoot)

        # set new properties of T1
        T1.size = T1.size + T2.size + 1
        HF.updateExNode(x)

        # rebalance tree
        HF.rebalanceLoop(T1, c)
        T1.delete(deleteIdx)

    @staticmethod
    # T1 is same height as T2, concat T2 to T1
    def cocatSameHeights(T1, T2):
        # join them with temporary root
        dummyRoot = AVLNode('DUMMY')
        dummyRoot.left = T1.root
        dummyRoot.right = T2.root
        T1.root.parent = dummyRoot
        T2.root.parent = dummyRoot
        HF.updateExNode(dummyRoot)

        # get actual root
        realRoot = T1.lastItem
        realRootIndex = T1.length() - 1

        # set properties of T1
        T1.root = dummyRoot
        T1.size = dummyRoot.size

        T1.delete(realRootIndex)

        # set real node
        realRoot.left = dummyRoot.left
        realRoot.right = dummyRoot.right
        dummyRoot.left.parent = realRoot
        dummyRoot.right.parent = realRoot
        HF.updateExNode(realRoot)
        T1.root = realRoot

    """rebalance tree for delete and concat

    @type node: AVLNode
    @param node: start balancing up from node
    @type T: AVLTreeList
    @param T: tree we are working on
    @rtype: int
    @returns: number of balancing operations performed

    Time Complexity: O(logn)
    """
    @staticmethod
    def rebalanceLoop(T, node):
        cntRotations = 0
        while node != None:
            # local update
            prevParentHeight = node.height
            HF.updateExNode(node)
            # compute BF
            bf = node.getBF()
            # if BF<2 and height hasnt changed - update path and terminate
            if abs(bf) < 2:
                if node.height == prevParentHeight:
                    HF.updatePath(node)
                    break
                else:
                    HF.updateExNode(node)
                    node = node.parent
            else:
                # if BF = 2 - rotate and update localy
                x = node
                node = node.parent
                cntRotations = cntRotations + HF.rotateAndUpdateLocally(x, T)
        return cntRotations

    """returns the k'th smallest item in the subtree of node

    @type node: AVLNode
    @param node: search for k'th item in node's subtree
    @type k: int
    @param val: serch for k'th item in node's subtree
    @rtype: AVLNode
    @returns: k'th item in node's subtree, None if not found.
    
    Time Complexity: O(logn)
    """
    @staticmethod
    def treeSelect(node, k):
        def select(x, k):
            r = x.left.size + 1
            if k == r:
                return x
            else:
                if k < r:
                    return select(x.left, k)
            return select(x.right, k - r)

        if k < 1 or k > node.size:
            return None
        return select(node, k)


    """updates height and size fields for every node starting from node up until the root

    @type node: AVLNode
    @param node: node to start updating up its path
    
    Time Complexity: O(logn)
    """
    @staticmethod
    def updatePath(node):
        x = node
        while x is not None:
            x.size = x.left.size + x.right.size + 1
            x.height = max(x.left.getHeight(), x.right.getHeight()) + 1
            x = x.parent

    """perform a rotation and update fields in path up until root

    @type node: AVLNode
    @param node: avl criminal
    @type T: AVLTreeList
    @param T: tree to which node is connected
    @rtype: int
    @returns: number of rotations performed
    
    Time Complexity: O(logn)
    """
    @staticmethod
    # returns number of rotations
    def rotateAndUpdate(node, T):
        ret = 1
        bfNode = node.getBF()
        rightChild = node.getRight()
        leftChild = node.getLeft()
        if bfNode == 2:  # problem in left subtree
            if leftChild.getBF() == 1:
                HF.oneRotation("left", "right", node, T)
            else:
                HF.semiRotation("left", "right", node)
                HF.oneRotation("left", "right", node, T)
                HF.updateExNode(node.parent.getLeft())  # update the third node in the rotation
                ret = 2
        if bfNode == -2:  # problem in left subtree
            if rightChild.getBF() == -1:
                HF.oneRotation("right", "left", node, T)
            else:
                HF.semiRotation("right", "left", node)
                HF.oneRotation("right", "left", node, T)
                HF.updateExNode(node.parent.getRight())
                ret = 2
        HF.updatePath(node)
        return ret

    """perform a rotation and update fields locally

    @type node: AVLNode
    @param node: avl criminal
    @type T: AVLTreeList
    @param T: tree to which node is connected
    @rtype: int
    @returns: number of rotations performed

    Time Complexity: O(1)
    """
    @staticmethod
    def rotateAndUpdateLocally(node, T):
        numRotations = 1
        bfNode = node.getBF()
        rightChild = node.getRight()
        leftChild = node.getLeft()
        if bfNode == 2:  # problem in left subtree
            if leftChild.getBF() == 1 or leftChild.getBF() == 0:
                HF.oneRotation("left", "right", node, T)
            else:
                HF.semiRotation("left", "right", node)
                HF.oneRotation("left", "right", node, T)
                numRotations += 2
        if bfNode == -2:  # problem in left subtree
            if rightChild.getBF() == -1 or rightChild.getBF() == 0:
                HF.oneRotation("right", "left", node, T)
            else:
                HF.semiRotation("right", "left", node)
                HF.oneRotation("right", "left", node, T)
                numRotations += 2

        # update height and size locally
        HF.updateExNode(node.parent.right)
        HF.updateExNode(node.parent.left)
        HF.updateExNode(node.parent)
        return numRotations

    """perforn first step in double rotation

    @type node: AVLNode
    @param node: node on which to perform rotation
    @type dir, opDir: string
    @param dir, opDir: dir is direction of the rotation, opDir is opposite direction

    Time Complexity: O(1)
    """
    @staticmethod
    def semiRotation(dir, opDir, node):
        child = node.getChild(dir)
        grand = child.getChild(opDir)
        # handle pointers switch
        grand.setParent(node)
        node.setChild(dir, grand)
        child.setChild(opDir, grand.getChild(dir))
        child.getChild(opDir).setParent(child)
        grand.setChild(dir, child)
        child.setParent(grand)

    """perforn one rotation

    @type dir, opDir: string
    @param dir, opDir: dir is direction of the rotation, opDir is opposite direction
    @type node: AVLNode
    @param node: node on which to perform rotation
    @type T: AVLTreeList
    @param T: tree to which node is connected

    Time Complexity: O(1)
    """
    @staticmethod
    def oneRotation(dir, opDir, node, T):
        nodeParent = node.getParent()
        child = node.getChild(dir)
        # handle pointers switch
        node.setChild(dir, child.getChild(opDir))
        node.getChild(dir).setParent(node)
        child.setChild(opDir, node)
        child.setParent(nodeParent)
        # handling according to if node is root
        if node != T.root:
            if nodeParent.getChild(dir) == node:
                nodeParent.setChild(dir, child)
            else:
                nodeParent.setChild(opDir, child)
        else:
            T.root = child
        node.setParent(child)

    """update size and height of node

    @type node: AVLNode
    @param node: node to update

    Time Complexity: O(1)
    """
    @staticmethod
    def updateExNode(node):
        node.setHeight(max(node.left.getHeight(), node.right.getHeight()) + 1)
        node.size = node.left.size + node.right.size + 1

    """insert new node with value val at positions i as in BST
    
    @type T: AVLTreeList
    @param T: tree to insert to
    @type i: int
    @param i: index to insert val at
    @type val: string
    @param val: value to insert
    @rtype: AVLNode
    @returns: return the new node

    Time Complexity: O(logn)
    """
    @staticmethod
    def insertNode(T, i, val):
        newNode = T.createNode(val)
        if T.length() == 0:
            T.root = newNode
        else:
            if i == T.length():
                newNode.setParent(T.lastItem)
                T.lastItem.setRight(newNode)
            else:
                # insert new node as predecessor of current item in position i
                loc = HF.treeSelect(T.root, i + 1)
                if loc.left.isRealNode():
                    maxLeftSubTree = HF.treeSelect(loc.left, loc.left.size)
                    maxLeftSubTree.setRight(newNode)
                else:
                    maxLeftSubTree = loc
                    loc.setLeft(newNode)
                newNode.setParent(maxLeftSubTree)

        T.size += 1
        return newNode

    """delete node as in BST

    @type T: AVLTreeList
    @param T: tree to delete from
    @type node: AVLNode
    @param n: node to delete
    @type i: int
    @param i: index of deleted item
    @rtype: AVLNode
    @returns: return parent of the deleted node

    Time Complexity: O(logn)
    """
    @staticmethod
    def BSTdelete(T, node, i):
        nodeToDelete = node
        ret = nodeToDelete.parent
        succesorFlag = False
        if node.left.isRealNode() and node.right.isRealNode():
            # find successor
            nodeToDelete = T.retrieveNode(i + 1)
            succesorFlag = True

            if nodeToDelete.parent == node:
                ret = nodeToDelete
            else:
                ret = nodeToDelete.parent

        HF.deleteNode(T, nodeToDelete)
        if succesorFlag:
            nodeToDelete.height = node.height
            nodeToDelete.size = node.size
            # change pointers of physically deleted node
            nodeToDelete.right = node.right
            nodeToDelete.left = node.left
            nodeToDelete.left.setParent(nodeToDelete)
            nodeToDelete.right.setParent(nodeToDelete)
            # handling parent
            if T.root != node:
                dir = 'left' if node.parent.left == node else 'right'
                nodeToDelete.setParent(node.parent)
                node.parent.setChild(dir, nodeToDelete)
            else:
                T.root = nodeToDelete
                nodeToDelete.parent = None

        return ret

    """delete node physically

        @type T: AVLTreeList
        @param T: tree to delete from
        @type node: AVLNode
        @param n: node to delete

        Time Complexity: O(1)
        """
    @staticmethod
    def deleteNode(T, node):
        # delete the node, assuming it is a successor
        connectedChild = node.right if node.right.isRealNode() else node.left
        parent = node.parent
        if node != T.root:
            dirChildType = "right" if parent.right == node else "left"
            parent.setChild(dirChildType, connectedChild)
        else:
            T.root = connectedChild if connectedChild.isRealNode() else None

        if connectedChild.isRealNode():
            connectedChild.setParent(parent)

    """shuffle array

    @type lst: array
    @param lst: array to shuffle

    Time Complexity: O(n)
    """
    @staticmethod
    def shuffleArray(lst):
        for i in range(len(lst)):
            randNum = random.randint(0, len(lst) - 1)
            # swap
            keepNum = lst[randNum]
            lst[randNum] = lst[i]
            lst[i] = keepNum
