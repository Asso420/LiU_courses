#!/usr/bin/python
import subprocess
import sys
import unicodedata
import random
import string
import secrets


def create_username(firstname, lastname):
    username = ''
    for i in range(0, 3):
      username += firstname[i]
    if len(lastname) == 0:
        for i in range(0, 2):
            username += chr(random.randint(97, 122))            
    else:
        for i in range(0, 2):
            username += lastname[i]
    for i in range(0, 3):
        username += chr(random.randint(48, 57))       
    return username


def replace_invalid_chars(name):
    new_name = ''
    for char in name:
        
        if not char in string.ascii_letters:
          
            new_name += chr(random.randint(97, 122))
        else:
            new_name += char
    
    return new_name




def create_user(file_name):
    subprocess.run("iconv -f UTF8 -t ASCII//TRANSLIT "+file_name+" > converted", shell=True)
    user_list = []
    with open("converted", "r") as file:
        for line in file:
            name_parts = line.strip().split()
            firstname = name_parts[0]
            lastname = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            firstname = replace_invalid_chars(firstname)
            lastname = replace_invalid_chars(lastname)
            username = create_username(firstname, lastname)
            exist = subprocess.run('getent passwd ' + username, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
            while not exist:
                username = create_username(firstname, lastname)
                exist = subprocess.run('getent passwdprint(file) ' + username, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
            #print(username)
            user_list.append(username)
    return user_list

def add_user(user_list):
    characters = string.ascii_letters + string.digits
    with open("users.txt", 'w+') as file:
        for name in user_list:
            username = name
            password = ''.join((secrets.choice(characters) for i in range(8)))
            try:
                subprocess.run(['useradd', username], check=True)
                char = chr(random.randint(1, 2))
                num = ord(char)
                print(num)
                space = "  "
                subprocess.run(f'mkdir /home{num}/{username}', shell=True)
                subprocess.run(f'chown {username}:{username} /home{num}/{username}', shell=True)
                text_to_write = f"{username} {space}    -fstype=nfs,rw,sync {space}      10.0.0.2:/home{num}/{username}"
                subprocess.run(f'echo {text_to_write} >> /etc/auto.home', shell=True)
                file.write(f"{username}:{1}\n")
            except subprocess.CalledProcessError as e:
                print(f"Failed to add user {username}: {e}")
            print(f"User: {username}, Password: {1}")
    file.close()
    subprocess.run(['chpasswd < users.txt'], shell=True)
def update_nis():
    subprocess.run(['make -C /var/yp'], shell=True)

def main():
    if len(sys.argv) != 2:
      print("Please provide the filename, bro")
    else:
        file_name = sys.argv[1]
        user_list = create_user(file_name)
        add_user(user_list)
        update_nis()


if __name__ == "__main__":
    main()
