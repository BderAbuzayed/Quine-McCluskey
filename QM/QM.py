# Bder Abuzayed
# EEE 4334
# Quine–McCluskey algorithm in python
product_terms = []    #Our global list that stores all the minterms
essential_implicants = [] #changed to global variable to pass it on the function to produce the output

def create_prime_implicant_chart(minterms, prime_implicants):
    """Create the Prime Implicant Chart mapping minterms to prime implicants."""
    chart = {minterm: [] for minterm in minterms}

    # Check which prime implicants cover each minterm
    for minterm in minterms:
        for implicant in prime_implicants:
            if covers(minterm, implicant):
                chart[minterm].append(implicant)

    # Display the chart in a readable format
    #print("\nPrime Implicant Chart:")
    #print(f"{'Minterms':<15} | {'Prime Implicants':<50}")
    #print("-" * 70)
    #for minterm, implicants in chart.items():
       # print(f"{minterm:<15} | {', '.join(implicants):<50}")

    return chart

# Function to check if a prime implicant covers a minterm
def covers(minterm, implicant):
    
    for m_bit, i_bit in zip(minterm, implicant):
        if i_bit != '-' and m_bit != i_bit:
            return False
    return True

def select_essential_prime_implicants(prime_implicant_chart):
    essential_implicants = set()
    covered_minterms = set()

    # Go through each minterm in the chart
    for minterm, implicants in prime_implicant_chart.items():
        if len(implicants) == 1:  # If only one implicant covers the minterm
            essential_implicant = implicants[0]
            if essential_implicant not in essential_implicants:
                essential_implicants.add(essential_implicant)
                
            # Mark the minterm as covered
            covered_minterms.add(minterm)
    
    # Remove covered minterms from the chart for next round
    for minterm in covered_minterms:
        del prime_implicant_chart[minterm]
    
    return essential_implicants, prime_implicant_chart

def combine_terms(term1, term2):
    """Combine two minterms that differ by exactly one bit."""
    diff_count = 0
    combined = []

    # Check that both terms have the same length
    if len(term1) != len(term2):
        print(f"Error: Terms have different lengths: {term1} and {term2}")
        return None

    for bit1, bit2 in zip(term1, term2):
        if bit1 != bit2:
            diff_count += 1
            combined.append('-')  # Replace differing bit with '-'
        else:
            combined.append(bit1)

    # If they differ by exactly one bit, return the combined term
    if diff_count == 1:
        #print(f"Combined {term1} and {term2} to {''.join(combined)}")  # Debug print
        return ''.join(combined)
    else:
        return None


def combine_all_terms(minterms):
    """Combine minterms that differ by one bit, repeat until no more combinations can be made."""
    all_prime_implicants = []  # List to store prime implicants
    grouped_terms = group_minterms(minterms)  # Group terms by the number of 1s
    
    while grouped_terms:
        next_grouped_terms = {}  # Prepare for the next iteration
        used_terms = set()       # Track terms that were combined in this iteration
        prime_candidates = set()  # Track terms that remain unused

        # Iterate through adjacent groups to combine terms
        for num_ones in sorted(grouped_terms.keys()):
            if num_ones + 1 in grouped_terms:  # Check for adjacent groups
                for term1 in grouped_terms[num_ones]:
                    for term2 in grouped_terms[num_ones + 1]:
                        combined = combine_terms(term1, term2)
                        if combined:
                            group_key = combined.count('1')  # Group based on new count of 1s
                            if group_key not in next_grouped_terms:
                                next_grouped_terms[group_key] = []
                            if combined not in next_grouped_terms[group_key]:
                                next_grouped_terms[group_key].append(combined)
                            used_terms.add(term1)
                            used_terms.add(term2)
            
            # Track terms that were not combined
            for term in grouped_terms[num_ones]:
                if term not in used_terms:
                    prime_candidates.add(term)

        # Add unused terms as prime implicants
        all_prime_implicants.extend(prime_candidates)
        
        # Prepare for the next iteration
        grouped_terms = remove_duplicates(next_grouped_terms)

    return all_prime_implicants

def remove_duplicates(grouped_terms):
    for key in grouped_terms:
        grouped_terms[key] = list(set(grouped_terms[key]))
    return grouped_terms

def group_minterms(minterms):
    """Group minterms by the number of 1s in their binary representation."""
    groups = {}

    for term in minterms:
        # Remove the part after | (if exists), and only count the binary part
        term = term.split('|')[0]
        num_ones = term.count('1')
        if num_ones not in groups:
            groups[num_ones] = []
        groups[num_ones].append(term)
    
    return groups

def output_pla_format(inputs, outputs, essential_implicants, output_file):
    # Create the header for the PLA file
    pla_output = f".i {inputs}\n.o {outputs}\n.p {len(essential_implicants)}\n"
    
    # Generate the product terms for the essential prime implicants
    for implicant in essential_implicants:
        pla_output += implicant + "\n"

    # Mark the end of the product terms
    pla_output += ".e\n"
    
    # Print to terminal 
    print("\nPLA Format Output (Terminal):")
    print(pla_output)

    # Write the PLA format file
    try:
        with open(output_file, 'w') as file:
            file.write(pla_output)
        print(f"\nPLA file saved to {output_file}")
    except Exception as e:
        print(f"Error saving PLA file: {str(e)}")

def process_pla_file(file_path, output_file):
    inputs = None
    outputs = None
    global product_terms

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove whitespace. THIS STEP IS VERY IMPORTANT becasue it will mess up the parsing if not done correctly
                
                if line.startswith('.i'):
                    inputs = int(line.split()[1])  # No. of inputs

                elif line.startswith('.o'):
                    outputs = int(line.split()[1])  # No. of outputs

                elif line.startswith('.p'):
                    product_term_count = int(line.split()[1])  # Store product terms count
                # Parse product terms themselves
                elif "|" in line:
                    product_terms.append(line.split('|')[0].strip())  # Store product term


        # Limit the product terms to the first 10 for debugging
        # Save the product terms (just for debugging)
        #print(f"First 5 Product Terms (After Parsing): {product_terms[:10]}")  
        
        # Call process_product_terms to generate the essential prime implicants
        process_product_terms()

        # Output the PLA format using the essential prime implicants and save to the file
        output_pla_format(inputs, outputs, essential_implicants, output_file)

        # Output the results
        print(f"Inputs: {inputs}")
        print(f"Outputs: {outputs}")
        print(f"Minterms: {product_term_count}")
        #print(f"Product Terms: {product_terms}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError as ve:
        print(f"ValueError: {ve}. This typically happens if there's an issue with the data format in the file.")
    except Exception as e:
        print(f"An unexpected error occurred in process_pla_file: {str(e)}")

def process_product_terms():
    # Combine the product terms (we limit it to the first 5 for now)
    first_five_terms = product_terms[:] 
    #print(f"First 5 Product Terms: {first_five_terms}")  # Debugging line
    
    combined_terms = combine_all_terms(first_five_terms) # prime implicant generated and stored into combiner_terms
    
    # Output the results
    #print(f"Prime Implicants: {combined_terms}")

    # Create and display the Prime Implicant Chart
    prime_implicant_chart = create_prime_implicant_chart(first_five_terms, combined_terms)
    
    
    global essential_implicants  # Make essential_implicants accessible to the output function
    # Select essential prime implicants
    essential_implicants, remaining_chart = select_essential_prime_implicants(prime_implicant_chart)
    
    # Output the results
    print(f"Essential Prime Implicants: {essential_implicants}")
 
# The Code reads a static file that already exists. I will include the file in the Zip
process_pla_file('example_7inputs_99minterms.pla', 'output.pla')   # Calls the function to parse the input from the pla format
process_product_terms()  # Now call the function to combine the product terms