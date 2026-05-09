from shared_kernel.marshal import from_b64, to_b64
from typing import override

from blacksheep import FromJSON
from blacksheep.server.responses import not_found, ok, unauthorized
from blacksheep.server.controllers import Controller, post

from pydantic import BaseModel

from identity_core.exceptions import (
    AuthenticationFailedError,
    InvalidChallengeError,
    UserNotFoundError,
)
from identity_core.ports.incoming import (
    FinalizeLoginPort,
    InitLoginPort,
    LoginCommand,
)


class ChallengeRequest(BaseModel):
    id: str


class ChallengeResponse(BaseModel):
    challenge_b64: str


class LoginRequest(BaseModel):
    id: str
    challenge_b64: str
    signature_b64: str


class LoginResponse(BaseModel):
    token: str


class AuthController(Controller):
    @classmethod
    @override
    def route(cls) -> str | None:
        return "/auth"

    def __init__(
        self,
        init_login_port: InitLoginPort,
        finalize_login_port: FinalizeLoginPort,
    ) -> None:
        self.init_login_port = init_login_port
        self.finalize_login_port = finalize_login_port

    @post("/challenge")
    async def create_challenge(self, data: FromJSON[ChallengeRequest]):
        """
        Generate a cryptographic challenge for user authentication.
        """
        req = data.value
        try:
            challenge_bytes = await self.init_login_port(req.id)
            return ok(ChallengeResponse(challenge_b64=to_b64(challenge_bytes)))
        except UserNotFoundError as e:
            return not_found(str(e))

    @post("/login")
    async def execute_login(self, data: FromJSON[LoginRequest]):
        """
        Finalize user authentication and issue an access token.
        """
        req = data.value
        cmd = LoginCommand(
            id=req.id,
            challenge=from_b64(req.challenge_b64),
            signature=from_b64(req.signature_b64),
        )

        try:
            auth_token = await self.finalize_login_port(cmd)
            return ok(LoginResponse(token=auth_token.token))
        except UserNotFoundError as e:
            return not_found(str(e))
        except InvalidChallengeError, AuthenticationFailedError:
            return unauthorized("Invalid challenge or signature")
