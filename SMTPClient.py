from socket import *
import base64
from sys import exit

#Message format
message = "\r\n Testing"
endMessage = "\r\n.\r\n"


#Server information
serverName = "mail.smtp2go.com"
serverPort = 2525
mailserver = (serverName,serverPort)
print(f"ServerName : {serverName} --- ServerPort : {serverPort}")


#Trying to connect
print("Trying to connect...")
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
print("Connected...")


#Response has been received. Returns as bytes so need to convert it.
recv = clientSocket.recv(1024).decode()
stateStatus = int(recv.split(" ")[0])
dateAndTime = recv.split(",")[1]

if stateStatus != 220:
    print("Reply did not receive from server.")
else:
    print(f"State status : {stateStatus}")
    print(f"Date and time : {dateAndTime}")


#Sending ehlo message.
heloCommand = 'EHLO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
recv1 = recv1.decode()
if recv1[:3] != '250':
    print('250 reply not received from server.')

###############################################################################################################
#Info for username and password
username = ""
password = ""
###############################################################################################################

if username == "" or password == "":
    print("Type username and password of smtp account!")
    exit(0)

#Connection with username and pw.
print("Trying to connect...")
base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024).decode()
print(recv_auth)
if recv_auth[:3] != '235':
    print('235 reply not received from server.')
else:
    print("Authentication succeeded. You are ready to send emails.")


#Sending MAIL FROM.
mailFrom = "MAIL FROM:<compnetworks@gmail.com>\r\n"
print("Sending MAIL FROM")
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024).decode()
print("Server response : " + recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')


#Sending RCPT TO
rcptTo = "RCPT TO:<destination@adress.com>\r\n"
print("Sending RCPT TO")
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
recv3 = recv3.decode()
print("Server response : " + recv2)
if recv1[:3] != '250':
    print('250 reply not received from server.')


# Send DATA
data = "DATA\r\n"
print("Sending data : " + data)
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()
print("After DATA command: "+recv4)


# Send message data.
message = input("Enter your message: \r\n")
print("Sending data : " + message)
clientSocket.send(message.encode())
clientSocket.send(endMessage.encode())
recv_msg = clientSocket.recv(1024).decode()
if recv1[:3] != '250':
    print('250 reply not received from server.')
else:
    print("Data sent")

quitMessage = "QUIT\r\n"
clientSocket.send(quitMessage.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
clientSocket.close()