import socket

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


# Establish a socket connection
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_address = 'IP_ADDRESS_OF_MACHINE_B'  # Replace with the actual IP address of Machine B
receiver_port = 12345  # Choose a suitable port number
receiver_endpoint = (receiver_address, receiver_port)
sender_socket.connect(receiver_endpoint)

# Example usage
binary_data = '01011100110010'  # Binary data to be encoded
quaternary_data = binary_to_quaternary(binary_data)

# Send the quaternary data to the receiver
sender_socket.sendall(str(quaternary_data).encode())

# Close the socket connection
sender_socket.close()
