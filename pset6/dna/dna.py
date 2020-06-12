import sys
import csv
import re

# Check if 3 arguments passed
if len(sys.argv) == 3:

    # Open sequence txt file
    with open(sys.argv[1], newline='') as csvfile:

        # Open a database csv file
        with open(sys.argv[2]) as fp:
            database = csv.DictReader(csvfile)
            strs = database.fieldnames[1:]
            sequence_content = fp.read()

            # Define STR counter list
            str_counter_list = []

            # Find repeated STR sequences
            for str_item in strs:
                repeat_counter = 1
                matched_times = 0

                while sequence_content.find(str_item * repeat_counter) > -1:
                    matched_times += 1
                    repeat_counter += 1

                # Add result to STR counter list
                str_counter_list.append(str(matched_times))

            # Count repeated strs
            str_found = 0
            for row in database:
                user_str = []
                candidates_name = None
                for i, item in enumerate(row.items()):
                    if item[0] != 'name':
                        user_str.append(item[1])
                    else:
                        candidates_name = item[1]

                if user_str == str_counter_list:
                    print(candidates_name)
                    str_found = 1
                    break
            if str_found == 0:
                print('No match')
else:
    print('Usage: python dna.py data.csv sequence.txt')