#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(int argc, string argv[])
{
    string input_string = get_string("Text: ");
    int input_string_size = strlen(input_string);
    int sentences = 0;
    int words = 0;
    int letters = 0;

    // Check the end of the string
    if (input_string_size > 0)
    {
        for (int i = 0; i <= input_string_size; i++)
        {
            // Check the end of the senctance
            if (input_string[i] == '.' || input_string[i] == '!' || input_string[i] == '?')
            {
                sentences++;
            }
            // Check the end of the word
            else if (isspace(input_string[i]) || input_string[i] == '\0')
            {
                words++;
            }
            // Check a new letter
            else if (isalpha(input_string[i]))
            {
                letters++;
            }
        }
    }

    // Calculate the Coleman-Liau index of a text
    // Formula: index = 0.0588 * L - 0.296 * S - 15.8
    float L = (100.0 / (float) words) * (float) letters;
    float S = (100.0 / (float) words) * (float) sentences;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // Generate output text
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int) roundf(index));
    }
}