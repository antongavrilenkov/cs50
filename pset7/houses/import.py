import sys
import cs50
import csv

# Check number of command-line arguments
n = len(sys.argv)
if n == 2:
    # Connect to students DB
    db = cs50.SQL("sqlite:///students.db")

    # Open CSV file
    with open(sys.argv[1], "r") as characters:
        # Create DictReader
        reader = csv.DictReader(characters)
        # Iterate over CSV file
        for row in reader:
            name = row["name"]

            # Parse first name, middle name and last name from name string
            nameArr = name.split()
            firstName = nameArr[0]
            middleName = nameArr[1] if len(nameArr) == 3 else None
            lastName = nameArr[2] if len(nameArr) == 3 else nameArr[1]

            house = row["house"]
            birth = row["birth"]

            # Insert values to DB from CSV row
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       firstName, middleName, lastName, house, birth)
else:
    print("error: Incorrect number of command-line arguments")
