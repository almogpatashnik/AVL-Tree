# AVL Tree   
This is a Python implementation of an AVL Tree, which is a self-balancing binary search tree. In an AVL Tree, the heights of the two child subtrees of any node are kept in balance, with a maximum height difference of one. Whenever this balance is disrupted, a process called 'rebalancing' is triggered to restore it.

This unique property ensures that essential operations like searching, insertion, deletion, joining, and splitting of elements within the tree operate efficiently, with a time complexity of O(log n) in both average and worst-case scenarios.

In this implementation, we've introduced the concept of 'imaginary nodes.' For every actual node in the tree, two virtual nodes are associated, which assist in maintaining the tree's balanced structure.  

## Usage
In order to use the AVLTree and AVLNode instances you should download the files from the *AVL folder*, place them in the correct directory 
and import as follow:
```python
from AVLList import AVLTreeList
```

### AVLTree Class
| Function       | Description                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| empty()        | Returns True if the tree is empty.                                                                                                                                      |
| retrieve(i)    | Returns the value of the item in place of i if it exists, otherwise it returns None.                                                                                     |
| insert(i, s)   | Inserts an item with value s into the list at the i-th place, if there are at least i items in the list. Returns the total number of rebalancing operations required in the step of repairing the tree to preserve the balance feature. |
| delete(i)      | Deletes the item at the i-th place in the list, if it exists. Returns the total number of balancing actions required during the tree repair phase to preserve the balance feature. If there are not enough items in the list, the function returns -1. |
| first()        | Returns the value of the first value in the list. If the list is empty, returns None.                                                                                   |
| last()         | Returns the value of the last value in the list. If the list is empty, returns None.                                                                                    |
| listToArray()  | Returns an array containing the elements of the list in the order of the indexes, or an empty array if the list is empty.                                              |
| length()       | Returns the number of items in the list.                                                                                                                                  |
| permutation()  | Returns the items of the list in a random order.                                                                                                                          |
| sort()         | Sorts the items in the list.                                                                                                                                             |
| search(val)    | Searches for an item in the list with the value of val and returns its index. If it doesn't exist in the list, returns -1.                                               |



### AVLNode SubClass
| Function         | Description                                                        |
|------------------|--------------------------------------------------------------------|
| getHeight()       | Returns the height of the node in the tree. If the Node is virtual returns -1.                                  |
| getValue()       | Returns the value of the node in the tree. If the Node is virtual returns -1.                                  |
| getLeft()        | Returns the left son of the node in the tree. If it doesnt have - returns None.    |
| getRight()        | Returns the right son of the node in the tree. If it doesnt have - returns None.    |
| getParent()       | Returns the parent of the node in the tree. If it doesnt have - returns None.   |
| isRealNode()     | Returns True if the node is real (ie: a non-virtual node).                               |



***Made by [@almogpatashnik](https://github.com/almogpatashnik) && [@saradorf](https://github.com/saradorf)***
