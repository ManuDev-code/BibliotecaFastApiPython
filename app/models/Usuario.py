class Usuario:
    ultimo_id = 0

    def __init__(self, id=None, nombre="", email="", telefono=""):
        if id is None:
            Usuario.ultimo_id += 1
            self.id = Usuario.ultimo_id
        else:
            self.id = id
            # Actualizar el último ID si el ID proporcionado es mayor
            if id > Usuario.ultimo_id:
                Usuario.ultimo_id = id

        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Email: {self.email} | Teléfono: {self.telefono}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            email=data.get("email"),
            telefono=data.get("telefono")
        )