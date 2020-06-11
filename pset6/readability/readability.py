def coleman_liau_index(letters, words, sentences):
    # Calculate the Coleman-Liau index of a text
    # Formula: index = 0.0588 * L - 0.296 * S - 15.8
    L = 100 / words * letters
    S = 100 / words * sentences
    index = (0.0588 * L) - (0.296 * S) - 15.8

    # Generate output text
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print("Grade " + str(round(index)))


# Define letters, words and sentences variables
letters, words, sentences = 0, 0, 0

# Request text from user
text = input('Text: ')

# Count letters, words and sentences
for character in text:
    if character in ('.', '!', '?'):
        sentences += 1
    elif character == ' ':
        words += 1
    elif character.isalpha():
        letters += 1
words += 1

# Print Coleman Liau Index resule to the screen
coleman_liau_index(letters, words, sentences)