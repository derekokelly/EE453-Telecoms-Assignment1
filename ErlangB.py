# Imports
import math
import numpy
import scipy
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from phoneLine import PhoneLine

# Amount of phone lines
n = 25
# List of traffic for Erlang calculation
amount_of_calls = [10, 25, 50, 100, 250, 500, 1000, 2000]

# Main function
def main():
    
    print("\n------------------------\n")
    print("Simulating:")

    # Print amount of calls
    for call in amount_of_calls:
        print("Traffic:", call, "calls")
    
    # Print number of lines
    print("\nNumber of lines:", n)
    print("\n------------------------\n")

    num_sims = 10

    # Loop through different call amounts
    for num_calls in amount_of_calls:

        # Set sums of GOS to 0
        sum_erlang_gos = 0
        sum_sim_gos = 0

        # Loop through simulations
        for i in range(0, num_sims):
            # Putting this inside the above for loop clears the lines while moving on to the next simulation

            # Create phone lines array to hold PhoneLine objects
            phone_lines = []

            for i in range(0, n):
                # Store PhoneLine objects in array with 0 start time and 0 end time
                phone_lines.append(PhoneLine(0, 0))

            # Generate call start times based off a random uniform distribution, sorted by earliest start time
            call_start_times = sorted(numpy.random.uniform(0, 60, num_calls))
            # Generate call holding times based off gamma distribution with mean centred around 3 mins
            call_length = numpy.random.standard_gamma(3, num_calls)
            
            # Get average call length
            avg_call_length = (sum(call_length) / len(call_length))

            # Keep track of amount of calls accepted & rejected
            num_calls_accepted = 0
            num_calls_rejected = 0

            # Loop through calls
            for i in range(0, num_calls):
                call_accepted = False
                current_call_start_time = call_start_times[i]
                current_call_end_time = (call_start_times[i] + call_length[i])

                line_number = 0

                # Loop through phone lines
                for line in phone_lines:
                    line_number += 1

                    # Check if line is free
                    if line.end_time <= current_call_start_time:
                        line.start_time = current_call_start_time
                        line.end_time = current_call_end_time
                        call_accepted = True
                        # We don't need to check any more lines, so break from for loop
                        break

                # Tally calls accepted & rejected
                if call_accepted:
                        num_calls_accepted += 1
                else:
                        num_calls_rejected += 1

            # ErlangB calculation
            traffic = num_calls * (avg_call_length / 60)
            erlang_gos = ErlangB(n, traffic)

            # Simulation calculation
            sim_gos = num_calls_rejected/num_calls

            # Sum GOS values to find average later
            sum_erlang_gos += erlang_gos
            sum_sim_gos += sim_gos
        
        avg_erlang_gos = sum_erlang_gos / num_sims
        avg_sim_gos = sum_sim_gos / num_sims

        print("For", num_calls, "calls")
        print("Avg Erlang GOS:", avg_erlang_gos)
        print("Avg Simulated GOS:", avg_sim_gos, "\n")

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
