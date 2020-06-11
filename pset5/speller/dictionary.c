// Implements a dictionary's functionality
#define  _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in the hash table
// A good rule of thumb is to keep the load factor at 75% or less (some will say 70%)
// to maintain (very close to) O(1) lookup.
// Based on 143091 in large dictionary, you would want a minimum of about 107,318 buckets (for 75%), or 100163 buckets for 70%. That's assuming no collisions.
// Total time with 2 buckets: 5.64
// Total time with 107,318 buckets: 0.05

const unsigned int N = 107318;

// Hash table
node *table[N];

// Words in dictionary counter
int words_in_dictionary = 0;

// Add word to hash table function
bool add_word_to_hash_table(const char *word)
{
    // Check word is not equal to an empty string
    if (strcmp(word, "") != 0)
    {
        // Get hash value for the word
        long unsigned hash_value = hash(word);

        // Allocate memory for a new node
        node *el = (struct node *) malloc(sizeof(struct node));

        // Check if memory was allocated
        if (el == NULL)
        {
            fputs("Memory error", stderr);
            exit(2);
        }

        // Set values for created node
        strcpy(el->word, word);
        el->next = NULL;

        // Add new element to the bucket if the buket is empty
        if (table[hash_value] == NULL)
        {
            table[hash_value] = el;
        }
        // Otherwise add new element in the beginning of the singly linked list
        else
        {
            el->next = table[hash_value];
            table[hash_value] = el;
        }

        // Increase word in dictionary variable by 1
        words_in_dictionary++;
    }

    // Return success value
    return true;
}

// The strcmpi() function is same as that of the strcmp() function
// but the only difference is that strcmpi() function is not case sensitive
int strcmpi(const char *s1, const char *s2)
{
    int i;

    if (strlen(s1) != strlen(s2))
    {
        return -1;
    }

    for (i = 0; i < strlen(s1); i++)
    {
        if (toupper(s1[i]) != toupper(s2[i]))
        {
            return s1[i]-s2[i];
        }
    }
    return 0;
}

// Return true if word is in the dictionary otherwise return false
bool check(const char *word)
{
    // Get hash value for the word
    long unsigned hash_value = hash(word);

    // Iterate through all nodes in the bucket and find if the word is in dictionary
    node *next_element = table[hash_value];

    // Check if bucket is not empty
    if (next_element != NULL)
    {
        // Compare element's word value with checking word
        if (strcmpi(next_element->word, word) == 0)
        {
            return true;
        }

        // Check if elements has attached elements
        if (next_element->next != NULL)
        {
            // Go through all elements in the linked list
            while (next_element->next != NULL)
            {
                next_element = next_element->next;
                if (strcmpi(next_element->word, word) == 0)
                {
                    return true;
                }
            }
        }
    }

    // Word is not in dictionary
    return false;
}

// Hash word
// djb2 hash function from http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char *line = NULL;
    size_t len = 0;
    size_t read;

    // Hashtable
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Open dictionary
    FILE *fp = fopen(dictionary, "r");

    // Check if it was successfully opened otherwise return false
    if (fp == NULL)
    {
        return false;
    }

    // Read new words from the file with '\n' separator.
    while ((read = getline(&line, &len, fp)) != -1)
    {
        // Replace new line characters by end of the string character
        if (line[strlen(line) - 1] == '\n')
        {
            line[strlen(line) - 1] = '\0';
        }

        // Add word to the hash table
        add_word_to_hash_table(line);
    }

    // Free memory
    free(line);
    fclose(fp);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words_in_dictionary;
}

// Recursivly unload nodes from memory
void unload_nodes(node *el)
{
    if (el->next == NULL)
    {
        free(el);
    }
    else
    {
        unload_nodes(el->next);
        free(el);
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Go through each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Unload each element in the bucket recursively
        if (table[i] != NULL)
        {
            unload_nodes(table[i]);
        }
    }
    return true;
}
