# Request pyramid's height
height = 0
while not (height > 0 and height < 9):
    height = input('Height: ')
    if height.isdigit():
        height = int(height)
    else:
        height = 0

# Render the pyramid
output = ''
for row in range(1, height + 1):
    line_output = ''
    for line_char in range(1, height + 3 + row):
        if (line_char <= height - row) or line_char in (height + 1, height + 2):
            line_output += ' '
        else:
            line_output += '#'
    output += line_output

    # Add new line character if not the last line
    if row < height:
        output += '\n'

# Print result to the screen
print(output)