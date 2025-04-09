from pydantic import BaseModel, EmailStr, Field

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telefono: str = Field("", max_length=20)

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: str = Field(None, min_length=1, max_length=100)
    email: EmailStr = None
    telefono: str = Field(None, max_length=20)

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Juan Pérez",
                "email": "juan@example.com",
                "telefono": "555-123-4567"
            }
        }