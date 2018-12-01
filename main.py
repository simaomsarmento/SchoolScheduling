import csp
from itertools import product

class Problem(csp.CSP):

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh and
        # set variables, domains, graph, and constraint_function accordingly
        T, R, S, W, A = self.load_information(fh)
        # Setting variables
        variables = W
        # Setting domains
        domains = dict()
        global_domain = list(product(T, R))
        for variable in variables:
            domains[variable] = global_domain.copy()
        # Setting graph
        graph = dict()
        for variable in variables:
            graph[variable] = [variable_aux for variable_aux in variables if variable_aux != variable]

        super().__init__(variables, domains, graph, self.constraints_function)
        self.A = A # adds information about course/class association
        self.day = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5}  # defining auxiliary dictionary for dates

    def load_information(self, fh):
        """
        Function to load information from input file and store on corresponding
        variables.
        :param fh: opened input file
        :return: T - list of tuples with possible time slots (d,t)
                 R - list of rooms
                 S - list of classes
                 W - list of tuples with weekly courses (c,k,i) - course/kind/index
                 A - class courses association (s,c)
        """
        info = fh.readlines()

        # verify file validity
        if len(info) == 5:
            pass
        else:
            exit('WRONG NUMBER OF LINES _ FILE MUST HAVE 5 LINES')

        # 1. Get time slots
        time_slots = info[0].rstrip().split(' ')[1:]
        T = [(slot.split(',')[0], slot.split(',')[1])  for slot in time_slots]
        T = sorted(T, key=lambda tup: tup[1]) # sort by hour so that earlier classes are evaluated first
        # 2. Get rooms
        R = info[1].rstrip().split(' ')[1:]
        # 3. Get classes
        S = info[2].rstrip().split(' ')[1:]
        # 4. Get weekly courses
        weekly_courses = info[3].rstrip().split(' ')[1:]
        W = [(course.split(',')[0], course.split(',')[1], course.split(',')[2])  for course in weekly_courses]
        # 5. Get class/courses association
        class_courses = info[4].rstrip().split(' ')[1:]
        A = [(assoc.split(',')[0], assoc.split(',')[1])  for assoc in class_courses]

        return T, R, S, W, A

    def constraints_function(self, A, a, B, b):
        """
        We must verify 3 conditions:
        1- if two courses are at the same time, the rooms must be different
        2- the same class cannot have two course at the same time
        3- the same course cannot have two of ocurrences of the same kind on the same day
        4- for the same course, the lower index must come before the greater index

        :param: A - (c,k,i) - c: course, k: kind, i: index
                a - (t, r) - t: time, r: room
                B - (c,k,i) - c: course, k: kind, i: index
                b - (t, r) - t: time, r: room
        :return: True or False
        """

        if a[0] == b[0]: # same time slot
            # Verify 1st constraint
            if a[1] == b[1]: # same room
                return False
            # Verify 2nd constraint
            if self.verify_class_colision(A[0], B[0]):
                return False

        if (A[0] == B[0]) and (A[1] == B[1]): # same course and same kind
            # Verify 3rd constraint
            if a[0][0] == b[0][0]: # a[0] represents (d,t) tuple. a[0][0] represents the day d
                return False
            # # Verify 4th constraint
            if ((A[2] > B[2]) and (self.day[a[0][0]]<self.day[b[0][0]])) or \
               ((A[2] < B[2]) and (self.day[a[0][0]]>self.day[b[0][0]])):
                return False
        return True

    def verify_class_colision(self, course1, course2):
        """
        Verify courses collision for same class

        :param course1
        :param course2
        :return: True if there is a class that has both courses else returns False
        """

        course1_classes = set()
        course2_classes = set()
        for assoc in self.A:
            if assoc[1] == course1:
                course1_classes.add(assoc[0])
            if assoc[1] == course2:
                course2_classes.add(assoc[0])

        # returns true if there is a collision
        if course1_classes.intersection(course2_classes) != set():
            return True

        return False

    def dump_solution(self, fh, solution):
        # Place here your code to write solution to opened file object fh
        for variable in self.variables:
            str_solution = variable[0]+','+variable[1]+','+variable[2]+' '+solution[variable][0][0]+','\
                           +solution[variable][0][1]+' '+solution[variable][1]+'\n'
            fh.write(str_solution)

        
def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)
    solution = csp.backtracking_search(p, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    if solution is None:
        output_file.write('None')
    else:
        p.dump_solution(output_file, solution)
