from cryptography.fernet import Fernet
import os
import log_method

cripher = Fernet(b'D7Zh4RcKcxIRDOrxB68u98_WT_31qlMhXwFTMByCAYc=')

@log_method.log_method_info
def crypt_file(filename):
    '''
    Шифрует любой файл.

    filename - Название файла, который нужно зашифровать
    Если такой файл уже существует в директории, то он его перезапишет

    Возвращает None, при этом создает файл "filename".bin - это и есть зашифрованный файл
    '''
    with open(filename, 'r') as decrypted:
        with open(filename + '.bin', 'wb') as encrypted:
            data = '\n'.join(decrypted.readlines())
            encrypted_data = cripher.encrypt(data.encode('utf-8'))
            encrypted.write(encrypted_data)


@log_method.log_method_info
def decrypt_file(filename):
    '''
    Выполняет расшифровку файла.

    filename - Название файла, который нужно расшифровать. Файл должен иметь расширение .bin
    Если такой файл уже существует в директории, то он его перезапишет

    Возвращает None, при этом создает файл "filename", убирая расширение .bin, который является расшифрованным файлом
    '''
    with open(filename, 'rb') as encrypted:
        with open(os.path.splitext(filename)[0], 'w') as decrypted:
            data = encrypted.read()
            decrypted_data = cripher.decrypt(data)
            lines = decrypted_data.split(b'\n')
            for line in lines[::2]:
                decrypted.writelines(line.decode('utf-8') + '\n')


if __name__ == '__main__':
    crypt_file('main.py')
    decrypt_file('main.py.bin')