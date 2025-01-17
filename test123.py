# Create lists of letters for easy lookup and shifting
lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def encrypt_text(text, n, m):
    result = ''
    for char in text:
        if char in lowercase:
            pos = lowercase.index(char)
            if char in lowercase[:13]:  # a to m
                # Shift forward by n * m
                new_pos = (pos + (n * m)) % 26
            else:  # n to z
                # Shift backward by n + m
                new_pos = (pos - (n + m)) % 26
            result += lowercase[new_pos]
            
        elif char in uppercase:
            pos = uppercase.index(char)
            if char in uppercase[:13]:  # A to M
                # Shift backward by n
                new_pos = (pos - n) % 26
            else:  # N to Z
                # Shift forward by m^2
                new_pos = (pos + (m ** 2)) % 26
            result += uppercase[new_pos]
            
        else:
            # Keep special characters unchanged
            result += char
            
    return result

def decrypt_text(text, n, m):
    result = ''
    for char in text:
        if char in lowercase:
            pos = lowercase.index(char)
            original_pos = (pos + (n * m)) % 26
            if lowercase[original_pos] in lowercase[:13]:  # was originally a-m
                # Reverse n * m shift
                new_pos = (pos - (n * m)) % 26
            else:  # was originally n-z
                # Reverse n + m shift
                new_pos = (pos + (n + m)) % 26
            result += lowercase[new_pos]
            
        elif char in uppercase:
            pos = uppercase.index(char)
            original_pos = (pos + n) % 26
            if uppercase[original_pos] in uppercase[:13]:  # was originally A-M
                # Reverse n shift
                new_pos = (pos + n) % 26
            else:  # was originally N-Z
                # Reverse m^2 shift
                new_pos = (pos - (m ** 2)) % 26
            result += uppercase[new_pos]
            
        else:
            result += char
            
    return result

# Get user inputs
text = input("Enter text to encrypt: ")
n = int(input("Enter n: "))
m = int(input("Enter m: "))

# Encrypt
encrypted = encrypt_text(text, n, m)
print("\nEncrypted text:", encrypted)

# Decrypt
decrypted = decrypt_text(encrypted, n, m)
print("Decrypted text:", decrypted)
print("Original matches decrypted:", text == decrypted)