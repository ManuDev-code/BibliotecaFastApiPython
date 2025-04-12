from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from app.schemas.Usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.Biblioteca_service import BibliotecaService

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Usuario no encontrado"}}
)


def get_biblioteca_service():
    service = BibliotecaService()
    service.inicializar()
    return service


@router.get("/", response_model=List[UsuarioResponse])
def obtener_usuarios(
        termino: str = None,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Obtiene todos los usuarios o busca por un término
    """
    if termino:
        usuarios = biblioteca_service.usuario_service.buscar(termino)
    else:
        usuarios = biblioteca_service.usuario_service.obtener_todos()

    return [UsuarioResponse(**usuario.to_dict()) for usuario in usuarios]


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
        usuario_id: int,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Obtiene un usuario por su ID
    """
    usuario = biblioteca_service.usuario_service.obtener_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return UsuarioResponse(**usuario.to_dict())


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
        usuario: UsuarioCreate,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Crea un nuevo usuario
    """
    nuevo_usuario = biblioteca_service.usuario_service.crear(
        nombre=usuario.nombre,
        email=usuario.email,
        telefono=usuario.telefono
    )
    return UsuarioResponse(**nuevo_usuario.to_dict())


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
        usuario_id: int,
        usuario: UsuarioUpdate,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Actualiza un usuario existente
    """
    # Verificar que el usuario existe
    usuario_existente = biblioteca_service.usuario_service.obtener_por_id(usuario_id)
    if not usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )

    # Actualizar solo los campos proporcionados
    usuario_actualizado = biblioteca_service.usuario_service.actualizar(
        id=usuario_id,
        nombre=usuario.nombre,
        email=usuario.email,
        telefono=usuario.telefono
    )

    return UsuarioResponse(**usuario_actualizado.to_dict())


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
        usuario_id: int,
        biblioteca_service: BibliotecaService = Depends(get_biblioteca_service)
):
    """
    Elimina un usuario
    """
    # Verificar que el usuario existe
    usuario = biblioteca_service.usuario_service.obtener_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )

    # Eliminar el usuario
    biblioteca_service.usuario_service.eliminar(usuario_id)