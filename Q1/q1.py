import string

def shift_character(char, n, m):
    if char in string.ascii_lowercase:
        if char <= 'm':
            return chr(((ord(char) - ord('a') + n * m) % 26) + ord('a'))
        else:
            return chr(((ord(char) - ord('a') - (n + m)) % 26) + ord('a'))
    elif char in string.ascii_uppercase:
        if char <= 'M':
            return chr(((ord(char) - ord('A') - n) % 26) + ord('A'))
        else:
            return chr(((ord(char) - ord('A') + m**2) % 26) + ord('A'))
    else:
        return char

def reverse_shift_character(char, n, m):
    if char in string.ascii_lowercase:
        if char <= 'm':
            return chr(((ord(char) - ord('a') - n * m) % 26) + ord('a'))
        else:
            return chr(((ord(char) - ord('a') + (n + m)) % 26) + ord('a'))
    elif char in string.ascii_uppercase:
        if char <= 'M':
            return chr(((ord(char) - ord('A') + n) % 26) + ord('A'))
        else:
            return chr(((ord(char) - ord('A') - m**2) % 26) + ord('A'))
    else:
        return char

def encrypt_text(input_file, output_file, n, m):
    with open(input_file, 'r') as file:
        raw_text = file.read()

    encrypted_text = ''.join(shift_character(char, n, m) for char in raw_text)

    with open(output_file, 'w') as file:
        file.write(encrypted_text)

def decrypt_text(input_file, output_file, n, m):
    with open(input_file, 'r') as file:
        encrypted_text = file.read()

    decrypted_text = ''.join(reverse_shift_character(char, n, m) for char in encrypted_text)

    with open(output_file, 'w') as file:
        file.write(decrypted_text)

def check_correctness(raw_file, decrypted_file):
    with open(raw_file, 'r') as raw, open(decrypted_file, 'r') as decrypted:
        raw_text = raw.read()
        decrypted_text = decrypted.read()

    return raw_text == decrypted_text

# Example usage
if __name__ == "__main__":
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))

    encrypt_text('Q1//raw_text.txt', 'Q1//encrypted_text.txt', n, m)
    decrypt_text('Q1//encrypted_text.txt', 'Q1//decrypted_text.txt', n, m)

    if check_correctness('Q1//raw_text.txt', 'Q1//decrypted_text.txt'):
        print("Decryption is correct!")
    else:
        print("Decryption failed.")
