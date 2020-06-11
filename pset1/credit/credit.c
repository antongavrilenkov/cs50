#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

string getCardIssuersName(long creditCardNumber);
int luhnCheck(const char *cc);
int checkCreditCardNumberLength(long creditCardNumber);

int main(void)
{
    // Define variables
    long creditCardNumber;
    char buffer[20];

    // Ask user to input his credit card number
    creditCardNumber = get_long("Number: ");
    sprintf(buffer, "%lu", creditCardNumber);

    // Validate Credit Card number using Luhn’s Algorithm
    if (!luhnCheck(buffer) || !checkCreditCardNumberLength(creditCardNumber))
    {
        printf("INVALID\n");
    }
    // If Credit Card number is Valid print
    // Credit Card's issuer name
    else
    {
        printf("%s\n", getCardIssuersName(creditCardNumber));
    }
}

string getCardIssuersName(long creditCardNumber)
{
    long tempNum = creditCardNumber;
    int companyId;

    // Get first two digits from Credit Card number
    while (tempNum >= 100)
    {
        tempNum = tempNum / 10;
        companyId = tempNum;
    }

    // Return Credit Card's issuer name
    if (companyId == 34 || companyId == 37)
    {
        return "AMEX";
    }
    else if (companyId == 51 || companyId == 52 || companyId == 53 || companyId == 54 || companyId == 55)
    {
        return "MASTERCARD";
    }
    else if ((companyId - companyId % 10) / 10 == 4)
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}

int checkCreditCardNumberLength(long creditCardNumber)
{
    if (creditCardNumber == 0)
    {
        return 0;
    }
    int nDigits = floor(log10(labs(creditCardNumber))) + 1;

    // Validate CC number length
    // American Express - 15-digit numbers, MasterCard - 16-digit numbers,
    // and Visa - 13 and 16-digit numbers
    if (nDigits != 13 && nDigits != 15 && nDigits != 16)
    {
        return 0;
    }
    return 1;
}

// Luhn's Algorithm implementation from rosettacode.org
// https://rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#C
int luhnCheck(const char *cc)
{
    const int m[] = {0, 2, 4, 6, 8, 1, 3, 5, 7, 9};
    int i, odd = 1, sum = 0;

    for (i = strlen(cc); i--; odd = !odd)
    {
        int digit = cc[i] - '0';
        sum += odd ? digit : m[digit];
    }

    return sum % 10 == 0;
}