import sys
import cs50

n = len(sys.argv)
if n == 2:
    # Connect to students DB
    db = cs50.SQL("sqlite:///students.db")
    studentsInHouse = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last ASC, first ASC", sys.argv[1])

    for row in studentsInHouse:
        # Construct full name text output
        fullName = row["first"] + " " + row["middle"] + " " + \
            row["last"] if row["middle"] != None else row["first"] + " " + row["last"]

        # Construct birth year text output
        bornText = "born " + str(row["birth"])

        # Print output to the screen
        print(fullName + ", " + bornText)
else:
    print("error: Incorrect number of command-line arguments")
