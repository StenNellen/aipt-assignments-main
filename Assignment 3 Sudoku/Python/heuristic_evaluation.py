import os
import statistics
from Sudoku import Sudoku
from Game import BacktrackingGame
from Heuristics import heuristics_first, heuristics_smallestdomain, heuristics_largestdomain, heuristic_lowestfirstdomainfield

# Define Heuristics List, used for looping through later
heuristics_to_test = [
    ("First In First Out", heuristics_first),
    ("Smallest Domain Size", heuristics_smallestdomain),
    ("Largest Domain Size", heuristics_largestdomain),
    ("First Domain Field Value", heuristic_lowestfirstdomainfield)
]

def run_evaluation():
    folder = "Sudokus"
    
    # Dictionary to collect data, to keep track of labeled categories of data.
    summary_data = {
        name: {'visits': [], 'pruned': [], 'useless': [], 're-queued': [], 'efficiency': []}
        for name, _ in heuristics_to_test
    }

    # Print the detailed table header
    print(f"{'Sudoku File':<15} | {'Heuristic Name':<25} | {'Visits':<10} | {'Pruned':<10} | {'Useless':<10} | {'Re-queued':<10} | {'Efficiency %':<12}")
    print("-" * 115)

    # Perform evaluation on all sudokus, this loops through sudoku 1 to 5
    for i in range(1, 6):
        filename = f"Sudoku{i}.txt"
        filepath = os.path.join(folder, filename)

        # Print error
        if not os.path.exists(filepath):
            print(f"{filename:<15} | {'File not found':<25} | {'-':<10} | {'-':<10} | {'-':<10} | {'-':<10} | {'-':<12}")
            continue

        # Perform evaluation on all heuristics
        for name, heuristic_func in heuristics_to_test:
            try:
                # setup the sudoku file
                s = Sudoku(filepath)
                # Create an instance of the game class with the sudoku
                game = BacktrackingGame(s)
            except Exception as e:
                print(f"{filename:<15} | Error loading Sudoku: {e}")
                continue

            # Initialize metrics
            metrics = {'visits': 0, 'pruned': 0, 'useless': 0, 're-queued': 0}

            # Solve the sudoku with the selected heuristic
            try:
                success = game.solve(heuristic_func, metrics)
            except Exception as e:
                print(f"{filename:<15} | {name:<25} | Error: {e}")
                continue

            total_visits = metrics['visits'] # The total number of arc-processing iterations.
            pruned = metrics['pruned'] # The number of times constraints reduced a domain.
            # Re-queued - The number of arcs added back to the agenda after a domain reduction.
            # Useless - The number of checks where the arc was consistent and no changes were made.
            efficiency = (pruned / total_visits * 100) if total_visits > 0 else 0.0 # The ratio of successful prunings to total visits.

            # Collect data
            summary_data[name]['visits'].append(total_visits)
            summary_data[name]['pruned'].append(pruned)
            summary_data[name]['useless'].append(metrics['useless'])
            summary_data[name]['re-queued'].append(metrics['re-queued'])
            summary_data[name]['efficiency'].append(efficiency)

            # Print the detailed table row
            print(f"{filename:<15} | {name:<25} | {metrics['visits']:<10} | {metrics['pruned']:<10} | {metrics['useless']:<10} | {metrics['re-queued']:<10} | {efficiency:<12.2f}")

    # End of table
    print("-" * 115)
    print("\n")

    # Printing a summary table

    # Column widths
    w_name = 25
    w_metric = 20
    
    # Print title
    print("=" * (w_name + 5 * w_metric + 15))
    print(f"{'SUMMARY STATISTICS (Mean [Min - Max])':^{w_name + 5 * w_metric + 15}}")
    print("=" * (w_name + 5 * w_metric + 15))
    
    # Print headers
    header = f"{'Heuristic Name':<{w_name}} | {'Visits':<{w_metric}} | {'Pruned':<{w_metric}} | {'Useless':<{w_metric}} | {'Re-queued':<{w_metric}} | {'Efficiency %':<{w_metric}}"
    print(header)
    print("-" * len(header))

    # Loop over every result
    for name, stats in summary_data.items():
        if not stats['visits']: continue
        
        row_str = f"{name:<{w_name}}"
        
        # Order of columns to match header
        order = ['visits', 'pruned', 'useless', 're-queued', 'efficiency']
        
        # Create the metrics row string
        for metric in order:
            values = stats[metric]
            if not values:
                row_str += f" | {'-':<{w_metric}}"
                continue
            # Data saved as: Average [min, max]
            avg = statistics.mean(values) 
            minimum = min(values)
            maximum = max(values)
            
            if metric == 'efficiency': # Efficiency is a fraction, thus rounded to 1 decimal for min/max
                cell = f"{avg:.2f} [{minimum:.1f}-{maximum:.1f}]"
            else:
                cell = f"{int(avg)} [{minimum}-{maximum}]"
            
            row_str += f" | {cell:<{w_metric}}"
        
        # Print the row
        print(row_str)
    
    # End of table
    print("-" * len(header))

if __name__ == "__main__":
    run_evaluation()