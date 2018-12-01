import main

example = 'Examples/test1.txt'

input_file = open(example, 'r')
output_file = open('Examples/test1_output.txt', 'w')

try:
    # do stuff with f
    main.solve(input_file, output_file)
finally:
    input_file.close()
    output_file.close()