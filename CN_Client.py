# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:37:24 2021

@author: sriman
"""

import socket
import threading


username=input("Choose a username :")
if username=="admin":
    password=input('Enter the Password :')
    
    
    

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',11111))

stop_thread=False


def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message=client.recv(1024).decode('ascii')
            if message=='USER':
                client.send(username.encode('ascii'))
                next_message=client.recv(1024).decode('ascii')
                if next_message == "PASSWORD":
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii')=="REFUSE":
                        print("Wrong password !!! Access denied!!!")
                        stop_thread=True
                        
                elif next_message=='BAN':
                    print('Access Denied because of the BAN!!')
                    client.close()
                    stop_thread=True
                    
            
                
                
            else:
                print(message)
                
        except:
            print("An error occured!!")
            client.close()
            break
            
        
def write():
    while 1:
        if stop_thread:
            break
        
        
        message=f'{username}: {input("")}'
        
        if message[len(username)+2:].startswith('/'):
           
           
                if username=="admin":
                     if message[len(username)+2:].startswith('/kick'):
                       client.send(f'KICK{message[len(username)+2+6:]}'.encode('ascii'))
                     elif message[len(username)+2:].startswith('/ban'):
                       client.send(f'BAN{message[len(username)+2+5:]}'.encode('ascii'))
                     else :
                       print("No such commands!!")
                
                
                    
                else:
                  print("Commands can only be excecuted by admin!!")  
            
        else:    
             client.send(message.encode('ascii'))
        
recieve_thread=threading.Thread(target=recieve)
recieve_thread.start()

write()
