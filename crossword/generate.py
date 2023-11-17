import sys

from crossword import *
import math


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        print("Enforcing node consistency")

        
        for i in self.domains:
            for j in self.domains[i].copy():
                if len(j) != i.length:
                    self.domains[i].remove(j)
            #print(f"word lenght: {i.length}")
            #print(f"new domain: {self.domains[i]}")
            
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        print("Revising...")
        overlaps = self.crossword.overlaps
        ind = overlaps[(x,y)]
        if overlaps[(x,y)] is None: 
            return False
        xx = self.domains[x]
        yy = self.domains[y]
        c1 = 0
        for i in xx.copy():
            c = 0
            for j in yy:
                if i[ind[0]] == j[ind[1]]:
                    c += 1
            if c == 0:
                self.domains[x].remove(i)
                c1 += 1
        if c1 > 0: return True
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        print("Updating ARCS")
        if arcs is None: 
            #If arcs is None, your function should start with an initial queue of all of the arcs in the problem
            arcs = [] 
            for i in self.domains:
                for j in self.domains:
                    if i == j: 
                        continue
                    else:
                        arcs.append((i,j))    

        while arcs:
            i,j = arcs.pop()
            if self.revise(i,j):
                if not self.domains[i]:
                    return False
                for var in self.crossword.neighbors(i) - {j}:
                    arcs.append((var, i))
                    #print(f"adding to arcs, {var}, {i}")
        return True
       

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        print("Checking assignment status")
        for i in self.domains.keys():
            if i not in assignment.keys():
                return False
            else:
                if assignment[i] is None:
                    return False 
        print(assignment)
        print("Task Completed")
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        print("Checking consistency")
        #print(assignment)
        words = []
        for i in assignment:
            if assignment[i] in words:
                return False
            elif i.length != len(assignment[i]):
                return False
            
            for j in self.crossword.neighbors(i):
                if j in assignment:
                    overlaps = self.crossword.overlaps
                    ind = overlaps[(i,j)]
                    if assignment[i][ind[0]] == assignment[j][ind[1]]:
                        continue
                    else:
                        return False
        return True

                
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        print("Selecting order sorted values")
        rank = {}
        words = self.domains[var]
        nodes = self.crossword.neighbors(var)
        for i in words:
            if i in assignment:
                continue
            else: 
                c = 0 
                for j in nodes:
                    if i in self.domains[j]:
                        c += 1
                rank[i] = c
        #print(rank)
        return sorted(rank)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        print("Selecting unassigned variable")
        degree = 0
        value = math.inf
        for i in self.domains.keys():
            if i in assignment:
                continue
            else:
                if value > len(self.domains[i]):
                    value = len(self.domains[i])
                    variable = i
                    if self.crossword.neighbors(i) is None:
                        degree = 0
                    else:
                        degree = len(self.crossword.neighbors(i))
                elif value == len(self.domains[i]):
                    if self.crossword.neighbors(i) is not None:
                        if degree < len(self.crossword.neighbors(i)):
                            value = len(self.domains[i])
                            variable = i
                            degree = len(self.crossword.neighbors(i))
                        else:
                            variable = i
                            value = len(self.domains[i])
                            degree = 0    
        return variable 

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        print("Backtracking")
        #print(assignment)
        
        if self.assignment_complete(assignment):
            print("All done")
            return assignment
        
        word = self.select_unassigned_variable(assignment)
        for i in self.order_domain_values(word, assignment):
            assignment[word] = i

            if self.consistent(assignment):
                j = self.backtrack(assignment)
                if j: 
                    return j
            del assignment[word]
        return None

        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
