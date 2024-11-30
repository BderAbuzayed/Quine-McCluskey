use strict;
use warnings;

# Initialize global variables
my @product_terms = ();  # Store all the minterms
my @essential_implicants = ();  # Store essential implicants

# Create the Prime Implicant Chart mapping minterms to prime implicants
sub create_prime_implicant_chart {
    my ($minterms_ref, $prime_implicants_ref) = @_;
    my %chart = ();  # Chart to store minterms and associated implicants

    # Check which prime implicants cover each minterm
    for my $minterm (@$minterms_ref) {
        for my $implicant (@$prime_implicants_ref) {
            if (covers($minterm, $implicant)) {
                push @{$chart{$minterm}}, $implicant;
            }
        }
    }
    
    return \%chart;
}

# Function to check if a prime implicant covers a minterm
sub covers {
    my ($minterm, $implicant) = @_;
    
    # Compare each bit of the minterm and implicant
    for my $i (0 .. length($minterm) - 1) {
        if (substr($implicant, $i, 1) ne '-' && substr($minterm, $i, 1) ne substr($implicant, $i, 1)) {
            return 0;  # False if the bits differ
        }
    }
    return 1;  # True if it covers
}

# Select essential prime implicants from the chart
sub select_essential_prime_implicants {
    my ($prime_implicant_chart_ref) = @_;
    my %covered_minterms = ();  # Keep track of covered minterms
    my @essential_implicants = ();  # List of essential implicants

    # Go through each minterm in the chart
    while (my ($minterm, $implicants_ref) = each %$prime_implicant_chart_ref) {
        if (@$implicants_ref == 1) {  # If only one implicant covers the minterm
            push @essential_implicants, $implicants_ref->[0];
            $covered_minterms{$minterm} = 1;
        }
    }

    # Remove covered minterms from the chart
    for my $minterm (keys %covered_minterms) {
        delete $prime_implicant_chart_ref->{$minterm};
    }

    # Return essential implicants and remaining chart
    return (\@essential_implicants, $prime_implicant_chart_ref);
}

# Combine two terms if they differ by exactly one bit
sub combine_terms {
    my ($term1, $term2) = @_;
    my $diff_count = 0;
    my @combined = ();

    for my $i (0 .. length($term1) - 1) {
        if (substr($term1, $i, 1) ne substr($term2, $i, 1)) {
            $diff_count++;
            push @combined, '-';  # Replace differing bit with '-'
        } else {
            push @combined, substr($term1, $i, 1);
        }
    }

    return $diff_count == 1 ? join('', @combined) : undef;
}

# Group minterms by the number of 1s in their binary representation
sub group_minterms {
    my ($minterms_ref) = @_;
    my %groups = ();

    for my $term (@$minterms_ref) {
        my $num_ones = $term =~ tr/1//;
        push @{$groups{$num_ones}}, $term;
    }

    return \%groups;
}

# Combine all terms by iterating through adjacent groups
sub combine_all_terms {
    my ($minterms_ref) = @_;
    my @all_prime_implicants = ();
    my $grouped_terms_ref = group_minterms($minterms_ref);

    while (keys %$grouped_terms_ref) {
        my %next_grouped_terms = ();
        my %used_terms = ();

        for my $num_ones (sort keys %$grouped_terms_ref) {
            if ($grouped_terms_ref->{$num_ones + 1}) {
                for my $term1 (@{$grouped_terms_ref->{$num_ones}}) {
                    for my $term2 (@{$grouped_terms_ref->{$num_ones + 1}}) {
                        my $combined = combine_terms($term1, $term2);
                        if ($combined) {
                            push @{$next_grouped_terms{($combined =~ tr/1//)}}, $combined;
                            $used_terms{$term1} = 1;
                            $used_terms{$term2} = 1;
                        }
                    }
                }
            }
        }

        # Add unused terms as prime implicants
        push @all_prime_implicants, grep { !$used_terms{$_} } map { @{$grouped_terms_ref->{$_}} } keys %$grouped_terms_ref;
        $grouped_terms_ref = \%next_grouped_terms;
    }

    return \@all_prime_implicants;
}

# Output PLA format with essential prime implicants
sub output_pla_format {
    my ($inputs, $outputs, $essential_implicants_ref, $output_file) = @_;
    
    # Handle empty essential implicants array
    my $pla_output = ".i $inputs\n.o $outputs\n.p " . scalar(@$essential_implicants_ref) . "\n";
    if (@$essential_implicants_ref) {
        $pla_output .= join("\n", @$essential_implicants_ref) . "\n";
    } else {
        $pla_output .= "\n";  # Handle empty case
    }
    $pla_output .= ".e\n";

    print "\nPLA Format Output (Terminal):\n$pla_output";

    # Write to the output file
    open my $fh, '>', $output_file or die "Could not open '$output_file' for writing: $!\n";
    print $fh $pla_output;
    close $fh;

    print "\nPLA file saved to $output_file\n";
}

# Process the input PLA file
sub process_pla_file {
    my ($file_path, $output_file) = @_;
    my @product_terms = ();
    my ($inputs, $outputs);

    open my $fh, '<', $file_path or die "Could not open '$file_path' for reading: $!\n";

    while (my $line = <$fh>) {
        chomp $line;
        if ($line =~ /^\.i\s+(\d+)/) {
            $inputs = $1;
        } elsif ($line =~ /^\.o\s+(\d+)/) {
            $outputs = $1;
        } elsif ($line =~ /^\.p\s+(\d+)/) {
            # We can ignore this part for now
        } elsif ($line =~ /\|/) {
            push @product_terms, (split /\|/, $line)[0];
        }
    }

    close $fh;

    # Validate product terms
    if (@product_terms == 0) {
        die "No product terms found in the PLA file!\n";
    }

    # Process the product terms to find the essential prime implicants
    my @prime_implicants = @{combine_all_terms(\@product_terms)};
    my $prime_implicant_chart_ref = create_prime_implicant_chart(\@product_terms, \@prime_implicants);
    my ($essential_implicants_ref, $remaining_chart_ref) = select_essential_prime_implicants($prime_implicant_chart_ref);

    # Output PLA format and save to file
    output_pla_format($inputs, $outputs, $essential_implicants_ref, $output_file);
}

# Main execution
process_pla_file('example_9minterms_1output.pla', 'output2.pla');