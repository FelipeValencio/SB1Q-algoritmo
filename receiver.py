import base64
import socket
import textwrap
from cryptography.fernet import Fernet
import ast
import matplotlib.pyplot as plt

# Define the reverse mapping rules
reverse_mapping_previous_positive = {
    1: '00',
    3: '01',
    -1: '10',
    -3: '11'
}

reverse_mapping_previous_negtative = {
    -1: '00',
    -3: '01',
    1: '10',
    3: '11'
}


def quaternary_to_binary(quaternary_sequence):
    binary_sequence = ''
    previous = 1  # 1 para positivo, 0 para negativo
    for symbol in quaternary_sequence:
        if previous == 1:
            binary = reverse_mapping_previous_positive[symbol]
        else:
            binary = reverse_mapping_previous_negtative[symbol]
        if symbol > 0:
            previous = 1
        else:
            previous = 0
        binary_sequence += binary
    return binary_sequence


def binary_to_text(binary_sequence):
    # split o binary_sequence em pedacos de tamaho 8
    binary_list = textwrap.wrap(binary_sequence, 8)
    text_message = ''
    for binary in binary_list:
        decimal = int(binary, 2)
        text_message += chr(decimal)
    return text_message

    # Establish a socket connection


receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_address = '0.0.0.0'  # Listen on all available network interfaces
receiver_port = 12345  # Choose the same port number used by the sender
receiver_endpoint = (receiver_address, receiver_port)
receiver_socket.bind(receiver_endpoint)
receiver_socket.listen(1)
while True:
    print("Receiver is listening for incoming connections...")

    # Accept the sender's connection
    sender_socket, sender_address = receiver_socket.accept()
    print("Connected to Sender:", sender_address)

    # Receive the quaternary message from the sender
    received_data = sender_socket.recv(8192).decode()
    received_data_message = received_data.split("]")[0] + ']'
    quaternary_message = ast.literal_eval(received_data_message)  # Safely evaluate the received string as a list
    print("Mensagem algoritmo: " + str(quaternary_message))

    # Receive the encryption key from the sender
    encryption_key_encoded = received_data.split("]")[1]
    encryption_key = base64.urlsafe_b64decode(encryption_key_encoded)

    # Convert quaternary message to binary
    binary_message = quaternary_to_binary(quaternary_message)

    # Remove trailing padding from binary message
    binary_message = binary_message.rstrip('0')
    print("Mensagem binario: " + str(binary_message))

    # Convert binary message to encrypted message (bytes)
    encrypted_message = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, 'big')
    print("Mensagem criptografada: " + str(encrypted_message))

    # Create an AES cipher instance with the encryption key
    cipher = Fernet(encryption_key)

    # Decrypt the message
    try:
        decrypted_message = cipher.decrypt(encrypted_message)
        # Convert the decrypted message to string
        text_message = decrypted_message.decode()
        print("Received Text Message:", text_message)
    except:
        print("Decryption failed. Incorrect encryption key or padding.")

    # Close the connection
    sender_socket.close()

    bits = []
    for i in range(0, len(binary_message), 2):
        bits.append(binary_message[i:i + 2])
    binary_codes = bits

    x = range(len(binary_codes))
    x_labels = [''.join(code) for code in binary_codes]

    plt.figure(figsize=(100, 6))

    # Plot lines with markers
    plt.step(x, quaternary_message, where='post')

    # Set X and Y axis labels, title, and grid
    plt.xlabel('Binary Codes')
    plt.ylabel('Code Values')
    plt.title('2B1Q Code Mapping')
    # Set X-axis tick locations and labels
    plt.xticks(x, x_labels, rotation='vertical')
    y_tick_values = [-3, -1, 1, 3]
    plt.yticks(y_tick_values)

    plt.grid(True)

    # Display the graph
    plt.show()
