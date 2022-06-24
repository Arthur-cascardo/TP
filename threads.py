import logging
import threading
import time
import socket
import runge_kutta as rk


def softPLC_thread(name):
    logging.info("Thread %s: starting", name)
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        logging.info("Thread %s: finishing", name)
                        break
                    conn.sendall(data)


def process_thread(name):
    logging.info("Thread %s: starting", name)
    rk.rk4()
    time.sleep(0.05)
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()

    # softPLC_thread
    logging.info("Main    : create and start thread %d.", 0)
    x = threading.Thread(target=softPLC_thread, args=("softPLC_thread",))
    threads.append(x)
    x.start()

    # process_thread
    logging.info("Main    : create and start thread %d.", 1)
    x = threading.Thread(target=process_thread, args=("process_thread",))
    threads.append(x)
    x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
