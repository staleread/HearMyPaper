import httpx

from .auth.module import AuthModule
from .conversion.module import ConversionModule
from .submission.module import SubmissionModule
from .user.module import UserModule


class HmpManagerClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.auth = AuthModule(client)
        self.user = UserModule(client)
        self.submission = SubmissionModule(client)
        self.conversion = ConversionModule(client)

    async def check_health(self) -> str:
        """Checks the health of the manager service."""
        response = await self.client.get("/health")
        response.raise_for_status()
        return response.text
