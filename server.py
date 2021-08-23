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
skt.bind(("",port))
skt.listen()
print("Socket is listening")
while True:
    session, address=skt.accept()
    print("Connected to ",address)
    if session:
        cam=cv2.VideoCapture(0)
        while(cam.isOpened()):
            ret,img=cam.read()
            data=pickle.dumps(img)
            msg=struct.pack("Q",len(data))+data
            session.sendall(msg)
            cv2.imshow("Transmitting video..",img)
            if cv2.waitKey(1)==13:
                cv2.destroyAllWindows()
                session.close
                break
