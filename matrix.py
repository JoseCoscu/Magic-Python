class Matrix:
    def __init__(self, filas, columnas, valores=None):
        self.filas = filas
        self.columnas = columnas
        if valores:
            if len(valores) != filas or any(len(fila) != columnas for fila in valores):
                raise ValueError("Dimensiones de los valores no coinciden con las dimensiones de la matriz.")
            self.valores = valores
        else:
            self.valores = [[0] * columnas for _ in range(filas)]

    def __len__(self):
        l = self.filas * self.columnas
        return l

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, nombre):
        if nombre.startswith('_'):
            partes = nombre[1:].split('_')
            if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                fila, columna = int(partes[0]), int(partes[1])
                if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                    return self.valores[fila][columna]
        if nombre.startswith('as'):
            try:
                partes = nombre.split('_')
                t = eval(partes[1])
                new_matrix = Matrix(self.filas, self.columnas,
                                    [[t(self.valores[x][y]) for y in range(self.columnas)] for x in range(self.filas)])

                return new_matrix
            except:
                pass
        raise AttributeError(f"'Matriz' object has no attribute '{nombre}'")

    def __setattr__(self, nombre, valor):
        if nombre.startswith('_'):
            partes = nombre[1:].split('_')
            if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
                fila, columna = int(partes[0]), int(partes[1])
                if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                    self.valores[fila][columna] = valor
                    return
        super().__setattr__(nombre, valor)

    def __iter__(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                yield self.valores[fila][columna]

    def __getitem__(self, indices):
        fila, columna = indices
        return self.valores[fila][columna]

    def __setitem__(self, indices, valor):
        fila, columna = indices
        self.valores[fila][columna] = valor

    def __add__(self, matrix):
        if self.filas != matrix.filas or self.columnas != matrix.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones para sumar.")
        resultado = Matrix(self.filas, self.columnas)
        for i in range(self.filas):
            for j in range(self.columnas):
                resultado[i, j] = self[i, j] + matrix[i, j]
        return resultado

    def __abs__(self):
        for i in self:
            i = abs(i)
        return self

    def __mul__(self, otra):
        if self.columnas != otra.filas:
            raise ValueError(
                "El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")
        resultado = Matrix(self.filas, otra.columnas)
        for i in range(self.filas):
            for j in range(otra.columnas):
                suma = 0
                for k in range(self.columnas):
                    suma += self[i, k] * otra[k, j]
                resultado[i, j] = suma
        return resultado

    def __str__(self):
        filas_str = ["\t".join(map(str, fila)) for fila in self.valores]
        return "\n".join(filas_str)

