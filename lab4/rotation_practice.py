"""Parts 3-4: implement AVL balance factor, rotations, and iterative and recursive AVL insertion.

Node structure, tree container, and height maintenance helpers are provided.
"""

from bst_practice import bst_insert

class Node:
  """Binary Search Tree node with parent pointer and height attribute."""

  def __init__(self, key, parent=None):
    self.key = key
    self.parent = parent
    self.left = None
    self.right = None
    self.height = 0

  def __repr__(self):
    return "Node(" + str(self.key) + ")"


class BinarySearchTree:
  """Container holding the root pointer of a Binary Search Tree."""

  def __init__(self):
    self.root = None

  def print_tree(self):
    """Print the full tree with child labels, heights, balance factors, and parents."""
    if self.root is None:
      print("(empty tree)")
      return

    seen = set()

    def node_summary(node):
      left_height = -1 if node.left is None else node.left.height
      right_height = -1 if node.right is None else node.right.height
      bf = left_height - right_height
      parent_key = "None" if node.parent is None else str(node.parent.key)
      return (
        str(node.key)
        + " [height=" + str(node.height)
        + ", bf=" + str(bf)
        + ", parent=" + parent_key + "]"
      )

    def print_children(node, prefix):
      if node.left is None and node.right is None:
        return

      children = [("L", node.left), ("R", node.right)]
      for index, (direction, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")

        if child is None:
          print(prefix + connector + direction + ": None")
        elif id(child) in seen:
          print(
            prefix + connector + direction + ": "
            + node_summary(child) + " [cycle or repeated reference]"
          )
        else:
          seen.add(id(child))
          print(prefix + connector + direction + ": " + node_summary(child))
          print_children(child, child_prefix)

    seen.add(id(self.root))
    print(node_summary(self.root))
    print_children(self.root, "")


def get_height(node):
  """Provided: return height of node (-1 for None, 0 for leaf)."""
  if node is None:
    return -1
  return node.height


def update_height(node):
  """Provided: recalculate node's height based on its left and right children."""
  if node is not None:
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def balance_factor(node):
  """Calculate balance factor: height(node.left) - height(node.right).

  Return 0 if node is None.
  """
  if node is None:
    return 0
  else:
    return get_height(node.left) - get_height(node.right)

def rotate_left(tree, x):
  """Perform a single left rotation around node x.

  Pivots on x's right child y. Updates child pointers, parent pointers,
  tree.root (if x was root), and recalculates heights for x and y.
  """
  # TODO 3.2B: Rewire pointers so y = x.right rises into x's position; update heights of x then y.
  y = x.right

  #transfer y's left child (if it isnt none) to x's right
  #update y's left child to see x as its new parent
  x.right = y.left
  if y.left != None:
    y.left.parent = x

  #changing the parent of x to point to y
  #y's parent is now set to x's parent to transfer y into its final position
  #if the parent is none then set the tree's root to y (as it is the new root)
  #else if x is the parents left child then y becomes that left child
  #the final possible case is x is the parents right child so y replaces it there
  y.parent = x.parent 
  if x.parent == None:
    tree.root = y
  elif x == x.parent.left:
    x.parent.left = y
  else:
    x.parent.right = y

  #final transition of x
  #y left child becomes x
  #x parent becomes y
  y.left = x
  x.parent = y

  #update from bottom to top
  update_height(x) #x is the lowerst child in the tree
  update_height(y) #y is the parent of x so it is higher


def rotate_right(tree, y):
  """Perform a single right rotation around node y.

  Pivots on y's left child x. Updates child pointers, parent pointers,
  tree.root (if y was root), and recalculates heights for y and x.
  """
  # TODO 3.2C: Rewire pointers so x = y.left rises into y's position; update heights of y then x.
  x = y.left #get y's right child (x) to rotate into y's spot

  #transfer x's right child (if it isnt none) to y's left
  #update x's right child to see y as its new parent
  y.left = x.right
  if x.right != None:
    x.right.parent = y

  #changing the parent of y to point to x
  #x's parent is now set to y's parent to transfer x into its final position
  #if the parent is none then set the tree's root to x (as it is the new root)
  #else if y is the parents left child then x becomes that left child
  #the final possible case is y is the parents right child so x replaces it there
  x.parent = y.parent 
  if y.parent == None:
    tree.root = x
  elif y == y.parent.left:
    y.parent.left = x
  else:
    y.parent.right = x

  #final transition of x
  #x right child becomes y
  #y parent becomes y
  x.right = y
  y.parent = x

  #update from bottom to top
  update_height(y) #y is the child of x so it goes first
  update_height(x) #x is the parent so it is updated last



def rotate_left_right(tree, z):
  """Perform a double Left-Right (LR) rotation around node z.

  Rotates left on z's left child, then rotates right on z.
  """
  # TODO 3.2D: Call rotate_left on z.left, then rotate_right on z.
  rotate_left(tree, z.left)
  rotate_right(tree, z)


def rotate_right_left(tree, z):
  """Perform a double Right-Left (RL) rotation around node z.

  Rotates right on z's right child, then rotates left on z.
  """
  # TODO 3.2E: Call rotate_right on z.right, then rotate_left on z.
  rotate_right(tree, z.right)
  rotate_left(tree, z)

def rebalance(tree, node, key):
  update_height(node)
  bf = balance_factor(node)

  #left heavy subtree
  if bf > 1:
    if key < node.left.key:
      rotate_right(tree, node) #LR
    else:
      rotate_left_right(tree, node) #LR
    return True #did rebalance

  #right heavy subtree
  if bf < -1:
    if key > node.right.key:
      rotate_left(tree, node) #RR
    else:
      rotate_right_left(tree, node) #RL
    return True #did rebalance
  
  return False # did not need to rebalance

def avl_insert_iterative(tree, key):
  """Insert a key iteratively, restore AVL balance, and return its Node."""
  # TODO 4.1A: BST-insert with a loop, then walk parent pointers upward updating heights and rotating at the first unbalanced node.
  inserted = bst_insert(tree, key) #return early on a duplicate key
  current = inserted.parent
  while current != None:
    if rebalance(tree, current, key) == True:
      break
    current = current.parent
  return inserted


def avl_insert_recursive(tree, key):
  """Insert a key recursively, restore AVL balance, and return its Node."""
  # TODO 4.1B: Recurse down to an empty slot; on the way back up, update heights, rotate if unbalanced, and return the subtree root.
  inserted = None
  
  # #define the recursive function to call
  def insert_subtree(node, parent):
    nonlocal inserted

    #if the node is empty insert the new value
    if node == None:
      inserted = Node(key, parent)
      return inserted

    #if the inserted key is less than node key go into the left child
    #else if the key is grater than the node key move into the right child
    #the final case is that the you are at the correct position so update the node with the new value
    if key < node.key:
      node.left = insert_subtree(node.left, node)
    elif key > node.key:
      node.right = insert_subtree(node.right, node)
    else:
      inserted = node
      return node #duplicate key

    #rebalance the tree if need be
    if rebalance(tree, node, key) == True:
      return node.parent #return the node that rotated into this position
    return node
  
  tree.root = insert_subtree(tree.root, None)
  tree.root.parent = None

  return inserted


if __name__ == "__main__":
  from lab_checks import check_rotations
  raise SystemExit(
    check_rotations(
      balance_factor,
      rotate_left,
      rotate_right,
      rotate_left_right,
      rotate_right_left,
      avl_insert_iterative,
      avl_insert_recursive
    )
  )
