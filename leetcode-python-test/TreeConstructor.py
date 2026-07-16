# Tree Constructor

## Question: 
## Given parent-child pairs, determine if they form a valid binary tree.

from collections import defaultdict

def tree_constructor(str_arr):
    parent_children = defaultdict(list)
    child_parent = {}

    for pair in str_arr:
        child, parent = map(int, pair.strip("()").split(","))

        # Each child can only have one parent
        if child in child_parent:
            return "false"

        child_parent[child] = parent
        parent_children[parent].append(child)

        # Binary tree: max 2 children
        if len(parent_children[parent]) > 2:
            return "false"

    return "true"

## Interview note: 
## Validates two important binary-tree rules: one parent per child and max two children per parent.
## Complexity: O(n) time.