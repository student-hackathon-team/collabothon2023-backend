from authlib.integrations.requests_client import OAuth2Session

from backend.environment import get_environment

commerzbank_client = OAuth2Session(
    get_environment().commerzbank_api_client_id,
    get_environment().commerzbank_api_client_secret,
    token_endpoint_auth_method="client_secret_post",
)
