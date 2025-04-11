class Libro:
    ultimo_id = 0

    def _init_(self, id=None, titulo="", autor="", isbn="", descripcion="", disponible=True):
        if id is None:
            Libro.ultimo_id += 1
            self.id = Libro.ultimo_id
        else:
            self.id = id
            # Actualizar el último ID si el ID proporcionado es mayor
            if id > Libro.ultimo_id:
                Libro.ultimo_id = id

        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.descripcion = descripcion
        self.disponible = disponible

    def _str_(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ID: {self.id} | Título: {self.titulo} | Autor: {self.autor} | ISBN: {self.isbn} | Estado: {estado}"

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "descripcion": self.descripcion,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            titulo=data.get("titulo"),
            autor=data.get("autor"),
            isbn=data.get("isbn"),
            descripcion=data.get("descripcion"),
            disponible=data.get("disponible", True)
        )