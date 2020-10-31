import sys
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

def generate_file_registros(filename, line_size, file_size=None, lines=None, repeat=False):
    # size in KB
    if lines:
        file_size = line_size * lines
    elif file_size:
        lines = file_size / line_size
    else:
        raise Exception("both parameter 'line' and 'file_size' can't be None type.")
    print(lines, file_size)
    print("O Arquivo a ser gerado terá %i Bytes e %i linhas" % (file_size, lines))

    if repeat:
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
                if primo(count):
                    for i in range(randint(2, 5)):
                        arq.write(count.to_bytes(4, 'little') + registro[4:] + b'\n')
                        count += 1
                    continue

                arq.write(registro + b'\n')
                count += 1
    else:
        with open(filename, 'wb') as arq:
            count = 1
            while count < lines:
                registro = generate_random_registro(count)
                arq.write(registro + b'\n')
                count += 1

if __name__ == "__main__":
    repeat = (len(sys.argv) > 3 and sys.argv[3].upper() == 'T')
    generate_file_registros(sys.argv[1], line_size=92, lines=int(sys.argv[2]), repeat=repeat)