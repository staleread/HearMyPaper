
import httpx

from .models import AccessClaims


class OPAClient:
    """
    Client for interacting with Open Policy Agent (OPA) for authorization decisions.
    """

    def __init__(self, base_url: str = "http://localhost:8181"):
        self.base_url: str = base_url

    async def get_workload_claims(self, spiffe_id: str) -> AccessClaims | None:
        """
        Query OPA for the AccessClaims associated with a SPIFFE ID.
        """
        url = f"{self.base_url}/v1/data/hmp/workloads/claims"
        # In a real setup, you might pass the spiffe_id as part of the query
        # or have a policy that filters based on input.
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json={"input": {"spiffe_id": spiffe_id}}
                )
                response.raise_for_status()
                result = response.json().get("result")
                if result:
                    return AccessClaims(**result)
        except Exception:
            # Fallback or log error
            pass
        return None

    async def get_stacked_decision(
        self, 
        spiffe_id: str | None, 
        user_claims: AccessClaims, 
        required_level: str,
        access_type: str
    ) -> bool:
        """
        Query OPA for a final 'allow' decision based on composite identity.
        """
        url = f"{self.base_url}/v1/data/hmp/authz/allow"
        input_data = {
            "input": {
                "workload_id": spiffe_id,
                "user": user_claims.model_dump(),
                "required_level": required_level,
                "access_type": access_type
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=input_data)
                response.raise_for_status()
                return response.json().get("result", False)
        except Exception:
            return False
