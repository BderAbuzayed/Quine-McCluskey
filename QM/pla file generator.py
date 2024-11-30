import random

def create_pla(file_path, inputs, outputs, logic_table):
    with open(file_path, 'w') as file:
        # Write metadata
        file.write(f".i {inputs}\n")
        file.write(f".o {outputs}\n")
        file.write(f".p {len(logic_table)}\n")  
        
        # Write logic table
        for row in logic_table:
            file.write(f"{row['inputs']} |{row['outputs']}\n")
        
        file.write(".e\n")


def generate_random_logic_table(inputs, outputs):
    # Calculate minterm range based on 2^inputs
    lower_bound = (2**inputs - 1) // 2  # Floor of (2^inputs - 1) / 2
    upper_bound = 2**inputs - 1  # 2^inputs - 1
    
    # Ensure the number of minterms is within the specified range
    minterm_count = random.randint(lower_bound, upper_bound)
    
    # Generate random minterms and construct logic table
    minterms = random.sample(range(2**inputs), minterm_count)  # Random unique minterms

    # Sort the minterms in ascending order
    minterms.sort()
    
    # Convert sorted minterms to the logic table format
    logic_table = [{'inputs': format(minterm, f'0{inputs}b'), 'outputs': '1'} for minterm in minterms]
    
    return logic_table


# Example usage
inputs = 7  # Change this as needed
outputs = 1
logic_table = generate_random_logic_table(inputs, outputs)

# Dynamically generate file name using the 'inputs' value
file_name = f'random_{inputs}inputs.pla'
create_pla(file_name, inputs, outputs, logic_table)  # Generates the file with the dynamic name
