from pydantic import BaseModel
from fastapi import HTTPException
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from starlette.responses import Response

from backend.environment import get_environment


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()

# Uses UUID
session_cookie = SessionCookie(
    cookie_name="session_cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=get_environment().cookie_secret,
    cookie_params=cookie_params,
)

session_backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


session_verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=session_backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


async def create_session(username: str, response: Response):
    session_id = uuid4()
    data = SessionData(username=username)

    await session_backend.create(session_id, data)
    session_cookie.attach_to_response(response, session_id)


async def delete_session(session_id: UUID, response: Response):
    await session_backend.delete(session_id)
    session_cookie.delete_from_response(response)
