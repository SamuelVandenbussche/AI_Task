import streamlit as st
from simpleai.search import CspProblem, backtrack

# Function to solve the cryptarithmetic puzzle
def solve_puzzle(puzzle):
    words = puzzle.split(" ")
    if len(words) != 5 or words[1] != '+' or words[3] != '=':
        st.write("Invalid input. Please enter a cryptarithmetic puzzle with 2 factors.")
    else:
        variables = []
        domains = {}
    
        for word in words:
            for char in word:
                if char != "=" and char != "+":
                    variables += char
        variables = set(variables)
    
        for word in words:
            for i, char in enumerate(word):
                if char != "=" and char != "+":
                    if i == 0:
                        domains[char] = list(range(1, 10))
                    else:
                        domains[char] = list(range(10))
    
        def constraint_unique(variables, values):
            return len(values) == len(set(values))
    
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
        if output:
            solution = {var: output[var] for var in variables}
            return solution
        else:
            return None

# Streamlit app title and description
st.title("Cryptarithmetic Puzzle Solver")
st.write("Enter a cryptarithmetic puzzle in the format 'TO + GO = OUT'.")

# Input widget for the puzzle
puzzle = st.text_input("Enter the puzzle:")

# Button to solve the puzzle
if st.button("Solve"):
    if puzzle:
        solution = solve_puzzle(puzzle)
        if solution:
            st.write("Solution:")
            
            # Display the solution with words horizontally beneath each other
            st.write("Digits Solution:")
            digits_line = ""
            for word in puzzle.split():
                for char in word:
                    if char.isalpha():
                        digits_line += str(solution[char])
                    else:
                        digits_line += char
                st.write(digits_line)
                digits_line = ""
            
            st.write("Letters Solution:")
            letters_line = ""
            for word in puzzle.split():
                for char in word:
                    if char.isalpha():
                        letters_line += char
                    else:
                        letters_line += char
                st.write(letters_line)
                letters_line = ""
        else:
            st.write("No solution found.")
