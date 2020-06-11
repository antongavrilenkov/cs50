#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int y = 0; y < width; y++)
        {
            // Calculate average value of original red, green and blue colors
            // and assign it as a new value for red green and blue
            float averageColor = (float)(image[i][y].rgbtRed + image[i][y].rgbtGreen + image[i][y].rgbtBlue) / 3;
            image[i][y].rgbtRed = round(averageColor);
            image[i][y].rgbtGreen = round(averageColor);
            image[i][y].rgbtBlue = round(averageColor);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int y = 0; y < width; y++)
        {
            // Calculate a new value of red, green and blue colors using a formula:
            // sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
            // sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
            // sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue
            float sepiaRed = 0.393 *  image[i][y].rgbtRed + 0.769 * image[i][y].rgbtGreen + 0.189 * image[i][y].rgbtBlue;
            float sepiaGreen = 0.349 *  image[i][y].rgbtRed + 0.686 * image[i][y].rgbtGreen + 0.168 * image[i][y].rgbtBlue;
            float sepiaBlue = 0.272 *  image[i][y].rgbtRed + 0.534 * image[i][y].rgbtGreen + 0.131 * image[i][y].rgbtBlue;
            image[i][y].rgbtRed = sepiaRed > 255 ? 255 : round(sepiaRed);
            image[i][y].rgbtGreen = sepiaGreen > 255 ? 255 : round(sepiaGreen);
            image[i][y].rgbtBlue = sepiaBlue > 255 ? 255 : round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int pointer_a = 0;
        int pointer_b = width - 1;

        // Mirror image pixels. Switch right and left pixels
        while (pointer_a < pointer_b)
        {
            // Declare temparary variables and copy RGB values of pointer_a to the temparary variables
            int tempRed =  image[i][pointer_a].rgbtRed;
            int tempGreen =  image[i][pointer_a].rgbtGreen;
            int tempBlue =  image[i][pointer_a].rgbtBlue;

            // Copy RGB values of pointer_b to RGB values of pointer_a
            image[i][pointer_a].rgbtRed =  image[i][pointer_b].rgbtRed;
            image[i][pointer_a].rgbtGreen =  image[i][pointer_b].rgbtGreen;
            image[i][pointer_a].rgbtBlue =  image[i][pointer_b].rgbtBlue;

            // Copy values from temparary variables to pointer_b RGB values
            image[i][pointer_b].rgbtRed =  tempRed;
            image[i][pointer_b].rgbtGreen =  tempGreen;
            image[i][pointer_b].rgbtBlue =  tempBlue;

            // Move pointers to next pixel
            pointer_a++;
            pointer_b--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // The new value of each pixel would be the average of
    // the values of all of the pixels that are within 1 row
    // and column of the original pixel (forming a 3x3 box).
    int resultImg[height][width][3];

    for (int i = 0; i < height; i++)
    {
        for (int y = 0; y < width; y++)
        {
            // Initialize Start and End coordinates for the 3x3 box
            int start_pixel_row = i - 1;
            int start_pixel_column = y - 1;
            int end_pixel_row = i + 1;
            int end_pixel_column = y + 1;

            // Override Start and End coordinates for pixels:
            // first / last row or first / last column

            // First row pixels
            if (i == 0)
            {
                start_pixel_row = i;
            }
            // Last row pixels
            else if (i == height - 1)
            {
                end_pixel_row = i;

            }

            // First column pixels
            if (y == 0)
            {
                start_pixel_column = y;
            }
            // Last column pixels
            else if (y == width - 1)
            {
                end_pixel_column = y;
            }

            // Find an average rgb value of all pixels in the 3x3 box
            int pixel_counter = 0;
            int red_sum = 0;
            int green_sum = 0;
            int blue_sum = 0;

            for (int r = start_pixel_row; r <= end_pixel_row; r++)
            {
                for (int c = start_pixel_column; c <= end_pixel_column; c++)
                {
                    red_sum += image[r][c].rgbtRed;
                    green_sum += image[r][c].rgbtGreen;
                    blue_sum += image[r][c].rgbtBlue;
                    pixel_counter++;
                }
            }

            float average_red = (float) red_sum / pixel_counter;
            float average_green = (float) green_sum / pixel_counter;
            float average_blue = (float) blue_sum / pixel_counter;

            // Store into temparary multidimensional array
            resultImg[i][y][0] = round(average_red);
            resultImg[i][y][1] = round(average_green);
            resultImg[i][y][2] = round(average_blue);
        }
    }

    // Replace original pixels by pixels from temparary array
    for (int i = 0; i < height; i++)
    {
        for (int y = 0; y < width; y++)
        {
            image[i][y].rgbtRed = resultImg[i][y][0];
            image[i][y].rgbtGreen = resultImg[i][y][1];
            image[i][y].rgbtBlue = resultImg[i][y][2];
        }
    }

    return;
}