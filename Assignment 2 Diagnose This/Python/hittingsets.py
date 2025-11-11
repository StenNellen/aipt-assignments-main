from heuristics import shortest_conflict_set_heuristic, first_conflict_set_heuristic, longest_conflict_set_heuristic

# Main hitting set algorithm
def run_hitting_set_algorithm(conflict_sets, heuristic=shortest_conflict_set_heuristic) -> tuple[list, list]:
    """
    Algorithm that handles the entire process from conflict sets to hitting sets.

    Args:
        conflict_sets (list): A list of conflict sets.
        heuristic (function): The heuristic function to use for selecting the next conflict set. 
                              Defaults to shortest_conflict_set_heuristic.

    Returns:
        tuple: A tuple containing the list of hitting sets and minimal hitting sets.
    """
    initial_conflict_set = heuristic(conflict_sets)
    if not initial_conflict_set:
        return [], []

    # Start the tree with the root node
    root = HittingNode(initial_conflict_set, conflict_sets)
    
    # Create a list of nodes to be expanded (BFS)
    nodes_to_expand = [root]

    while nodes_to_expand:
        # Get the first node in the queue
        current_node = nodes_to_expand.pop(0)

        # If the node is terminal, we don't need to expand it further.
        if current_node.is_terminal():
            continue

        # For each branch in the current node's conflict set, create a child.
        for branch in current_node.get_branches():
            current_node.add_child(branch, heuristic)

            # Add the newly created child node to the queue to be processed.
            nodes_to_expand.append(current_node.children[branch])

    # Once the tree is fully expanded, collect the hitting sets.
    hitting_sets = root.get_hitting_sets()

    # Minimize the hitting sets
    minimal_hitting_sets = minimize_hitting_sets(hitting_sets)

    return hitting_sets, minimal_hitting_sets

# Optimized algorithm to minimize hitting sets.
# Instead of naively checking all subsets, we order the hitting sets by length only check new sets against the already confirmed minimal sets.
def minimize_hitting_sets(hitting_sets) -> list:
    """
    Function to minimize hitting sets.

    Args:
        hitting_sets (list): A list of hitting sets.

    Returns:
        list: A list of minimal hitting sets.
    """
    # Sort candidates by length.
    sorted_hs = sorted(hitting_sets, key=len)
    
    minimal_hs = []

    for hs_candidate in sorted_hs:
        is_minimal = True
        candidate_set = set(hs_candidate)

        # Check if the candidate is a superset of any already-confirmed minimal set.
        for minimal_set in minimal_hs:
            if set(minimal_set).issubset(candidate_set):
                is_minimal = False
                break  # Found a subset, so candidate is not minimal.
        
        if is_minimal:
            minimal_hs.append(hs_candidate)
            
    return minimal_hs


# Tree Structure for Hitting Set Algorithm
class HittingNode:
    """A node in the hitting set tree."""

    # Class variable to track number of nodes created for runtime analysis
    _nodes_created = 0

    def __init__(self, conflict_set: list[list], conflict_sets_left: list[list], parent=None):
        self.parent: HittingNode | None = parent
        self.conflict_sets_left: list[list] = conflict_sets_left
        self.conflict_set: list = conflict_set
        self.children: dict[any, HittingNode | None] = {c:None for c in conflict_set} if conflict_set else {}

        # Increment the node creation counter
        HittingNode._nodes_created += 1

    @classmethod
    def get_nodes_created(cls):
        """Returns the total number of nodes created since the last reset."""
        return cls._nodes_created

    @classmethod
    def reset_counter(cls):
        """Resets the node creation counter to zero."""
        cls._nodes_created = 0
    
    def get_hitting_sets(self) -> list[list]:
        """Collect all hitting sets assuming the tree is fully expanded.
        Each hitting set is represented as a list of branch elements.

        Returns:
            list[list]: the hitting sets
        """
        # Base case: if terminal, return an empty hitting set
        if self.is_terminal():
            return [[]]
        
        # Recursive case: collect hitting sets from children
        hitting_sets: list[list] = []
        for conflict, child in self.children.items():
            if child:
                for hs in child.get_hitting_sets():
                    hitting_sets.append([conflict] + hs)
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

    def add_child(self, branch: any, heuristic: callable):
        """Adds a child node by applying a heuristic.

        This method calculates the remaining conflicts for the child
        and uses the provided heuristic to select the child's own conflict set.

        Args:
            branch (any): The element from the parent's conflict set that defines this child.
            heuristic (callable): The function to select the next best conflict set.
        """
        # Calculate the child's specific list of remaining conflicts.
        conflict_sets_left = [cs for cs in self.conflict_sets_left if branch not in cs]

        # Apply the heuristic to this new list to find the best conflict set for the child.
        child_conflict_set = heuristic(conflict_sets_left)

        # Create the new child node with its own calculated data.
        node = HittingNode(child_conflict_set, conflict_sets_left, self)
        self.children[branch] = node
        