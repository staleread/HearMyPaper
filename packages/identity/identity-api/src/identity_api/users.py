from typing import override
from shared_kernel.marshal import from_b64, to_b64
from datetime import datetime

from blacksheep import FromJSON
from blacksheep.server.responses import created, not_found, ok, status_code
from blacksheep.server.controllers import Controller, get, post, put
from pydantic import BaseModel, EmailStr

from identity_core.enums import AccessLevel
from identity_core.exceptions import (
    IdentityCollisionError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from identity_core.ports.incoming import (
    CreateUserPort,
    GetUserPort,
    GetUserPublicKeyPort,
    UpdateUserPort,
    UserCreateCommand,
    UserUpdateCommand,
)


class UserCreateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    public_key_b64: str
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserUpdateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]


class UserResponse(BaseModel):
    id: str
    name: str
    surname: str
    email: EmailStr
    confidentiality_level: AccessLevel
    integrity_levels: list[AccessLevel]
    created_at: datetime


class PublicKeyResponse(BaseModel):
    public_key_b64: str


class UsersController(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/users"

    def __init__(
        self,
        create_user_port: CreateUserPort,
        get_user_port: GetUserPort,
        get_user_public_key_port: GetUserPublicKeyPort,
        update_user_port: UpdateUserPort,
    ) -> None:
        self.create_user_port = create_user_port
        self.get_user_port = get_user_port
        self.get_user_public_key_port = get_user_public_key_port
        self.update_user_port = update_user_port

    @post("/")
    async def create_user(self, data: FromJSON[UserCreateRequest]):
        req = data.value
        try:
            cmd = UserCreateCommand(
                name=req.name,
                surname=req.surname,
                email=req.email,
                public_key=from_b64(req.public_key_b64),
                confidentiality_level=req.confidentiality_level,
                integrity_levels=req.integrity_levels,
            )
            user = await self.create_user_port(cmd)
            return created(
                UserResponse(
                    id=user.id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    confidentiality_level=user.confidentiality_level,
                    integrity_levels=user.integrity_levels,
                    created_at=user.created_at,
                ),
                f"/users/{user.id}",
            )
        except (UserAlreadyExistsError, IdentityCollisionError) as e:
            return status_code(409, str(e))

    @get("/{user_id}")
    async def get_user(self, user_id: str):
        """Retrieves a user by ID."""
        try:
            user = await self.get_user_port(user_id)
            return ok(
                UserResponse(
                    id=user.id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    confidentiality_level=user.confidentiality_level,
                    integrity_levels=user.integrity_levels,
                    created_at=user.created_at,
                )
            )
        except UserNotFoundError as e:
            return not_found(str(e))

    @get("/{user_id}/public-key")
    async def get_user_public_key(self, user_id: str):
        """Retrieves a user's public key by ID."""
        try:
            public_key = await self.get_user_public_key_port(user_id)
            return ok(PublicKeyResponse(public_key_b64=to_b64(public_key)))
        except UserNotFoundError as e:
            return not_found(str(e))

    @put("/{user_id}")
    async def update_user(self, user_id: str, data: FromJSON[UserUpdateRequest]):
        req = data.value
        try:
            cmd = UserUpdateCommand(
                name=req.name,
                surname=req.surname,
                email=req.email,
                confidentiality_level=req.confidentiality_level,
                integrity_levels=req.integrity_levels,
            )
            user = await self.update_user_port(user_id, cmd)
            return ok(
                UserResponse(
                    id=user.id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    confidentiality_level=user.confidentiality_level,
                    integrity_levels=user.integrity_levels,
                    created_at=user.created_at,
                )
            )
        except UserNotFoundError as e:
            return not_found(str(e))
        except UserAlreadyExistsError as e:
            return status_code(409, str(e))
