from socket import *
import sys
import zlib
import gzip
import re
'''def setup_socket(hostname, port):
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((hostname, port))

        # Listen for incoming connections
        server_socket.listen(5)  # Maximum number of queued connections

        print(f"Socket is listening on {hostname}:{port}")

        return server_socket

    except socket.error as e:
        print(f"Socket setup failed: {e}")
        return None

if __name__ == "__main__":
    hostname = '127.0.0.1'  # Localhost
    port = 8888              # Example port number

    server_socket = setup_socket(hostname, port)

    if server_socket:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        # Now you can communicate with the client using client_socket
        # Don't forget to close the sockets when done.
        client_socket.close()
        server_socket.close()'''
def parse_http_request(request_data):
    host_pattern = r'Host:\s(.*?)\r\n'
    match = re.search(host_pattern, request_data)
    if match:
        # Extract and return the host from the matched group
        return match.group(1)
    else:
        return None
    # Implement HTTP request parsing logic here
    # i should return a port and a destation  ip from this data
    #return destination_ip and port
    pass

def forward_request_to_server(request_data):
    # Implement forwarding logic here
    pass
def proxy_to_server(destation_ip, destation_port):
    #print(destation_ip)
    pass


def create_socket(ip_address, port):
   server_socket = socket(AF_INET, SOCK_STREAM)
   server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
   server_socket.bind((ip_address,  port))
   print(port)
   server_socket.listen(1)
   print("Server is running at ip {} and port {}".format(ip_address, port))
   return  server_socket

def receive_all(socket):
    """Receive data from a socket until no more data is available."""
    buffer_size = 1024
    received_data = b""  # Initialize an empty byte string to store received data
    while True:
        chunk = socket.recv(buffer_size)  # Receive a chunk of data
        if not chunk:  # If no more data is available, exit the loop
            break
        received_data += chunk  # Append the received chunk to the data
    return received_data
# Main function

def main():
    ip_address = "localhost"
    port = 1234
    server_socket = create_socket(ip_address, port)
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        request_data = client_socket.recv(1024).decode("utf-8")
        if request_data:
            print("Received request:")
            print(request_data)
        
            destation_ip = parse_http_request(request_data)
            print(destation_ip)
            
            socket_client = socket(AF_INET, SOCK_STREAM)
            socket_client.connect((destation_ip.encode("utf-8"),80))
            socket_client.send(request_data.encode("utf-8"))
           # response = receive_all(socket_client) 
            response = socket_client.recv(1024)
            is_text = (response.decode("utf-8", "ignore"))
            print(is_text)
            if is_text:
                altered_message = is_text.replace("Stockholm", "kir").replace("Smiley", "kir")
                client_socket.send(altered_message.encode("utf-8"))
                response_message = client_socket.recv(1024)
                client_socket.close()
                break




if __name__ == "__main__":
    main()

'''while True: #The proxy is runing allways
        # accept the request and save info about socket in "serverSideSocket"
        serverSideSocket, addr = welcomeSocket.accept()  
        # handles clients request and alters it if needed
        message = handle_client(serverSideSocket)
        
        if len(message) != 0: #run this block if message is not empty
            #Find port and Ip for dest of the message
            destPort, destIP = port_and_ip(message)
            #Create client socket and connect it to dest server then send altred message
            clientSideSocket = socket(AF_INET, SOCK_STREAM)#ipv4/tcp
            clientSideSocket.connect((destIP, destPort))
            clientSideSocket.send(message.encode("utf-8"))
            # recive first chunk of data from the server
            responseMessage = clientSideSocket.recv(1024)
            # Checks if response content is text
            is_text = is_text_content(responseMessage.decode("utf-8", "ignore")) 

            while True: # while we can read data, we continue same process 
                if len(responseMessage) != 0:
                    if is_text: # if content is text then alter it and send it to the server
                        alteredMessage = alter_response(responseMessage.decode("utf-8", "ignore"))
                        serverSideSocket.send(alteredMessage.encode("utf-8"))
                    else: # if not text (image) send in directly to the browser
                        serverSideSocket.send(responseMessage)
                else:
                    serverSideSocket.close()
                    break
                responseMessage = clientSideSocket.recv(1024)
                
            clientSideSocket.close()'''


           # request = request.replace(b"Connection: keep-alive",b"Connection: close") #change connection type to closed
