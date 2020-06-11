#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Define Height variable
    int height;

    // Ask piramid's height until it's in a range from 1 to 8
    do
    {
        height = get_int("Height:\n");
    }
    while (height > 8 || height < 1);

    // Loop through rows of piramid
    for (int row = 0; row < height; row++)
    {
        // Loop through each character of piramid's row
        for (int i = 0; i < height + row + 3; i++)
        {
            // Print whitespaces in the beginning of each row
            if (i < height - row - 1)
            {
                printf(" ");
            }
            // Print whitespaces in the middle of each row
            else if (i == height || i == height + 1)
            {
                printf(" ");
            }
            // Otherwise print hashes
            else
            {
                printf("#");
            }
        }
        // Move to a new line
        printf("\n");
    }
}