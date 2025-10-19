#Description: Converts a given text message to Morse code and vice versa. The program should be able to encode and decode Morse code.

morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/'
}

def encode_morse(text):
    return ' '.join(morse_code_dict.get(i.upper(), '') for i in text)

def decode_morse(morse):
    inverse_dict = {v: k for k, v in morse_code_dict.items()}
    return ''.join(inverse_dict.get(i, '') for i in morse.split())

# Input and Output
choice = input("Choose operation: Encode or Decode (E/D): ").upper()

if choice == 'E':
    text = input("Enter text to encode: ")
    print(f"Encoded Morse code: {encode_morse(text)}")
elif choice == 'D':
    morse = input("Enter Morse code to decode: ")
    print(f"Decoded text: {decode_morse(morse)}")
else:
    print("Invalid choice.")
