def luhn_checksum(card_number):
    # Check Luhn checksum
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(card_number):
    # Validate Credit Card number using Luhn’s Algorithm
    return luhn_checksum(card_number) == 0


def check_credit_card_number_length(credit_card_number):
    # Check credit card number length
    credit_card_number_length = len(str(credit_card_number))
    if credit_card_number_length in (13, 15, 16):
        return True
    return False


def get_credit_card_issuers_name(credit_card_number):
    # Get credit card issuer's name
    if check_credit_card_number_length(credit_card_number) and is_luhn_valid(credit_card_number) and credit_card_number.isdigit():
        company_id = int(str(credit_card_number)[: 2])
        if company_id in (34, 37):
            return 'AMEX'
        elif company_id in (51, 52, 53, 54, 55):
            return 'MASTERCARD'
        elif(company_id - company_id % 10) / 10 == 4:
            return 'VISA'
    return 'INVALID'


# Request credit card number input
credit_card_number = input('Number: ')

# Print result to the screen
print(get_credit_card_issuers_name(credit_card_number))