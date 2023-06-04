import base64
import socket
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt

# Define the mapping rules
mapping = {
    '00': 1,
    '01': 3,
    '10': -1,
    '11': -3
}

bits_graph = []


def binary_to_quaternary(binary_sequence):
    quaternary_sequence = []
    previous = 1  # 1 para positivo, 0 para negativo
    for i in range(0, len(binary_sequence), 2):
        bits = binary_sequence[i:i + 2]
        bits_graph.append(bits)
        quaternary_symbol = mapping[bits] if previous is 1 else -mapping[bits]
        if quaternary_symbol > 0:
            previous = 1
        else:
            previous = 0
        quaternary_sequence.append(quaternary_symbol)
    return quaternary_sequence


# Generate a new encryption key
encryption_key = Fernet.generate_key()
encryption_key_encoded = base64.urlsafe_b64encode(encryption_key)

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
binary_data = ''.join(format(byte, '08b') for byte in encrypted_message)

print("Mensagem binario: " + str(binary_data))

quaternary_data = binary_to_quaternary(binary_data)

print("Mensagem algoritmo: " + str(quaternary_data))

x = bits_graph

# Generate the y-axis values (signal amplitudes)
y = quaternary_data

# Plot the signal graph
plt.plot(x, [-3, -1, 1, 3])
plt.axis(y)
plt.xlabel('Symbol Index')
plt.ylabel('Signal Amplitude')
plt.title('2B1Q Signal Graph')
plt.grid(True)

# Display the graph
plt.show()

# Send the quaternary data to the receiver
sender_socket.sendall(str(quaternary_data).encode())
sender_socket.sendall(encryption_key_encoded)

# Close the socket connection
sender_socket.close()
