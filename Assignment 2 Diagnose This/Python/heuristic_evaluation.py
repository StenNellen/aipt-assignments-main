from heuristics import shortest_conflict_set_heuristic, first_conflict_set_heuristic, longest_conflict_set_heuristic
from hittingsets import run_hitting_set_algorithm, HittingNode
from conflictsets import ConflictSetRetriever
from os.path import join
from statistics import mean, median

# Helper function to print evaluation summary
def print_evaluation_summary(results, num_documents):
    """Prints a formatted summary of the heuristic performances."""
    
    print("\n--- Heuristic Performance Summary ---")
    print(f"Evaluated on {num_documents} documents.\n")

    for name, data in results.items():
        nodes = data['nodes_created']
        print(f"Heuristic: '{name}'")
        print(f"  - Total Nodes Created: {sum(nodes):,}")
        print(f"  - Average Nodes Created: {mean(nodes):,.2f}")
        print(f"  - Median Nodes Created: {median(nodes):,.2f}")
        print(f"  - Min/Max Nodes Created: {min(nodes):,}/{max(nodes):,}")
        print("-" * 20)

    # Ensure all heuristics found the same number of minimal sets for each run.
    first_key = list(results.keys())[0]
    for key in results:
        if results[key]['minimal_hitting_sets_found'] != results[first_key]['minimal_hitting_sets_found']:
            print("\nWARNING: Mismatch in minimal hitting sets found. Check algorithm correctness.")
            break
    else:
        print("\nAll heuristics correctly found the same number of minimal hitting sets.")

    print("\n--- End of Evaluation ---")

# Advanced evaluation function
def run_evaluation(document_paths, heuristics_to_test):
    """
    Runs the hitting set algorithm for multiple circuits and heuristics,
    then prints a summary of the performance.

    Args:
        document_paths (list[str]): List of paths to the circuit files.
        heuristics_to_test (list[callable]): List of heuristic functions to evaluate.
    """
    results = {}

    for i, doc_path in enumerate(document_paths):
        
        # Retrieve conflict sets for the current document
        csr = ConflictSetRetriever(doc_path)
        conflict_sets = csr.retrieve_conflict_sets()

        if not conflict_sets:
            continue

        # Run each heuristic on this set of conflicts
        for heuristic in heuristics_to_test:
            HittingNode.reset_counter()
            _, minimal_hitting_sets = run_hitting_set_algorithm(conflict_sets, heuristic)
            nodes = HittingNode.get_nodes_created()
            
            # Save the results
            heuristic_name = heuristic.__name__
            if heuristic_name not in results:
                results[heuristic_name] = {
                    'nodes_created': [],
                    'minimal_hitting_sets_found': []
                }
            results[heuristic_name]['nodes_created'].append(nodes)
            results[heuristic_name]['minimal_hitting_sets_found'].append(len(minimal_hitting_sets))

    # Print the evaluation summary
    print_evaluation_summary(results, len(document_paths))


if __name__ == '__main__':
    # List of documents to evaluate
    documents = ["circuit1.txt", "circuit2.txt", "circuit3.txt", "circuit4.txt", "circuit5.txt", "circuit6.txt", "circuit7.txt"]

    # List of heuristics to compare
    heuristics_to_compare = [
        shortest_conflict_set_heuristic,
        longest_conflict_set_heuristic,
        first_conflict_set_heuristic
    ]

    # Run the advanced evaluation
    run_evaluation([join("circuits", doc) for doc in documents], heuristics_to_compare)