import socket

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

# Receive the quaternary data from the sender
received_data = sender_socket.recv(1024).decode()
quaternary_data = eval(received_data)  # Convert the received string back to a list

# Convert quaternary data to binary
binary_data = quaternary_to_binary(quaternary_data)
print("Received Binary Data:", binary_data)

# Close the connection
sender_socket.close()
receiver_socket.close()
