import time
import tracemalloc
from pysat.formula import CNF

TIME_LIMIT = 1200

def resolve(ci, cj):
    resolvents = []
    for lit in ci:
        if -lit in cj:
            new_clause = set(ci).union(cj)
            new_clause.discard(lit)
            new_clause.discard(-lit)
            resolvents.append(frozenset(new_clause))
    return resolvents

def resolution(clauses, start_time):
    clauses = set(frozenset(clause) for clause in clauses)
    new = set()

    while True:
        # Frequent time check to make sure we don't exceed the time limit
        if time.time() - start_time > TIME_LIMIT:
            print(f"Terminated after {TIME_LIMIT} seconds.")
            return None
        
        pairs = [(ci, cj) for i, ci in enumerate(clauses) for j, cj in enumerate(clauses) if i < j]
        
        for ci, cj in pairs:
            # Check the time before each resolution step
            if time.time() - start_time > TIME_LIMIT:
                print(f"Terminated after {TIME_LIMIT} seconds.")
                return None
            
            resolvents = resolve(ci, cj)
            # Check the time after resolving a pair of clauses
            if time.time() - start_time > TIME_LIMIT:
                print(f"Terminated after {TIME_LIMIT} seconds.")
                return None
            
            for res in resolvents:
                # Check time after processing each resolvent
                if time.time() - start_time > TIME_LIMIT:
                    print(f"Terminated after {TIME_LIMIT} seconds.")
                    return None
                
                if not res:
                    return False  # Empty clause means UNSAT
                new.add(res)

        if new.issubset(clauses):
            return True  # No new clauses, hence satisfiable
        clauses.update(new)

def main():
    filename = "CBS_k3_n100_m403_b10_2.cnf"  # Put file name here
    cnf = CNF(from_file=filename)
    clauses = [list(clause) for clause in cnf.clauses]

    tracemalloc.start()
    start_time = time.time()

    result = resolution(clauses, start_time)

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
