import socket
import json

"""Настройка модуля сервера через файл config.txt"""
config = open("config1.txt", "r")
HOST = config.readline()
HOST = HOST.replace("\n", '')
PORT = int(config.readline())
sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
while True:
    conn, addr = sock.accept()
    print(' Подключен:', addr)
    while True:
        data = conn.recv(1024)
        if not data: break
        recvdata = data.decode()
        print("Полученные данные:")
        print(recvdata)
        json_otv = """
        {
            "mark": "",
            "comment": ""
        }
        """
        otvet = json.loads(json_otv)
        otvet["mark"] = "1"
        otvet["comment"] = "Comment 1"
        otv = json.dumps(otvet)
        print(otv.encode())
        conn.send(otv.encode())
    conn.close()