# Imports
import math
import random
import numpy
import scipy
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from phoneLine import PhoneLine

# Amount of phone lines
n = 30
# List of traffic for Erlang calculation
predicted_amount_of_calls = [500]

# Main function
def main():
    
    print("\n--------\n")

    # Print amount of calls & lines
    for call in predicted_amount_of_calls:
        print("Traffic: ", call, " calls")
        print("Number of lines: ", n)
        print("\n--------\n")
    
    # Generate call start times based off a random uniform distribution
    call_start_times = sorted(numpy.random.uniform(0, 60, call))
    # Generate call holding times based off gamma distribution
    call_length = numpy.random.standard_gamma(10, call)
    
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
        print("\n--------\n")
        print("Starting simulation on call ", i, "\n")
        call_accepted = False
        current_call_start = call_start_times[i]
        current_call_end = (call_start_times[i] + call_length[i])
        current_call_duration = call_length[i]

        print("Call start time:", current_call_start)
        print("Call end time:", current_call_end)
        print("Call duration:", current_call_duration)

        line_number = 0

        # Loop through phone lines
        for line in phone_lines:
            line_number += 1

            print("\nChecking line: ", line_number)
            print("Line call start time: ", line.call_start)
            print("Line call end time: ", line.call_end)

            # Check if line is free
            if line.call_end <= current_call_start:
                line.call_start = current_call_start
                line.call_end = current_call_end
                call_accepted = True
                print("\nCall accepted on line ", line_number)
                break
            else:
                # Check if we have lines left
                if line_number == n:
                    print("\nNo lines were free, call rejected.")
                else:
                    print("\nLine ", line_number, " is busy. Trying next line.")

        # Tally calls accepted & rejected
        if call_accepted:
                num_calls_accepted += 1
        else:
                num_calls_rejected += 1

    print("\n--------\n")

    print("Calls accepted: ", num_calls_accepted)
    print("Calls rejected: ", num_calls_rejected)

    # ErlangB calculation
    traffic = call * (ave_call_length / 60)
    erlang_gos = ErlangB(n, traffic)
    print("Erlang GOS: ", erlang_gos)
    print("Predicted GOS: ", (num_calls_rejected/call))

    print("\n--------\n")

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
