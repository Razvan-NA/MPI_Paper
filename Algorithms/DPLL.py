import time
import tracemalloc
from pysat.formula import CNF

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
                        return None  # conflict
                    new_clauses.append(new_clause)
                else:
                    new_clauses.append(c)
            clauses = new_clauses
            changed = True
            break  
    return clauses

def dpll(clauses, assignment, start_time):
    if time.time() - start_time > TIME_LIMIT:
        return None 

    clauses = unit_propagate(clauses, assignment)
    if clauses is None:
        return False
    if not clauses:
        return True

    
    for clause in clauses:
        for literal in clause:
            var = abs(literal)
            break
        break

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
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB")

if __name__ == "__main__":
    main()
