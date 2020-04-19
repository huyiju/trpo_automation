import socket
import json

"""Настройка модуля сервера через файл config.txt"""
config = open("config2.txt", "r")
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
        json_otv1 = """
        {
            "messageType": 2,
            "grade": 0,
            "comment": ""
        }
        """
        json_otv2 = """
        {
            "messageType": 3,
            "key": "",
            "text": "",
            "rejectCode": ""
        }
        """
        json_otv3 = """
        {
            "messageType": 4,
            "errorMessage": ""
        }
        """
        otvet = json.loads(json_otv2)
        otvet["key"] = "1"
        otvet["text"] = "Comment 2"
        otvet["rejectCode"] = "001"

        otv = json.dumps(otvet)
        print(otv.encode())
        conn.send(otv.encode())
    conn.close()