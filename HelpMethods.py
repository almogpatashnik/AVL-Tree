    """rebalance tree for delete
    @type node: AVLNode
    @param node: start balancing up from node
    @type T: AVLTreeList
    @param T: tree we are working on
    @rtype: int
    @returns: number of balancing operations performed
    Time Complexity: O(logn)
    """
    def rebalanceLoop(T, node):
        cntRotations = 0
        while node != None:
            # local update
            prevParentHeight = node.height
            updateExNode(node)
            # compute BF
            bf = node.getBF()
            # if BF<2 and height hasnt changed - update path and terminate
            if abs(bf) < 2:
                if node.height == prevParentHeight:
                    updatePath(node)
                    break
                else:
                    updateExNode(node)
                    node = node.parent
            else:
                # if BF = 2 - rotate and update localy
                x = node
                node = node.parent
                cntRotations = cntRotations + rotateAndUpdateLocally(x, T)
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
    # returns number of rotations
    def rotateAndUpdate(node, T):
        ret = 1
        bfNode = node.getBF()
        rightChild = node.getRight()
        leftChild = node.getLeft()
        if bfNode == 2:  # problem in left subtree
            if leftChild.getBF() == 1:
                oneRotation("left", "right", node, T)
            else:
                semiRotation("left", "right", node)
                oneRotation("left", "right", node, T)
                updateExNode(node.parent.getLeft())  # update the third node in the rotation
                ret = 2
        if bfNode == -2:  # problem in left subtree
            if rightChild.getBF() == -1:
                oneRotation("right", "left", node, T)
            else:
                semiRotation("right", "left", node)
                oneRotation("right", "left", node, T)
                updateExNode(node.parent.getRight())
                ret = 2
        updatePath(node)
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
    def rotateAndUpdateLocally(node, T):
        numRotations = 1
        bfNode = node.getBF()
        rightChild = node.getRight()
        leftChild = node.getLeft()
        if bfNode == 2:  # problem in left subtree
            if leftChild.getBF() == 1 or leftChild.getBF() == 0:
                oneRotation("left", "right", node, T)
            else:
                semiRotation("left", "right", node)
                oneRotation("left", "right", node, T)
                numRotations += 2
        if bfNode == -2:  # problem in left subtree
            if rightChild.getBF() == -1 or rightChild.getBF() == 0:
                oneRotation("right", "left", node, T)
            else:
                semiRotation("right", "left", node)
                oneRotation("right", "left", node, T)
                numRotations += 2

        # update height and size locally
        updateExNode(node.parent.right)
        updateExNode(node.parent.left)
        updateExNode(node.parent)
        return numRotations


    """perforn first step in double rotation
    @type node: AVLNode
    @param node: node on which to perform rotation
    @type dir, opDir: string
    @param dir, opDir: dir is direction of the rotation, opDir is opposite direction
    Time Complexity: O(1)
    """
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
                loc = treeSelect(T.root, i + 1)
                if loc.left.isRealNode():
                    maxLeftSubTree = treeSelect(loc.left, loc.left.size)
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

        deleteNode(T, nodeToDelete)
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



