
class BTreeNode:
    MININUM = 1

    elements = []
    sub_nodes = []

    def __init__(self, elements, sub_nodes, mininum=None):
        self.elements = elements or []
        self.sub_nodes = sub_nodes or []
        self.MININUM = mininum or self.MININUM

    @property
    def MAXINUM(self):
        return self.MININUM * 2

    @property
    def elements_count(self):
        return len(self.elements) if self.elements else 0

    @property
    def sub_nodes_count(self):
        return len(self.sub_nodes) if self.sub_nodes else 0

    # interface

    '''
    add a new element to this set, if the element was already in the set, then there is no change.
    '''
    def add(self, elem):
        self._loose_add(elem)
        if self.elements_count > self.MAXINUM:
            new_root = BTreeNode([], [self])
            new_root._fix_excess(0)
            return new_root
        return self

    '''
    remove a specified element from this set
    '''
    def remove(self, elem):
        self._loose_remove(elem)
        if self.sub_nodes == 1 and self.elements_count == 0:
            return self.sub_nodes[0]
        return self

    def _loose_remove(self, target):
        index = self._first_GE(target)
        if (self.sub_nodes_count == 0 and
                index < self.elements_count and
                self.elements[index] != target):
            return
        elif (self.sub_nodes_count == 0 and
                index < self.elements_count and
                self.elements[index] == target):
            self.elements.pop(index)
            return
        elif (self.sub_nodes_count > 0 and
                index < self.elements_count and
                self.elements[index] != target) or index == self.elements_count:
            self.sub_nodes[index]._loose_remove(target)
            if self.sub_nodes[index].elements_count < self.MININUM:
                self.fix_shortage(index)
        elif (self.sub_nodes_count > 0 and
                index < self.elements_count and
                self.elements[index] == target):
            self.elements[index] = self.sub_nodes[index].remove_largest()
            if self.sub_nodes[index].elements_count < self.MININUM:
                self.fix_shortage(index)

    def remove_largest(self):
        if self.sub_nodes_count <= 0:
            return self.elements.pop(-1)
        res = self.sub_nodes[-1].remove_largest()
        if self.sub_nodes[-1].elements_count < self.MININUM:
            self.fix_shortage(self.sub_nodes_count - 1)
        return res

    def fix_shortage(self, child_index):

        if 0 <= child_index < self.sub_nodes_count - 1 and self.sub_nodes[child_index + 1].elements_count > self.MININUM:
            self.sub_nodes[child_index].elements.append(self.elements[child_index])
            if self.sub_nodes[child_index + 1].sub_nodes:
                self.sub_nodes[child_index].sub_nodes.append(
                    self.sub_nodes[child_index + 1].sub_nodes.pop(0)
                )
            self.elements[child_index] = self.sub_nodes[child_index + 1].elements.pop(0)

        elif child_index > 0 and self.sub_nodes[child_index - 1].elements_count > self.MININUM:
            self.sub_nodes[child_index].elements.append(self.elements[child_index - 1])
            if self.sub_nodes[child_index].sub_nodes:
                self.sub_nodes[child_index].sub_nodes.append(
                    self.sub_nodes[child_index - 1].sub_nodes.pop(-1)
                )
            self.elements[child_index - 1] = self.sub_nodes[child_index - 1].elements.pop(-1)

        elif child_index > 0 and self.sub_nodes[child_index - 1].elements_count == self.MININUM:
            child = self.sub_nodes[child_index]
            new_child = BTreeNode(
                self.sub_nodes[child_index - 1].elements[:] + [self.elements.pop(child_index - 1)],
                self.sub_nodes[child_index - 1].sub_nodes[:] + child.sub_nodes[:]
            )
            self.sub_nodes[child_index - 1] = new_child
            self.sub_nodes.pop(child_index)

        elif 0 <= child_index < self.sub_nodes_count and self.sub_nodes[child_index + 1].elements_count == self.MININUM:
            child = self.sub_nodes[child_index]
            new_child = BTreeNode(
                [self.elements.pop(child_index)] + self.sub_nodes[child_index + 1].elements[:],
                child.sub_nodes[:] + self.sub_nodes[child_index + 1].sub_nodes[:]
            )
            self.sub_nodes[child_index] = new_child
            self.sub_nodes.pop(child_index + 1)

    '''
    determine whether a particular element is in this set
    '''
    def contains(self, target):
        index = self._first_GE(target)

        if index < self.elements_count and self.elements[index] == target:
            return True
        elif self.sub_nodes_count == 0:
            return False
        else:
            return self.sub_nodes[index].contains(target)

    def _first_GE(self, target):
        for i in range(self.elements_count):
            if self.elements[i] >= target:
                return i                
        return self.elements_count

    def _insert_element(self, elem):
        if not self.elements or self.elements[-1] < elem:
            self.elements.append(elem)
            return
        for i in range(self.elements_count):
            if elem <= self.elements[i]:
                self.elements.insert(i, elem)
                return

    def _loose_add(self, target):
        index = self._first_GE(target)
        if index < self.elements_count and self.elements[index] == target:
            return
        elif self.sub_nodes_count == 0:
            self._insert_element(target)
        else:
            sub_node = self.sub_nodes[index]
            sub_node._loose_add(target)
            if sub_node.elements_count > sub_node.MAXINUM:
                self._fix_excess(index)

    def _fix_excess(self, index):
        excess_node = self.sub_nodes.pop(index)

        mid = excess_node.MAXINUM // 2

        left = BTreeNode(
            excess_node.elements[:mid], excess_node.sub_nodes[:mid + 1]
        )
        right = BTreeNode(
            excess_node.elements[mid + 1:], excess_node.sub_nodes[mid + 1:]
        )
        self.sub_nodes.insert(index, right)
        self.sub_nodes.insert(index, left)

        self._insert_element(excess_node.elements[mid])


# Serarch
def search(i):
    n11 = BTreeNode([2,3], None)
    n12 = BTreeNode([5], None)
    n13 = BTreeNode([10], None)
    n14 = BTreeNode([16], None)
    n15 = BTreeNode([18], None)
    n16 = BTreeNode([20], None)
    n17 = BTreeNode([25], None)

    n21 = BTreeNode([4], [n11, n12])
    n22 = BTreeNode([12], [n13, n14])
    n23 = BTreeNode([19, 22], [n15, n16, n17])

    root = BTreeNode([6, 17], [n21, n22, n23])

    return root.contains(i)


def level_traverse(root):
    queue = [root]
    rv = []
    while len(queue) > 0:
        node = queue.pop(0)
        rv.append(node.elements)
        for child in node.sub_nodes:
            queue.append(child)
    return rv


def print_tree(tree):
    print(level_traverse(root))


if __name__ == '__main__':
    rv = []
    nums = [5]
    root = BTreeNode([], [])
    for i in [2, 3, 5,10,16,18,20,25,4,12,19,22,6,17][::-1]:
        root = root.add(i)
        rv = level_traverse(root)
    print(level_traverse(root))

    # root = root.remove(22)
    # print(level_traverse(root))
    root = root.remove(12)
    root = root.remove(6)
    root = root.remove(19)
    root = root.remove(5)
    root = root.remove(18)
    root = root.remove(17)

    print(level_traverse(root))
