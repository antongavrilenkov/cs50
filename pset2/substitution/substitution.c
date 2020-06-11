#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int is_valid_key(string key);
char encrypt_character(string cypher, char character);
int is_dublicate_characters(string array);

int main(int argc, string argv[])
{
    // Check there is only on parameter (encryption key) passed to the programm.
    if (argc == 2)
    {
        // Check encryption key is valid.
        if (!is_valid_key(argv[1]))
        {
            return 1;
        }

        // Ask user to enter a string for encryption
        string input_string = get_string("plaintext: ");

        int input_string_size = strlen(input_string);

        // Declare a retult variable
        char encrypted_string[input_string_size];

        // Iterate each character of the string for encryption
        for (int i = 0; i < input_string_size; i++)
        {
            // Encrypt a character and store it to encrypted_string variable
            encrypted_string[i] = encrypt_character(argv[1], input_string[i]);
        }
        // Add string break character at the end of encrypted_string char array
        encrypted_string[input_string_size] = '\0';

        // Print ecrypted string to the screen
        printf("ciphertext: %s\n", encrypted_string);

        // Return a success code 0
        return 0;
    }
    // Print usage instruction if passed parameters are incorrect
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
}

// Check an encryption key is valid
int is_valid_key(string key)
{
    if (strlen(key) != 26 || is_dublicate_characters(key))
    {
        printf("Key must contain 26 characters.\n");
        return 0;
    }

    // Check all key's characters are alphabet characters
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must contain 26 characters.\n");
            return 0;
        }
    }
    return 1;
}

// Encrypt character function
char encrypt_character(string cypher, char character)
{
    // Check if character is one of alphabet characters
    if (isalpha(character))
    {
        // Find character position in alphobet. A - 0, B - 1, Z - 25
        int character_alphabet_number = toupper(character) - 65;

        // Encrypt character using cypher key and apply toupper or tolower function depends in original input
        return (isupper(character)) ? toupper(cypher[character_alphabet_number]) : tolower(cypher[character_alphabet_number]);
    }
    else
    {
        // If character is not in alphabet return it without encryption
        return character;
    }
}

// Check dublicate characters in array
int is_dublicate_characters(string key)
{
    int count = strlen(key);
    for (int i = 0; i < count - 1; i++)
    {
        for (int j = i + 1; j < count; j++)
        {
            if (key[i] == key[j])
            {
                return 1;
            }
        }
    }
    return 0;
}