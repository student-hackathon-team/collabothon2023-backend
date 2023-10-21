from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import Response

from backend.auth.session import SessionData, session_cookie, session_verifier, create_session, \
    delete_session
from backend.commerzbank_apis.client import commerzbank_client

auth_router = APIRouter()


class LoginPayload(BaseModel):
    username: str


@auth_router.post("/login")
async def login_endpoint(payload: LoginPayload, response: Response):
    await create_session(username=payload.username, response=response)

    token = commerzbank_client.fetch_token(
        url="https://api-sandbox.commerzbank.com/auth/realms/sandbox/protocol/openid-connect/token",
        grant_type="client_credentials"
    )


    return f"created session for {payload.username}"


@auth_router.get("/whoami", dependencies=[Depends(session_cookie)])
async def whoami(session_data: SessionData = Depends(session_verifier)):
    return session_data


@auth_router.post("/logout")
async def logout_endpoint(response: Response, session_id: UUID = Depends(session_cookie)):
    await delete_session(session_id, response)
    return "deleted session"
