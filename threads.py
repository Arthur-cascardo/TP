import logging
import threading
import time
import socket
import runge_kutta as rk
import json


href_list = []
href_aux = []
ht = []

logging.info("Thread %s: starting")
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 52415  # Port to listen on (non-privileged ports are > 1023


def getDataFromSynoptic():
    #  Metodo para aquisição dos dados do sinotico via socket TCP/IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        href_aux.append(float(json.loads(data)))
        if not data:
            logging.info("Thread %s: finishing")
        if ht:
            conn.sendall(json.dumps(ht[-1]).encode())
        else:
            conn.sendall(data)


def softPLC_thread():
    getDataFromSynoptic()


def process_thread():
    while True:
        if href_aux:
            res = rk.rk4(1, 1, href_aux[-1], 10) # Calcula pelo metodo Runge-Kutta
            href_list.append(href_aux[-1])  # Acrescenta referencia na lista
            href_aux.clear()
            if res not in ht:  # Verifica se o resultado calculado ja esta na lista
                ht.append(res)  # Adiciona se não estiver
        time.sleep(0.05)


# process_thread
logging.info("Main    : create and start thread %d.", 1)
process = threading.Thread(target=process_thread, args=())
process.start()

# softPLC_thread
logging.info("Main    : create and start thread %d.", 0)
softPLC = threading.Thread(target=softPLC_thread, args=())
softPLC.start()

softPLC.join()
