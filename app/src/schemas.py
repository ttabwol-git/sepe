import re

from pydantic import BaseModel
from pydantic import field_validator
from pydantic import Field


class Task(BaseModel):
    postal_code: str
    user_email: str

    @field_validator("postal_code", mode="before")
    @classmethod
    def validate_postal_code(cls, value):
        if len(value) != 5:
            raise ValueError("Postal code must be 5 characters long")
        if not value.isdigit():
            raise ValueError("Postal code must be a number")
        if int(value) > 52006:
            raise ValueError("Invalid postal code")
        return value

    @field_validator("user_email", mode="before")
    @classmethod
    def validate_user_email(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        return value


class URLParams(BaseModel):
    idCliente: str = "39"
    codigoEntidad: str = ""
    idGrupoServicio: str = "8"
    idTipoAtencion: str = "1"
    idTipoAtencionTR: str = "0"
    codigoPostal: str
    latOrigen: str
    lngOrigen: str
    idsJerarquiaTramites: str = "5"


class Office(BaseModel):
    id: str = Field(..., alias="codigoOficina")
    name: str = Field(..., alias="oficina")
    address: str = Field(..., alias="direccion")
    phone: str = Field(..., alias="telefono")
    working_hours: str = Field(..., alias="horarioAtencion")
    first_available_time: str = Field(..., alias="primerHuecoDisponible")
