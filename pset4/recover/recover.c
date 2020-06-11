#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }

    fseek(inptr, 0L, SEEK_END);
    long sz = ftell(inptr);
    rewind(inptr);

    // Allocate memory to contain the whole file:
    BYTE *buffer = (BYTE *) malloc(sizeof(BYTE) * sz);
    if (buffer == NULL)
    {
        fputs("Memory error", stderr);
        exit(2);
    }

    int imageCount = 0;
    char filename[8];
    FILE *outptr = NULL;

    while (true)
    {
        // Read a block of the memory card image
        size_t bytesRead = fread(buffer, sizeof(BYTE), BLOCK_SIZE, inptr);

        // Break out of the loop when we reach the end of the card image
        if (bytesRead == 0 && feof(inptr))
        {
            break;
        }

        // Check if we found a JPEG
        bool containsJpegHeader = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;

        // If we found a yet another JPEG, we must close the previous file
        if (containsJpegHeader && outptr != NULL)
        {
            fclose(outptr);
            imageCount++;
        }

        // If we found a JPEG, we need to open the file for writing
        if (containsJpegHeader)
        {
            sprintf(filename, "%03i.jpg", imageCount);
            outptr = fopen(filename, "w");
        }

        // Write anytime we have an open file
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(BYTE), bytesRead, outptr);
        }
    }

    fclose(inptr);
    free(buffer);
    return 0;
}