# Imports
import math
import random
import numpy
import scipy
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from phoneLine import PhoneLine

# Amount of phone lines
n = 25
# List of traffic for Erlang calculation
amount_of_calls = [500]

# Main function
def main():
    
    print("\n----------------\n")

    # Print amount of calls
    for call in amount_of_calls:
        print("Traffic:", call, "calls")
    
    # Print number of lines
    print("Number of lines:", n)
    print("\n----------------\n")
    
    # Generate call start times based off a random uniform distribution, sorted by earliest start time
    call_start_times = sorted(numpy.random.uniform(0, 60, call))
    # Generate call holding times based off gamma distribution with mean centred around 3 mins
    call_length = numpy.random.standard_gamma(3, call)
    
    # Get average call length
    ave_call_length = (sum(call_length) / len(call_length))

    phone_lines = []

    for i in range(0, n):
        # Store PhoneLine objects in array with 0 start time and 0 end time
        phone_lines.append(PhoneLine(0, 0))

    # Keep track of amount of calls accepted & rejected
    num_calls_accepted = 0
    num_calls_rejected = 0

    # Loop through calls
    for i in range(0, call):
        call_accepted = False
        current_call_start = call_start_times[i]
        current_call_end = (call_start_times[i] + call_length[i])

        line_number = 0

        # Loop through phone lines
        for line in phone_lines:
            line_number += 1

            # Check if line is free
            if line.call_end <= current_call_start:
                line.call_start = current_call_start
                line.call_end = current_call_end
                call_accepted = True
                break

        # Tally calls accepted & rejected
        if call_accepted:
                num_calls_accepted += 1
        else:
                num_calls_rejected += 1

    print("Calls rejected:", num_calls_rejected, "/ 500")

    # ErlangB calculation
    traffic = call * (ave_call_length / 60)
    erlang_gos = ErlangB(n, traffic)
    print("Erlang GOS:", erlang_gos)
    print("Simulated GOS:", (num_calls_rejected/call))

    print("\n----------------\n")

# ErlangB formula
def ErlangB (n, A0):
    numerator = (A0**n / math.factorial(n))
    sum_ = 0
    for i in range(0, n + 1):
        sum_ += (A0**i) / math.factorial(i)
    return (numerator / sum_)

# Call main
if __name__ == '__main__':
    main()
