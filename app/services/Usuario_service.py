from typing import List, Optional
from app.models.Usuario import Usuario
from app.utils.data_handler import DataHandler


class UsuarioService:
    def __init__(self):
        self.data_handler = DataHandler[Usuario]("data/usuarios.json", Usuario)
        self.usuarios = self.data_handler.load_data()
        self._cargar_contador()

    def _cargar_contador(self):
        """Carga el contador de IDs desde el archivo o lo inicializa con el máximo ID existente"""
        contador = self.data_handler.load_counter("usuario_id")
        if contador > 0:
            Usuario.ultimo_id = contador
        elif self.usuarios:
            Usuario.ultimo_id = max(u.id for u in self.usuarios)
        else:
            Usuario.ultimo_id = 0

    def _guardar_contador(self):
        """Guarda el contador de IDs en el archivo"""
        self.data_handler.save_counter("usuario_id", Usuario.ultimo_id)

    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        return self.usuarios

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        for usuario in self.usuarios:
            if usuario.id == id:
                return usuario
        return None

    def buscar(self, termino: str) -> List[Usuario]:
        """Busca usuarios que coincidan con el término de búsqueda"""
        resultados = []
        termino = termino.lower()
        for usuario in self.usuarios:
            if (termino in usuario.nombre.lower() or
                    termino in usuario.email.lower() or
                    termino in str(usuario.id).lower() or
                    termino in usuario.telefono.lower()):
                resultados.append(usuario)
        return resultados

    def crear(self, nombre: str, email: str, telefono: str) -> Usuario:
        """Crea un nuevo usuario"""
        usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
        self.usuarios.append(usuario)
        self.data_handler.save_data(self.usuarios)
        self._guardar_contador()
        return usuario

    def actualizar(self, id: int, nombre: str = None, email: str = None, telefono: str = None) -> Optional[Usuario]:
        """Actualiza un usuario existente"""
        usuario = self.obtener_por_id(id)
        if usuario:
            if nombre is not None:
                usuario.nombre = nombre
            if email is not None:
                usuario.email = email
            if telefono is not None:
                usuario.telefono = telefono
            self.data_handler.save_data(self.usuarios)
            return usuario
        return None

    def eliminar(self, id: int) -> bool:
        """Elimina un usuario por su ID"""
        usuario = self.obtener_por_id(id)
        if usuario:
            self.usuarios.remove(usuario)
            self.data_handler.save_data(self.usuarios)
            return True
        return False