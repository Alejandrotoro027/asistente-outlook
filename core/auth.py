import os
import msal
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TENANT_ID = os.getenv("TENANT_ID", "common")  # Por defecto 'common' para cuentas personales

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["Mail.ReadWrite", "Mail.ReadWrite.Shared"]

def build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=cache,
    )

def build_auth_url():
    app = build_msal_app()
    return app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI,
    )

def get_token_from_code(auth_code):
    app = build_msal_app()
    result = app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    if "access_token" in result:
        return result["access_token"]
    raise Exception(f"Token error: {result.get('error_description')}")

