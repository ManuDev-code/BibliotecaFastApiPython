from typing import List, Optional
from app.models.Libro import Libro
from app.utils.data_handler import DataHandler


class LibroService:
    def _init_(self):
        self.data_handler = DataHandler[Libro]("data/libros.json", Libro)
        self.libros = self.data_handler.load_data()
        self._cargar_contador()

    def _cargar_contador(self):
        """Carga el contador de IDs desde el archivo o lo inicializa con el máximo ID existente"""
        contador = self.data_handler.load_counter("libro_id")
        if contador > 0:
            Libro.ultimo_id = contador
        elif self.libros:
            Libro.ultimo_id = max(l.id for l in self.libros)
        else:
            Libro.ultimo_id = 0

    def _guardar_contador(self):
        """Guarda el contador de IDs en el archivo"""
        self.data_handler.save_counter("libro_id", Libro.ultimo_id)

    def obtener_todos(self) -> List[Libro]:
        """Obtiene todos los libros"""
        return self.libros

    def obtener_por_id(self, id: int) -> Optional[Libro]:
        """Obtiene un libro por su ID"""
        for libro in self.libros:
            if libro.id == id:
                return libro
        return None

    def buscar(self, termino: str) -> List[Libro]:
        """Busca libros que coincidan con el término de búsqueda"""
        resultados = []
        termino = termino.lower()
        for libro in self.libros:
            if (termino in libro.titulo.lower() or
                    termino in libro.autor.lower() or
                    termino in str(libro.id).lower() or
                    termino in libro.isbn.lower()):
                resultados.append(libro)
        return resultados

    def crear(self, titulo: str, autor: str, isbn: str, descripcion: str) -> Libro:
        """Crea un nuevo libro"""
        libro = Libro(titulo=titulo, autor=autor, isbn=isbn, descripcion=descripcion)
        self.libros.append(libro)
        self.data_handler.save_data(self.libros)
        self._guardar_contador()
        return libro

    def actualizar(self, id: int, titulo: str = None, autor: str = None, isbn: str = None, descripcion: str = None) -> \
    Optional[Libro]:
        """Actualiza un libro existente"""
        libro = self.obtener_por_id(id)
        if libro:
            if titulo is not None:
                libro.titulo = titulo
            if autor is not None:
                libro.autor = autor
            if isbn is not None:
                libro.isbn = isbn
            if descripcion is not None:
                libro.descripcion = descripcion
            self.data_handler.save_data(self.libros)
            return libro
        return None

    def eliminar(self, id: int) -> bool:
        """Elimina un libro por su ID"""
        libro = self.obtener_por_id(id)
        if libro:
            self.libros.remove(libro)
            self.data_handler.save_data(self.libros)
            return True
        return False

    def actualizar_disponibilidad(self, id: int, disponible: bool) -> Optional[Libro]:
        """Actualiza la disponibilidad de un libro"""
        libro = self.obtener_por_id(id)
        if libro:
            libro.disponible = disponible
            self.data_handler.save_data(self.libros)
            return libro
        return None