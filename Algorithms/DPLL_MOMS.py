import time
import tracemalloc
from pysat.formula import CNF
from collections import Counter

TIME_LIMIT = 1200  #time limit can be changed

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1]
        for clause in unit_clauses:
            unit = clause[0]
            assignment.append(unit)
            new_clauses = []
            for c in clauses:
                if unit in c:
                    continue
                if -unit in c:
                    new_clause = [l for l in c if l != -unit]
                    if not new_clause:
                        return None 
                    new_clauses.append(new_clause)
                else:
                    new_clauses.append(c)
            clauses = new_clauses
            changed = True
            break
    return clauses

def moms_variable(clauses):
    if not clauses:
        return None
    min_len = min(len(c) for c in clauses)
    min_clauses = [c for c in clauses if len(c) == min_len]

    counts = Counter()
    for clause in min_clauses:
        for lit in clause:
            counts[abs(lit)] += 1

    if counts:
        return counts.most_common(1)[0][0]
    return None

def dpll(clauses, assignment, start_time):
    
    if time.time() - start_time > TIME_LIMIT:
        return None  

    clauses = unit_propagate(clauses, assignment)
    if clauses is None:
        return False
    if not clauses:
        return True

    var = moms_variable(clauses)
    for val in [var, -var]:
        new_assignment = assignment.copy()
        new_assignment.append(val)
        new_clauses = [list(c) for c in clauses] + [[val]]
        result = dpll(new_clauses, new_assignment, start_time)
        if result:
            assignment[:] = new_assignment
            return True

    return False

def main():
    filename = "generated_problem.cnf"  
    cnf = CNF(from_file=filename)
    clauses = [list(clause) for clause in cnf.clauses]

    tracemalloc.start()
    start_time = time.time()

    assignment = []
    result = dpll(clauses, assignment, start_time)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"File: {filename}")
    print("Result:", "SAT" if result else "UNSAT")
    if result:
        print("Model:", assignment)
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB")

if __name__ == "__main__":
    main()
