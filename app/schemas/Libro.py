from pydantic import BaseModel, Field

class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field("", max_length=20)
    descripcion: str = Field("", max_length=1000)

class LibroCreate(LibroBase):
    pass

class LibroUpdate(BaseModel):
    titulo: str = Field(None, min_length=1, max_length=200)
    autor: str = Field(None, min_length=1, max_length=100)
    isbn: str = Field(None, max_length=20)
    descripcion: str = Field(None, max_length=1000)

class LibroResponse(LibroBase):
    id: int
    disponible: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "titulo": "Don Quijote de la Mancha",
                "autor": "Miguel de Cervantes",
                "isbn": "9788420412146",
                "descripcion": "Obra cumbre de la literatura española",
                "disponible": True
            }
        }