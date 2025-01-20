file = "C:\\Users\\Virasone\\Documents\\Giro\\advent-of-code-2024\\2\\data_small.txt"

# Find max length and number of sequences
max_length = -1
num_sequences = 0
with open(file, 'r') as f:
    for line in f:
        line_split = line.split()
        max_length = max(max_length, len(line_split))
        num_sequences += 1

# Print data formatted for Minizinc
sequences_data = "sequences = ["
white_space_padding = len(sequences_data)
first_line = True
with open(file, 'r') as f:
    for line in f:
        sequence = "|"

        # Get sequence numbers
        line_split = line.split()
        for i in range(len(line_split)):
            sequence += f'{line_split[i]}, '

        # Add padding numbers
        num_padding = max_length - len(line_split)
        for i in range(num_padding):
            sequence += f'0, '
        
        # Remove last comma
        sequence[:-2]

        if not first_line:
            sequences_data += white_space_padding * ' '
        sequences_data += f'{sequence}\n'

        first_line = False

sequences_data += white_space_padding * ' '
sequences_data += "|];"

# Write the data in a file
with open("minizinc_data.txt", "w") as f:
    f.write(f'max_length = {max_length};\n')
    f.write(f'num_sequences = {num_sequences};\n')
    f.write(sequences_data)
