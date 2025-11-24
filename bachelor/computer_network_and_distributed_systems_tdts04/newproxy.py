from socket import *
import re




def create_socket(ip_address, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)
    print("Server is running at ip {} and port {}".format(ip_address, port))
    return server_socket

def parse_http_request(request_data):
    host_pattern = r'Host:\s(.*?)\r\n'
    match = re.search(host_pattern, request_data)
    if match:
        return match.group(1)
    else:
        return None

def content_type(data):
    data_decode = data.decode('utf-8' , "ignore")
    if re.search("Content-Type: text", data_decode):
        return True
    return False


def change_request(request_from_browser):
    host_pattern = r'smiley.jpg'
    match = re.search(host_pattern, request_from_browser)
    if match:
        result = request_from_browser.replace("smiley.jpg", "trolly.jpg")
        return result
    else:
        return request_from_browser
  

def main():
    ip_address = "localhost"
    port = 1234
    proxy_server_socket = create_socket(ip_address, port)
    print(f"Proxy server listening on {ip_address}:{port}...")
    while True:
        client_socket, client_address = proxy_server_socket.accept() # it returns a new socket object (client_socket) representing the connection and the address (client_address) of the client.
        print(f"Connection from {client_address} has been established.")
        request_from_browser = client_socket.recv(1024).decode("utf-8", "ignore") # recive data from browser
        if len(request_from_browser) != 0:
          server_ip_address =  parse_http_request(request_from_browser)
          #print("222222222222222222222222222222222222222222222")
          request_from_browser_v2 = change_request(request_from_browser)
          print (request_from_browser_v2)
          proxy_client_socket = socket(AF_INET, SOCK_STREAM)
          proxy_client_socket.connect((server_ip_address, 80))
          proxy_client_socket.send(request_from_browser_v2.encode("utf-8", "ignore"))
          server_respond = proxy_client_socket.recv(1024)
          content_is_text = content_type(server_respond)
          while True:
             
                if len(server_respond) > 0:
                    if content_is_text: 
                        server_respond = server_respond.decode("utf-8" , "ignore")
                        #print(server_respond)
                        server_respond_v2 = server_respond.replace("Stockholm", "Linköping").replace("Smiley", "trolly")
                        if "./Linköping-spring" in server_respond_v2:
                            server_respond_v2 = server_respond_v2.replace("./Linköping-spring", "./Stockholm-spring")
                        client_socket.send(server_respond_v2.encode('utf-8'))
                      
                    else: # if the data is not the a text type then we just send it to the client without any changes
                        client_socket.send(server_respond)
                else:
                  proxy_client_socket.close()
                  break
                server_respond =proxy_client_socket.recv(1024)
        client_socket.close()


if __name__ == "__main__":
    main()