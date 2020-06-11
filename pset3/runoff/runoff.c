#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // Check canditate's name is exist
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            // Check name of previous canditate is not the same
            for (int y = rank - 1; y >= 0; y--)
            {
                // Check if candidate's name was already used
                if (i == preferences[voter][y])
                {
                    return false;
                }
            }

            // Store the vote
            preferences[voter][rank] = i;

            return true;
        }
    }
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // Go through all voter preferences
    for (int i = 0; i < voter_count; i++)
    {
        int is_voted = 0;
        // Go trough all voter ranks
        for (int y = 0; y < candidate_count; y++)
        {
            // Check if voter has already vote
            if (is_voted == 0)
            {
                // Find a candidate with the highest rank and who is not eliminated from election
                if (!candidates[preferences[i][y]].eliminated)
                {
                    // Increase candidate's votes by one
                    candidates[preferences[i][y]].votes++;

                    // Set is_voted flag to 1 and / prevent using votes for candidates with lower rank
                    is_voted = 1;
                }
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // Define number of notes that enough for win in the election
    int votes_for_win = voter_count / 2 + 1;

    // Iterate all candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // Check if a candidate has enough votes to win an election
        if (!candidates[i].eliminated && candidates[i].votes >= votes_for_win)
        {
            // Print winner's name and return true
            printf("%s\n", candidates[i].name);
            return true;
        }
    }

    // Return false if nobody has enough votes to win an election
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // Initialize a variable that will contain minimum amount of votes
    int minimum_votes = -1;

    // Find a minimum amount of votes
    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && (minimum_votes == -1 || candidates[i].votes < minimum_votes))
        {
            minimum_votes = candidates[i].votes;
        }
    }

    // Return minimum amount of votes
    return (minimum_votes != -1) ? minimum_votes : 0;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        // Check if candidate has more votes than minimum
        // It means there is no tie in the election proccess
        if (!candidates[i].eliminated && min < candidates[i].votes)
        {
            return false;
        }
    }

    // There is tie in the election
    return true;
}

// Eliminate the candidate (or candidiates) in last place
void eliminate(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        // Check if current candidate is not already eliminated
        // and he has minimum amount of votes
        if (!candidates[i].eliminated && candidates[i].votes == min)
        {
            // Eliminate the candidate
            candidates[i].eliminated = true;
        }
    }
    return;
}