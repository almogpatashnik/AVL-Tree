"""A class represnting a node in an AVL tree"""


class AVLNode(object):

    """Constructor
    @type value: str
    @type key: int
    @param value: data of your node
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1  # height of the node in the tree. -1 indicate that it is a "dummy" node
        self.size = 0 #number of nodes in the node's sub tree


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
