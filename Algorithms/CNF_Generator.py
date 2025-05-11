import random

def generate_clause(num_vars, max_clause_length=10):
    clause_length = random.randint(3, min(max_clause_length, num_vars // 2))
    clause = set()
    while len(clause) < clause_length:
        var = random.randint(1, num_vars)
        lit = var if random.choice([True, False]) else -var
        clause.add(lit)

    return list(clause)

def generate_cnf_problem(num_vars, num_clauses, max_clause_length=10):
    clauses = [generate_clause(num_vars, max_clause_length) for _ in range(num_clauses)]
    for _ in range(num_clauses // 3):  
        clause1 = random.choice(clauses)
        clause2 = random.choice(clauses)
        clause = [random.choice(clause1), random.choice(clause2), random.choice(clause1)]
        clauses.append(clause)

    return clauses

def write_dimacs(filename, problems, num_vars_list):
    with open(filename, "w") as f:
        for i, (clauses, num_vars) in enumerate(zip(problems, num_vars_list), 1):
            f.write(f"c Problem {i}\n")
            f.write(f"p cnf {num_vars} {len(clauses)}\n")
            for clause in clauses:
                f.write(" ".join(str(lit) for lit in clause) + " 0\n")
            f.write("\n")  

def main():
    filename = "generated_problem.cnf"
    problems = []
    num_vars_list = []

    print("Generating CNF problem...")
    num_vars = int(input(f"Enter number of variables for problem: "))
    num_clauses = int(input(f"Enter number of clauses for problem: "))
    problem = generate_cnf_problem(num_vars, num_clauses, max_clause_length=15) 
    problems.append(problem)
    num_vars_list.append(num_vars)

    write_dimacs(filename, problems, num_vars_list)
    print(f"\nDone! CNF file with problems saved as '{filename}'")

if __name__ == "__main__":
    main()
