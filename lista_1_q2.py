import sys
import ctypes
from ctypes import c_byte, c_int32, Array
import struct
import random
from random import randint, choice
ids_inscricao = list(range(1, 10000))
cursos = ['BCC', 'ADM', 'ENG. ELETRONICA', 'ENG. AMBIENTAL', 'ENG. ELETRICA',
          'LETRAS', 'REDES']

def generate_random_registro(_id=None):
    # _id = random.choice(ids_inscricao)
    #ids_inscricao.pop(_id) # 4 bytes
    curso = choice(cursos).ljust(20) # 20 bytes
    cpf = "%i%i%i.%i%i%i.%i%i%i-%i%i" %(randint(0, 9), randint(0, 9),randint(0, 9),
                                   randint(0, 9), randint(0, 9), randint(0, 9),
                                   randint(0, 9), randint(0, 9), randint(0, 9),
                                   randint(0, 9), randint(0, 9))
    cpf = cpf.ljust(15) # 15 bytes

    dataNascimento = "{0}/{1}/{2}".format(randint(1, 31), randint(1, 12), randint(1950, 2000)).ljust(11) # 11 bytes
    sexo = choice(['M', 'F']) # 1 byte
    email = '@email.com'
    aux = randint(4, 40-len(email))
    aux_email = ''
    for i in range(aux):
        aux_email += chr(randint(*choice(((48, 57), (97, 122), (65, 90)))))

    email = (aux_email + email).ljust(40) # 40 bytes
    opcaoQuadro = chr(randint(65, 90)) # 1 byte
    aux = curso + cpf + dataNascimento + sexo + email + opcaoQuadro
    return _id.to_bytes(4, 'little') + aux.encode()

def generate_file_registros(filename, line_size, file_size=None, lines=None):
    # size in KB
    if lines:
        file_size = line_size * lines
    elif file_size:
        lines = file_size / line_size
    else:
        raise Exception("both parameter 'line' and 'file_size' can't be None type.")

    print("O Arquivo a ser gerado terá %iKB e %i linhas" % (file_size, lines))

    def primo(num):
        if num < 2:
            return False

        for i in range(2, num):
            if num % i == 0 and i != num:
                return False
        return True

    with open(filename, 'wb') as arq:
        count = 1
        while count < lines:
            registro = generate_random_registro(count)
            if primo(i):
                for i in range(randint(2, 5)):
                    arq.write(count.to_bytes(4, 'little') + registro[4:])
                    count += 1
                continue

            arq.write(registro)

class Registro:
    _struct = struct.Struct("i20s15s11s1s40s1s")

    def __init__(self, bytes):
        # assert len(bytes) == self._struct.size
        self._unpack = self._struct.unpack(bytes)
        self.id_inscricao = self._unpack[0]
        self.curso = self._unpack[1].decode()
        self.cpf = self._unpack[2].decode()
        self.dataNascimento = self._unpack[3].decode()
        self.sexo = self._unpack[4].decode()
        self.email = self._unpack[5].decode()
        self.opcaoQuadro = self._unpack[6].decode()

    def __str__(self):
        return self.id_inscricao + self.curso + self.cpf +\
        self.dataNascimento + self.sexo + self.email + self.opcaoQuadro



if __name__ == '__main__':
    # r = Registro(b'\x01\x00\x00\x00'+b'A'*88)
    # print(r)
    aux=generate_random_registro()
    print(aux)
    print(len(aux))