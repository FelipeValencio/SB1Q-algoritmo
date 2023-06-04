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
        quaternary_symbol = mapping[bits] if previous == 1 else -mapping[bits]
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

# Send the quaternary data to the receiver
sender_socket.sendall(str(quaternary_data).encode())
sender_socket.sendall(encryption_key_encoded)

# Close the socket connection
sender_socket.close()

# Generate the x-axis values (binary sequence)
bits = []
for i in range(0, len(binary_data), 2):
    bits.append(binary_data[i:i + 2])
x_axis_values = list(bits)

# Custom X and Y axis values
y_axis_values = [-3, -1, 1, 3]

# Data points
data_points = []
for i in range(0, len(x_axis_values)):
    data_points.append((quaternary_data[i], x_axis_values[i]))

# Extract X and Y coordinates from data points
x = [point[1] for point in data_points]
y = [point[0] for point in data_points]

# Plot data points
plt.scatter(x, y)
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Custom Axis and Data Points')
plt.xticks(x_axis_values)
plt.yticks(y_axis_values)
plt.grid(True)

# Display the graph
plt.show()
