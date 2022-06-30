import logging
import math
import threading
import time
import socket
import runge_kutta as rk
import json
from simple_pid import PID

href_list = []
href_aux = []
ht = [1]
qout = [0]
h_0 = 1
qin_0 = 1
period = 0.05
t = 0
qin = [1,1]


logging.info("Thread %s: starting")
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 52415  # Port to listen on (non-privileged ports are > 1023


def softPLC_thread():
    #  Metodo para aquisição dos dados do sinotico via socket TCP/IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not lock.locked():
            lock.acquire()  #Entra na seção critica
            href_aux.append(float(json.loads(data)))
            lock.release()  #Sai da seção critica
        if not data:
            logging.info("Thread %s: finishing")
        if ht:
            if not lock.locked():
                lock.acquire()
                pid = PID(2, 6, 0.05, setpoint=href_aux[-1])
                pid.output_limits = (0, None)
                qin[-1] = pid(ht[-1])
                h_0 = ht[-1]
                lock.release()
            conn.sendall(json.dumps(f"Vazão de entrada: {qin[-1]}\n"
                                    f"Vazão de saida: {qout[-1]}\n"
                                    f"Altura referencia: {href_aux[-1]}\n"
                                    f"Altura atual: {ht[-1]}").encode())
            time.sleep(2 * period)
        else:
            conn.sendall(data)
            time.sleep(2 * period)


def process_thread():
    res = 0
    while True:
        if href_aux and not lock.locked():
            lock.acquire()
            qin.append(res)
            res = rk.rk4(qin[-2], ht[-1], qin[-1], 2)  # Calcula pelo metodo Runge-Kutta
            qin.append(res)
            href_list.append(href_aux[-1])  # Acrescenta referencia na lista
            ht.append(res)
            qout.append(0.5 * math.sqrt(ht[-1]))  # Calcula e salva vazão em função da altura h(t)
            lock.release()
            time.sleep(period)


lock = threading.Lock()

# process_thread
logging.info("Main    : create and start thread %d.", 1)
process = threading.Thread(target=process_thread, args=())
process.start()

# softPLC_thread
logging.info("Main    : create and start thread %d.", 0)
softPLC = threading.Thread(target=softPLC_thread, args=())
softPLC.start()

