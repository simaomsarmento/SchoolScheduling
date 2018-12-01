import main

example = 'Examples/example1_infeasible.txt'

input_file = open(example, 'r')
output_file = open('Examples/example1_infeasible_output.txt', 'w')

try:
    # do stuff with f
    main.solve(input_file, output_file)
finally:
    input_file.close()
    output_file.close()