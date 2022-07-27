# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:08:54 2021

@author: sriman
"""

import threading
import socket

host='127.0.0.1' 
port= 11111

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
users=[]
with open("bans.txt",'w') as f:
    f.write("")


def broadcast(message):    
    for client in clients:
        client.send(message)
        
def handle(client):
    while True:
        try:
            msg=message=client.recv(1024)
        
            
                
            
            if msg.decode('ascii').startswith('KICK'):
                if users[clients.index(client)]=="admin":
                    name1=msg.decode('ascii')
                    name_to_kick=name1[4:]
                    kick_user(name_to_kick)
                
                else:
                    client.send('Command refused'.encode('ascii'))
                
            elif msg.decode('ascii').startswith('BAN'): 
                if users[clients.index(client)]=="admin":
                    name2=msg.decode('ascii')
                    name_to_ban=name2[3:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a') as f:
                          f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!!')
                else:
                    client.send('Command refused'.encode('ascii'))
            else:
                broadcast(message)
            
        except:
           index=clients.index(client) 
           clients.remove(client)
           client.close()  
           user=users[index]
           broadcast(f'{user} left the chat!'.encode('ascii'))
           users.remove(user)
           break
       
def recieve():
      while True:
             client,address=server.accept()
             print(f"Connected with {str(address)}")
             
             client.send('USER'.encode('ascii'))
             user=client.recv(1024).decode('ascii')
             
             with open('bans.txt','r') as f:
                 bans=f.readlines()
             
             if user+'\n' in bans:
                 client.send('BAN'.encode('ascii'))
                 client.close()
                 continue
             
                
             if user=="admin":
                 client.send('PASSWORD'.encode('ascii'))
                 password=client.recv(1024).decode('ascii')
                 
                 if password != "computer network":
                     client.send("REFUSE".encode('ascii'))
                     client.close()
                     continue
                 
             users.append(user)
             clients.append(client)
             
             print(f'Username of the client is {user}!')
             broadcast(f'{user} joined the chat '.encode('ascii'))
             client.send('Connected to the server!'.encode('ascii'))
             
              
             thread=threading.Thread(target=handle,args=(client,))
             thread.start()
            

def kick_user(username):
    if username in users:
        user_index=users.index(username)
        client_to_kick=clients[user_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You are Kicked by the admin'.encode('ascii'))
        client_to_kick.close()
        users.remove(username)
        broadcast(f'{username} was kicked by the admin!!'.encode('ascii'))



print("Server is listening...")
recieve()        