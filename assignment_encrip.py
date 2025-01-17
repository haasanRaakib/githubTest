def encrypt_text(input_file, output_file, n, m):
    with open(input_file, 'r') as f:
        raw_text = f.read()

    encrypted_text = ''
    for char in raw_text:
        if 'a' <= char <= 'm':  # Lowercase letters in the first half
            shift = n * m
            encrypted_text += shift_character(char, shift, direction="right")
        elif 'n' <= char <= 'z':  # Lowercase letters in the second half
            shift = n + m
            encrypted_text += shift_character(char, shift, direction="left")
        elif 'A' <= char <= 'M':  # Uppercase letters in the first half
            shift = n
            encrypted_text += shift_character(char, shift, direction="left")
        elif 'N' <= char <= 'Z':  # Uppercase letters in the second half
            shift = m**2
            encrypted_text += shift_character(char, shift, direction="right")
        else:  # Special characters and numbers remain unchanged
            encrypted_text += char

    with open(output_file, 'w') as f:
        f.write(encrypted_text)


def decrypt_text(input_file, output_file, n, m):
    with open(input_file, 'r') as f:
        encrypted_text = f.read()

    decrypted_text = ''
    for char in encrypted_text:
        if 'A' <= char <= 'M':  # Uppercase letters in the first half
            shift = n
            decrypted_text += shift_character(char, shift, direction="right")
        elif 'N' <= char <= 'Z':  # Uppercase letters in the second half
            shift = m**2
            decrypted_text += shift_character(char, shift, direction="left")
        elif 'a' <= char <= 'm':  # Lowercase letters in the first half
            shift = n * m
            decrypted_text += shift_character(char, shift, direction="left")
        elif 'n' <= char <= 'z':  # Lowercase letters in the second half
            shift = n + m
            decrypted_text += shift_character(char, shift, direction="right")

        else:  # Special characters and numbers remain unchanged
            decrypted_text += char

    with open(output_file, 'w') as f:
        f.write(decrypted_text)


def shift_character(char, shift, direction):
    """Shifts the character to the left or right within the alphabet."""
    alphabet = "abcdefghijklmnopqrstuvwxyz" if char.islower() else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    index = alphabet.index(char)

    if direction == "right":
        new_index = (index + shift) % 26
    elif direction == "left":
        new_index = (index - shift) % 26

    return alphabet[new_index]


def decryption_correctness(original_file, decrypted_file):
    with open(original_file, 'r') as f1, open(decrypted_file, 'r') as f2:
        original_text = f1.read()
        decrypted_text = f2.read()

    return original_text == decrypted_text





# Main Execution
input_file = 'D:/DOWNLOAD/raw_text.txt'
encrypted_file = 'D:/DOWNLOAD/encrypted_text.txt'
decrypted_file = 'D:/DOWNLOAD/decrypted_text.txt'

n = int(input("Enter the value of n: "))
m = int(input("Enter the value of m: "))

# Encryption of the text
encrypt_text(input_file, encrypted_file, n, m)
print(f"Text encrypted successfully. Encrypted text saved to {encrypted_file}.")

# Decryption of the text
decrypt_text(encrypted_file, decrypted_file, n, m)
print(f"Text decrypted successfully. Decrypted text saved to {decrypted_file}.")

# Checking the correctness
if decryption_correctness(input_file, decrypted_file):
    print("The decrypted text matches the original.")
else:
    print("The decrypted text does not match the original.")
