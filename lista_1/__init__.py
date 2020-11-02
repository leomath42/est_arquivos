import struct


class Registro(bytes):
    _struct = struct.Struct("i20s15s11s1s40s1s1s")
    """
    int id_inscricao;
    char curso[20];
    char cpf[15];
    char dataNacimento[11];
    char sexo;
    char email[40];
    char opcaoQuadro;
    byte endLine; // adicionei
    """
    size = _struct.size

    def __init__(self, bytes):
        # assert len(bytes) == self._struct.size
        self._unpack = self._struct.unpack(bytes)
        self.id_inscricao = self._unpack[0]
        self.curso = self._unpack[1]
        self.cpf = self._unpack[2]
        self.dataNascimento = self._unpack[3]
        self.sexo = self._unpack[4]
        self.email = self._unpack[5]
        self.opcaoQuadro = self._unpack[6]
        self.endLine = self._unpack[7]

    def __str__(self):
        return str(self.__bytes__())

    def __eq__(self, other):
        return self.cpf == other.cpf or self.id_inscricao == other.id_inscricao

    def __lt__(self, other):
        return self.id_inscricao < other.id_inscricao

    def __gt__(self, other):
        return self.id_inscricao > other.id_inscricao

    def __bytes__(self):
        return bytes(self.id_inscricao.to_bytes(4, "little") + self.curso + self.cpf + \
                     self.dataNascimento + self.sexo + self.email + self.opcaoQuadro + self.endLine)


class RegistroFile():
    """
        Wrapper/Proxy file for Registro data encoding.
    """
    __non_wrapped__ = ['_RegistroFile__wrapper_file', 'MAX_DATA_IN_MEMORY', 'line_size', '_slider', '_buffer']
    size = Registro.size
    def __init__(self, file, mode='r', MAX_DATA_IN_MEMORY=50 * 1024, buffering=-1, encoding=None,
                 errors=None, newline=None, closefd=True, opener=None):

        self.__wrapper_file = open(file, mode, buffering, encoding, errors, newline, closefd, opener)
        # máximo de linhas(MAX_DATA_IN_MEMORY/size) ou qtd de linhas no buffer(buffer/size).
        def file_size():
            pos = self.__wrapper_file.tell()
            self.__wrapper_file.seek(0, 2)
            aux = self.__wrapper_file.tell()
            self.__wrapper_file.seek(pos, 0)
            return aux

        self.file_size = file_size()

        if MAX_DATA_IN_MEMORY < 0:
            self.MAX_DATA_IN_MEMORY = (self.file_size // self.size) * self.size
        else:
            self.MAX_DATA_IN_MEMORY = (MAX_DATA_IN_MEMORY // self.size) * self.size

        #self._buffer = self.__wrapper_file.read(self.MAX_DATA_IN_MEMORY)
        self._buffer = bytes()
        self.lines = 0#(len(self._buffer) // self.size)
        self._slider = 0


    def __repr__(self):
        return self.__wrapper_file.__repr__()

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return int(len(self._buffer) / self.size)

    def __iter__(self):
        return self

    def __next__(self):
        if self.lines <= self._slider:
            self._buffer = self.__wrapper_file.read(self.MAX_DATA_IN_MEMORY)
            self._slider = 0
            self.lines = int(len(self._buffer) / self.size)
            if not self._buffer:
                self.__wrapper_file.close()
                raise StopIteration()

        aux = self._buffer[self._slider * self.size:(self._slider + 1) * self.size]
        self._slider += 1
        self.file_size -= self.size
        return Registro(aux)

    def __getattr__(self, item):
        if item not in self.__class__.__non_wrapped__:
            return getattr(self.__wrapper_file, item)
        attr = self.__dict__.get(item)
        if attr:
            return attr
        raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, item))

    def __setattr__(self, key, value):
        if key not in self.__class__.__non_wrapped__:
            setattr(self.__wrapper_file, key, value)
        else:
            self.__dict__[key] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__wrapper_file.close()


if __name__ == "__main__":
    r = RegistroFile('registro_0_ate_100.txt', 'rb')
    print(len(r))
    print(r.file_size)
    for line in r:
        print(line.email, r.file_size)
    # while True:
    #     print(Registro(next(r)).email, r.file_size)
    print(r.file_size)