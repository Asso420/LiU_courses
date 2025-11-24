

from socket import *
from bs4 import BeautifulSoup
import requests
import sys
import zlib
import gzip
import re
import base64
import urllib

def parse_http_request(request_data):
    host_pattern = r'Host:\s(.*?)\r\n'
    match = re.search(host_pattern, request_data)
    if match:
        return match.group(1)
    else:
        return None

def create_socket(ip_address, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)
    print("Server is running at ip {} and port {}".format(ip_address, port))
    return server_socket

from bs4 import BeautifulSoup
'''
def fetch_images(html_content):
    image_urls = []
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <a> tags in the HTML content
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        # Get the value of the 'href' attribute of each <a> tag
        href = a_tag.get('href')
        # Append the image URL to the list
        if href:
            image_urls.append(href)
    return image_urls
'''
'''
def fetch_images(html_content, base_url):
    image_urls = []
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <a> tags in the HTML content
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        # Get the value of the 'href' attribute of each <a> tag
        href = a_tag.get('href')
        # Append the image URL to the list
        if href:
            # Convert the relative URL to absolute URL
            absolute_url = urllib.parse.urljoin(base_url, href)
            image_urls.append(absolute_url)
    return image_urls
'''
'''
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
            destination_ip = parse_http_request(request_data)
            print(destination_ip)
            socket_client_proxy = socket(AF_INET, SOCK_STREAM)
            socket_client_proxy.connect((destination_ip, 80))
            socket_client_proxy.send(request_data.encode("utf-8"))
            response = socket_client_proxy.recv(4096)
            is_text = response.decode("utf-8", "ignore")
            
            if is_text:
                #headers, html_body = is_text.split('\r\n\r\n', 1)
                headers, html_body = re.split(r'\r\n\r\n|\n\n', is_text, maxsplit=1)
                print ('html_body:')
                print (html_body)
                altered_message = is_text.replace("Smiley", "Boill").replace("Stockholm", "Mirckholf")
                print("Modified HTML content:")
                print(altered_message)
                client_socket.send(altered_message.encode("utf-8"))

                image_urls = fetch_images(html_body)
                print ("Image URLsfgjhkjl:")
                print(image_urls)

                for url in image_urls:
                    print ('hjdfkljghvkcmnvdk')
                    image_request = f"GET {url} HTTP/1.1\r\nHost: {destination_ip}\r\n\r\n"
                    print ("Image Request):")
                    print(image_request)

                    socket_client_proxy.send(image_request.encode("utf-8"))
                    image_response = socket_client_proxy.recv(4096)
                    client_socket.send(image_response)
                client_socket.close()
                break'''
'''
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
            destination_ip = parse_http_request(request_data)
            print(destination_ip)
            socket_client_proxy = socket(AF_INET, SOCK_STREAM)
            socket_client_proxy.connect((destination_ip, 80))
            socket_client_proxy.send(request_data.encode("utf-8"))
            response = socket_client_proxy.recv(4096)
            is_text = response.decode("utf-8", "ignore")
            
            if is_text:
                headers, html_body = re.split(r'\r\n\r\n|\n\n', is_text, maxsplit=1)
                altered_message = is_text.replace("Smiley", "Boill").replace("Stockholm", "Mirckholf")
                print("Modified HTML content:")
                print(altered_message)
                client_socket.send(altered_message.encode("utf-8"))

                # Extract base URL from the request headers
                #base_url = "http://" + destination_ip  # Example, you might need to adjust this depending on the headers
                base_url = "http://zebroid.ida.liu.se/fakenews/test4.html"
                image_urls = fetch_images(html_body, base_url)
                print("Image URLs:")
                print(image_urls)

                for url in image_urls:
                    print ('hjdfkljghvkcmnvdk')
                    image_request = f"GET {url} HTTP/1.1\r\nHost: {destination_ip}\r\n\r\n"
                    print ("Image Request):")
                    print(image_request)

                    socket_client_proxy.send(image_request.encode("utf-8"))
                    image_response = socket_client_proxy.recv(4096)
                    client_socket.send(image_response)
                client_socket.close()
                break
'''


'''
#sista
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
            destination_ip = parse_http_request(request_data)
            print(destination_ip)
            socket_client_proxy = socket(AF_INET, SOCK_STREAM)
            socket_client_proxy.connect((destination_ip, 80))
            socket_client_proxy.send(request_data.encode("utf-8"))
            response = b''
            while True:
                chunk = socket_client_proxy.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            is_text = response.decode("utf-8", "ignore")
            if is_text:
                headers, html_body = re.split(r'\r\n\r\n|\n\n', is_text, maxsplit=1)
                altered_message = is_text.replace("Smiley", "Boill").replace("Stockholm", "Mirckholf")
                print("Modified HTML content:")
                print(altered_message)
                client_socket.send(altered_message.encode("utf-8"))

                # Extract base URL from the request headers
                base_url = "http://zebroid.ida.liu.se/fakenews/test4.html"
                image_urls = fetch_images(html_body, base_url)
                print("Image URLs:")
                print(image_urls)

                for url in image_urls:
                    image_request = f"GET {url} HTTP/1.1\r\nHost: {destination_ip}\r\n\r\n"
                    print ("Image Request):")
                    print(image_request)

                    socket_client_proxy.send(image_request.encode("utf-8"))
                    image_response = b''
                    while True:
                        chunk = socket_client_proxy.recv(4096)
                        if not chunk:
                            break
                    image_response += chunk
                    #image_response = socket_client_proxy.recv(4096)
                    client_socket.send(image_response)
                    
            client_socket.close()
            break

'''
def fetch_images(html_content, base_url):
    image_urls = []
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <img> tags in the HTML content
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        # Get the value of the 'src' attribute of each <img> tag
        src = img_tag.get('src')
        # Append the image URL to the list
        if src:
            # Convert the relative URL to absolute URL
            absolute_url = urllib.parse.urljoin(base_url, src)
            image_urls.append(absolute_url)
    return image_urls

def main():
    ip_address = "localhost"
    port = 1234
    server_socket = create_socket(ip_address, port)
    print(f"Proxy server listening on {ip_address}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        request_data = client_socket.recv(4096).decode("utf-8")
        if request_data:
            print("Received request:")
            print(request_data)
            destination_ip = parse_http_request(request_data)
            print(f"Destination IP: {destination_ip}")

            socket_client_proxy = socket(AF_INET, SOCK_STREAM)
            socket_client_proxy.connect((destination_ip, 80))
            socket_client_proxy.send(request_data.encode("utf-8"))

            response_data = b""
            while True:
                chunk = socket_client_proxy.recv(4096)
                if not chunk:
                    break
                response_data += chunk

            response_text = response_data.decode("utf-8", "ignore")
            if response_text:
                headers, html_body = re.split(r'\r\n\r\n|\n\n', response_text, maxsplit=1)
                altered_html_body = html_body.replace("Smiley", "Boill").replace("Stockholm", "Mirckholf")

                print("Modified HTML content:")
                print(altered_html_body)
                client_socket.send(headers.encode("utf-8") + b"\r\n\r\n" + altered_html_body.encode("utf-8"))

                base_url = "http://zebroid.ida.liu.se/fakenews/test4.html"
                image_urls = fetch_images(html_body, base_url)
                print("Image URLs:")
                print(image_urls)

                for url in image_urls:
                    image_request = f"GET {url} HTTP/1.1\r\nHost: {destination_ip}\r\n\r\n"
                    print("Image Request:")
                    print(image_request)

                    socket_client_proxy.send(image_request.encode("utf-8"))
                    image_response_data = b""
                    while True:
                        chunk = socket_client_proxy.recv(4096)
                        if not chunk:
                            break
                        image_response_data += chunk
                    client_socket.send(image_response_data)
            client_socket.close()
            socket_client_proxy.close()

if __name__ == "__main__":
    main()

"http://zebroid.ida.liu.se/fakenews/smiley.jpg"
'''
from socket import*
from bs4 import BeautifulSoup
import requests
import sys
import zlib
import gzip
import re
import base64

 
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

def create_socket(ip_address, port):
   server_socket = socket(AF_INET, SOCK_STREAM)
   server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
   server_socket.bind((ip_address,  port))
   print(port)
   server_socket.listen(1)
   print("Server is running at ip {} and port {}".format(ip_address, port))
   return  server_socket

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
            
            socket_client_proxy = socket(AF_INET, SOCK_STREAM)
            socket_client_proxy.connect((destation_ip.encode("utf-8"),80))
            socket_client_proxy.send(request_data.encode("utf-8"))


            response = socket_client_proxy.recv(1024)
            is_text = (response.decode("utf-8", "ignore"))
            print(is_text)
            if is_text:
                headers, html_body = is_text.split('\r\n\r\n', 1)

                # Modify the HTML body
                altered_message = is_text.replace("Smiley", "Boill").replace("Stockholm", "Mirckholf")
                print("Modified HTML content:")
                print(altered_message)

                #modified_response = f"{headers}\r\n\r\n{altered_message_with_troll_image}"
               # client_socket.send(modified_response.encode("utf-8"))

                client_socket.send(altered_message.encode("utf-8"))

                response_message = client_socket.recv(1024)
                
                client_socket.close()
                break

if __name__ == "__main__":
    main()
'''


''' altered_message_with_troll_image = replace_jpg_images(altered_message)
                print("Modified HTML content with troll image:")
                print(altered_message_with_troll_image)
    
       client_socket.send(altered_message_with_troll_image.encode("utf-8")) '''
    


     # Parse HTML to find image URL
''' soup = BeautifulSoup(html_body, 'html.parser')
                img_tag = soup.find('img')
                if img_tag:
                    image_url = img_tag['src']
                    print("http://zebroid.ida.liu.se/fakenews/smiley.jpg:", image_url)

                    # Fetch the image
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_data = image_response.content
                        encoded_image = base64.b64encode(image_data)
                        # Send image data to client
                        client_socket.send(image_data)
                    else:
                        print("Failed to fetch image:", image_response.status_code)

                encoded_image_data = client_socket.recv(1024)
                image_data = base64.b64decode(encoded_image_data)'''
'''
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
# Main function '''
'''
def replace_jpg_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all image tags
    img_tags = soup.find_all( 'img')
    #iterate through each image tag
    for img_tag in img_tags:
        #check if the image is JPG and its source contains "Smiley" 
        if img_tag['src'].endswith('.jpg') and 'Smiley' in img_tag['src']:
            #replace 
            img_tag['src'] = 'http://zebroid.ida.liu.se/fakenews/trolly.jpg'

    return str(soup)'''



           # response = receive_all(socket_client)
'''response = b''
            while True:
                chunk = socket_client_proxy.recv(1024)
                if not chunk: 
                    break
                response += chunk '''           

'''
def forward_request_to_server(request_data):
    # Implement forwarding logic here
    pass
def proxy_to_server(destation_ip, destation_port):
    #print(destation_ip)
    pass'''

'''
def fetch_images(html_content):
    # Regular expression to match the image URL within the text
    img_pattern = r'image of (.*?)\.(?:jpg|jpeg|png|gif)'
    image_urls = re.findall(img_pattern, html_content, re.IGNORECASE)
    return image_urls'''