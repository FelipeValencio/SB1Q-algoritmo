import socket
from cryptography.fernet import Fernet

# Define the mapping rules
mapping = {
    '00': -3,
    '01': -1,
    '10': 1,
    '11': 3
}


def binary_to_quaternary(binary_sequence):
    quaternary_sequence = []
    for i in range(0, len(binary_sequence), 2):
        bits = binary_sequence[i:i + 2]
        quaternary_symbol = mapping[bits]
        quaternary_sequence.append(quaternary_symbol)
    return quaternary_sequence


# Encryption key
encryption_key = b'ultrasuperdupersecretoxiii'

# Establish a socket connection
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_address = '192.168.100.72'  # Replace with the actual IP address of Machine B
receiver_port = 12345  # Choose a suitable port number
receiver_endpoint = (receiver_address, receiver_port)
sender_socket.connect(receiver_endpoint)

# Example usage
# Get the text message from the user
text_message = input("Enter the text message: ")

print("Mensagem escrita: " + text_message)

# Create an AES cipher instance with the encryption key
cipher = Fernet(encryption_key)

# Encrypt the text message
padded_message = text_message.encode().ljust(16)
encrypted_message = cipher.encrypt(text_message.encode())

print("Mensagem criptografada: " + str(encrypted_message))

# Convert text message to binary data
binary_data = ' '.join(format(byte, '08b') for byte in encrypted_message)

print("Mensagem binario: " + str(binary_data))

quaternary_data = binary_to_quaternary(binary_data)

print("Mensagem algoritmo: " + str(quaternary_data))

# Send the quaternary data to the receiver
sender_socket.sendall(str(quaternary_data).encode())

# Close the socket connection
sender_socket.close()
