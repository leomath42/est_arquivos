
if __name__ == '__main__':
    with open('registro_sorted.txt', 'rb') as arq:
        dataSize = arq.seek(0, 2)
        arq.seek(0, 0)
        chunk = int((dataSize // Registro.size // 100) * 93) if dataSize > 93 * 1000 else dataSize
        arq_output = open('registro_sem_duplicata.txt', 'w')
        while dataSize > 0:
            block = arq.read(chunk) if dataSize > chunk else arq.read(dataSize)
            # head = 0
            # tail = Registro.size
            arr = []

            # max_registro = Registro(block[head:tail])
            max_registro = Registro(block[Registro.size*0:Registro.size*1])

            for i in range(1, len(block)//Registro.size):
                registro = Registro(block[Registro.size * i : Registro.size * (i+1)])

                if registro.cpf == max_registro.cpf and registro.id_inscricao > max_registro.id_inscricao:
                    max_registro = registro
                else:
                    arr.append(str(max_registro))
                    max_registro = registro

            arq_output.writelines(arr)
            dataSize -= chunk

        arq_output.close()
