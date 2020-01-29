import socket
import numpy as np
import cv2 as cv
import os


addr = ("0.0.0.0", 8080)
buf = 512
width = int(640/2)
height = int(320/2)
code = b'start'
num_of_chunks = width * height * 3 / buf
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
print(ip)

def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation =cv.INTER_AREA)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk, _ = s.recvfrom(buf)
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)
 
        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(height, width, 3)
        frame200 = rescale_frame(frame, percent=300)

        cv.imshow('recv', frame200)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    s.close()
    cv.destroyAllWindows()