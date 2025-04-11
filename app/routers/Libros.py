from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from app.schemas.Libro import LibroCreate, LibroUpdate, LibroResponse
from app.services.Biblioteca_service import BibliotecaService

router = APIRouter(
    prefix="/libros",
    tags=["libros"],
    responses={404: {"description": "Libro no encontrado"}}
)


def get_biblioteca_service():
    service = BibliotecaService()
    service.inicializar()
    return service


@router.get("/", response_model=List[LibroResponse])
def obtener_libros(
        termino: str = None,
        disponible: bool = None,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Obtiene todos los libros o busca por un término y/o disponibilidad
    """
    if termino:
        libros = biblioteca_service.libro_service.buscar(termino)
    else:
        libros = biblioteca_service.libro_service.obtener_todos()

    # Filtrar por disponibilidad si se especifica
    if disponible is not None:
        libros = [libro for libro in libros if libro.disponible == disponible]

    return [LibroResponse(**libro.to_dict()) for libro in libros]


@router.get("/{libro_id}", response_model=LibroResponse)
def obtener_libro(
        libro_id: int,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Obtiene un libro por su ID
    """
    libro = biblioteca_service.libro_service.obtener_por_id(libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return LibroResponse(**libro.to_dict())


@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
def crear_libro(
        libro: LibroCreate,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Crea un nuevo libro
    """
    nuevo_libro = biblioteca_service.libro_service.crear(
        titulo=libro.titulo,
        autor=libro.autor,
        isbn=libro.isbn,
        descripcion=libro.descripcion
    )
    return LibroResponse(**nuevo_libro.to_dict())


@router.put("/{libro_id}", response_model=LibroResponse)
def actualizar_libro(
        libro_id: int,
        libro: LibroUpdate,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Actualiza un libro existente
    """
    # Verificar que el libro existe
    libro_existente = biblioteca_service.libro_service.obtener_por_id(libro_id)
    if not libro_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )

    # Actualizar solo los campos proporcionados
    libro_actualizado = biblioteca_service.libro_service.actualizar(
        id=libro_id,
        titulo=libro.titulo,
        autor=libro.autor,
        isbn=libro.isbn,
        descripcion=libro.descripcion
    )

    return LibroResponse(**libro_actualizado.to_dict())


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(
        libro_id: int,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Elimina un libro
    """
    # Verificar que el libro existe
    libro = biblioteca_service.libro_service.obtener_por_id(libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )

    # Eliminar el libro
    biblioteca_service.libro_service.eliminar(libro_id)