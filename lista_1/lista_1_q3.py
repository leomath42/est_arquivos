#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    External Merge Join
"""
import sys
import time
import os

if __name__ != "__main__":
    from lista_1 import Registro, RegistroFile
else:
    from __init__ import Registro, RegistroFile


def external_merge_join(file_name_1, file_name_2, sort=False):

    def sort_files(file_name_1, file_name_2):
        # considerando ambos ordenados !
        # with RegistroFile(file_name_1, 'rb+') as arq1, RegistroFile(file_name_2, 'rb+') as arq2:
        #     # qsort aqui
        # aux = []
        for arq in (RegistroFile(file_name_1, 'rb+'), RegistroFile(file_name_2, 'rb+')):
            aux = []
            buff = arq.read(arq.file_size)
            for i in range(0, len(buff)//arq.size):
                aux.append(Registro(buff[i * arq.size: (i+1) * arq.size]))
            arq.seek(0, 0)
            arq.writelines(sorted(aux, key=lambda registro: registro.cpf))
            arq.close()
        # for index, arq in enumerate([RegistroFile(file_name_1, 'wb'), RegistroFile(file_name_2, 'wb')]):
        #     arq.writelines(sorted(dats[index], key=lambda registro: registro.cpf))

            # sort arq_left
            # sort arq_right
            # fim sort
    if sort:
        sort_files(file_name_1, file_name_2)

    arq1 = RegistroFile(file_name_1, 'rb')
    arq2 = RegistroFile(file_name_2, 'rb')
    merged = RegistroFile('merge_join_output.txt', 'wb')
    arq_left = arq_right = None

    if arq1.file_size >= arq2.file_size:
        arq_left = arq1
        arq_right = arq2
    else:
        arq_left = arq2
        arq_right = arq1

    while arq_left.file_size > 0 and arq_right.file_size > 0:
        chunk_output = list()
        left = next(arq_left, None)
        right = next(arq_right, None)
        while left and right:# in zip(arq_left, arq_right):
            if left.cpf == right.cpf:
                # add cartesian product of left_subset and right_subset to output
                # no caso, irei colocar só o left pro output !
                chunk_output.append(left)
                left = next(arq_left, None)
                right = next(arq_right, None)
            elif left.cpf < right.cpf:
                left = next(arq_left, None)
            else: #left > right:
                right = next(arq_right, None)
        # for registro in chunk_output:
        #     merged.write(registro)
        merged.writelines(chunk_output)
    # return merged
if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv['h']):
        print("use : file_name_1 file_name2 s p")
        print("use 'file_name_1' e 'file_name_2', são arquivos a serem combinados")
        print("use 's' caso os arquivos não estejam ordenados")
        print("use 'p' para imprir o arquivo combinado no final.")
    elif len(sys.argv) > 2:
        file_name_1 = sys.argv[1]
        file_name_2 = sys.argv[2]
        sort = (len(sys.argv) > 3 and sys.argv[3].lower() == 's') or (len(sys.argv) > 4 and sys.argv[4].lower() == 's')
        def benchmark(func, *args):
            t0 = time.perf_counter()
            func(*args)
            t1 = time.perf_counter()
            return t1 - t0

        _t = benchmark(external_merge_join, file_name_1, file_name_2, sort)

        if (len(sys.argv) > 3 and sys.argv[3].lower() == 'p') or (len(sys.argv) > 4 and sys.argv[4].lower() == 'p'):
            for line in RegistroFile('merge_join_output.txt', 'rb'):
                print(line.email)

        with RegistroFile(file_name_1, 'rb+') as arq1, RegistroFile(file_name_2, 'rb+') as arq2,\
            RegistroFile('merge_join_output.txt', 'rb') as out:

            print("File 1 : {0} size {1} KB".format(file_name_1, arq1.file_size/1024))
            print("File 2 {0}: {1} KB".format(file_name_2, arq2.file_size/1024))
            print("Merged file output: {0} size {1} KB".format('merge_join_output.txt', out.file_size/1024))
            print("time to external merge sort: {0}".format(_t))