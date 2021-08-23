import cv2
import socket
import pickle
import struct

try:
    skt=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket successfully created")
except socket.error as err:
    print("socket failed with error{}".format(err))

port=5555
server_ip="enter your ip here"
skt.connect((server_ip,port))
data= b""
payload_size=struct.calcsize("Q" )
while True:
    while len(data)<payload_size:
        packet=skt.recv(4*1024)
        if not packet:break
        data+=packet
    packed_msg_size=data[:payload_size]
    data=data[payload_size:]
    msg_size=struct.unpack("Q",packed_msg_size)[0]

    while len(data)<msg_size:
        data+=skt.recv(4*1024)
    img_data=data[:msg_size]
    data=data[msg_size:]
    img=pickle.loads(img_data)
    cv2.imshow("Receiving Video",img)
    if cv2.waitKey(1)==13:
        cv2.destroyAllWindows()
        break
skt.close()