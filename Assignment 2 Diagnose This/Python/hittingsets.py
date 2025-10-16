def run_hitting_set_algorithm(conflict_sets):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """
    return None, None

class HittingNode:
    def __init__(self, conflict_set: list[list], conflict_sets_left: list[list], parent=None):
        self.parent: HittingNode = parent
        self.conflict_sets_left: list[list] = conflict_sets_left
        self.conflict_set: list = conflict_set
        self.children: dict[any, HittingNode | None] = {c:None for c in conflict_set}
    
    def get_hitting_sets(self) -> list[list]:
        """Collect all hitting sets assuming the tree is fully expanded.
        Each hitting set is represented as a list of branch elements.

        Returns:
            list[list]: the hitting sets
        """
        hitting_sets: list[list] = []
        for conflict, child in self.children.items():
            if child:
                for hs in child.get_hitting_sets():
                    hitting_sets.append(hs + [conflict])
            else:
                hitting_sets.append([conflict])

        return hitting_sets
    
    def get_branches(self):
        """Get the branches (keys) of this node.

        Returns:
            list: the branches (keys) of this node
        """
        return self.children.keys()
    
    def get_conflict_sets(self) -> list[list]:
        """Get the conflict sets that are left to be hit at this node.

        Returns:
            list: the conflict sets that are left to be hit at this node
        """
        return self.conflict_sets_left
    
    def is_terminal(self) -> bool:
        """A node is terminal if all conflicts have been hit.
        
        Returns:
            bool: True if terminal, False otherwise
        """
        return len(self.conflict_sets_left) == 0

    
    def add_child(self, branch: any, conflict_set: list):
        """Adds a child.
        """
        conflict_sets_left = self.conflict_sets_left.copy()
        # Go over every conflict set backwards, removing those that contain the branch value
        for i in range(len(conflict_sets_left)-1,-1,-1):
            if branch in conflict_sets_left[i]:
                conflict_sets_left.pop(i)

        node = HittingNode(conflict_set, conflict_sets_left, self)
        self.children[branch] = node
        