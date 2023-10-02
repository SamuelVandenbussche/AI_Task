from simpleai.search import CspProblem, backtrack

#de gebruiker voor een puzzel vragen en de input opsplitsen per spatie
puzzle = st.text_input("geef een cryptarithmetic puzzle: ").upper()
words = puzzle.split(" ")

#de input valideren 
if len(words) != 5 or words[1] != '+' or words[3] != '=':
    print("Invalid input. Please enter a cryptarithmetic puzzle with 2 factors.")
else:
    variables = []

    domains = {}
#alle unieke letters in de variables variabel steken
    for word in words:
        for char in word:
            if char != "=" and char != "+":
                variables += char
    variables = set(variables)
#de letters die eerst in het woord staan een range geven van 1 tot 9 en de rest 0 tot 9
    for word in words:
        for i, char in enumerate(word):
            if char != "=" and char != "+":
                if i == 0:
                    domains[char] = list(range(1, 10))
                else:
                    domains[char] = list(range(10))

#hier zorg ik ervoor dat de letters unieke waardes hebben
    def constraint_unique(variables, values):
        return len(values) == len(set(values))
#hier geef ik de woorden random waardes en het stopt wanneer de som klopt
    def constraint_add(variables, values):
        factor1 = ""
        factor2 = ""
        result = ""
        for char in words[0]:
            position = variables.index(char)
            factor1 += str(values[position])
        factor1 = int(factor1)
        for char in words[2]:
            position = variables.index(char)
            factor2 += str(values[position])
        factor2 = int(factor2)
        for char in words[4]:
            position = variables.index(char)
            result += str(values[position])
        result = int(result)
        return (factor1 + factor2) == result

    constraints = [
        (variables, constraint_unique),
        (variables, constraint_add),
    ]
    problem = CspProblem(variables, domains, constraints)

    output = backtrack(problem)
    #hier zorg ik ervoor dat de output visueel aantrekkelijk is
    if output:
        solution = {var: output[var] for var in variables}
        
        print("\nDigits Solution:")
        for word in words:
            for char in word:
                if char.isalpha():
                    print(solution[char], end=" ")
                else:
                    print(char, end=" ")
            print()

        print("\nLetters Solution:")
        for word in words:
            for char in word:
                if char.isalpha():
                    print(char, end=" ")
                else:
                    print(char, end=" ")
            print()
    else:
        print("No solution found.")
