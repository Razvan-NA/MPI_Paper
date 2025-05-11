import time
import tracemalloc
from pysat.formula import CNF

TIME_LIMIT = 1200  #can change time limit in seconds

def resolve(clause1, clause2, var):
    resolvent = set(clause1).union(set(clause2))
    resolvent.discard(var)
    resolvent.discard(-var)
    return list(resolvent)

def eliminate_variable(clauses, var):
    pos_clauses = [c for c in clauses if var in c]
    neg_clauses = [c for c in clauses if -var in c]

    new_clauses = []
    for c1 in pos_clauses:
        for c2 in neg_clauses:
            resolvent = resolve(c1, c2, var)
            if not resolvent:
                return [], True  
            new_clauses.append(resolvent)

    remaining_clauses = [c for c in clauses if var not in c and -var not in c]
    return remaining_clauses + new_clauses, None

def dp(clauses, start_time):
    variables = set(abs(lit) for clause in clauses for lit in clause)

    while variables:
        
        if time.time() - start_time > TIME_LIMIT:
            print(f"Terminated after {TIME_LIMIT} seconds (time limit reached).")
            return None 

        var = variables.pop()
        clauses, conflict = eliminate_variable(clauses, var)
        if conflict is True:
            return False
        if not clauses:
            return True

    return True

def main():
    filename = "generated_problem.cnf"  
    cnf = CNF(from_file=filename)
    clauses = [list(clause) for clause in cnf.clauses]

    tracemalloc.start()
    start_time = time.time()

    result = dp(clauses, start_time)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"File: {filename}")
    if result is True:
        print("Result: SAT")
    elif result is False:
        print("Result: UNSAT")
    else:
        print("Result: UNKNOWN (time limit reached)")
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory Usage: {peak / 1024:.2f} KB")

if __name__ == "__main__":
    main()
