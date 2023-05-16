import socket
import textwrap
from cryptography.fernet import Fernet

# Define the reverse mapping rules
reverse_mapping = {
    -3: '00',
    -1: '01',
    1: '10',
    3: '11'
}


def quaternary_to_binary(quaternary_sequence):
    binary_sequence = ''
    for symbol in quaternary_sequence:
        binary_symbol = reverse_mapping[symbol]
        binary_sequence += binary_symbol
    return binary_sequence


def binary_to_text(binary_sequence):
    # split o binary_sequence em pedacos de tamaho 8
    binary_list = textwrap.wrap(binary_sequence, 8)
    text_message = ''
    for binary in binary_list:
        decimal = int(binary, 2)
        text_message += chr(decimal)
    return text_message


# Encryption key
encryption_key = b'ultrasuperdupersecretoxiii'

# Establish a socket connection
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_address = '0.0.0.0'  # Listen on all available network interfaces
receiver_port = 12345  # Choose the same port number used by the sender
receiver_endpoint = (receiver_address, receiver_port)
receiver_socket.bind(receiver_endpoint)
receiver_socket.listen(1)

print("Receiver is listening for incoming connections...")

# Accept the sender's connection
sender_socket, sender_address = receiver_socket.accept()
print("Connected to Sender:", sender_address)

# Receive the quaternary message from the sender
received_data = sender_socket.recv(1024).decode()
quaternary_message = eval(received_data)  # Convert the received string back to a list

# Convert quaternary message to binary
binary_message = quaternary_to_binary(quaternary_message)

# Remove trailing padding from binary message
binary_message = binary_message.rstrip('0')

# Convert binary message to encrypted message (bytes)
encrypted_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, 'big')

# Create an AES cipher instance with the encryption key
cipher = Fernet(encryption_key)

# Decrypt the message
decrypted_message = cipher.decrypt(encrypted_message)

# Convert the decrypted message to string
text_message = decrypted_message.decode()
print("Received Text Message:", text_message)

# Close the connection
sender_socket.close()
receiver_socket.close()
