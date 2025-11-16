from authlib.integrations.starlette_client import OAuth
from app.config import settings


# Initialize OAuth with Google configuration
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_uri': settings.google_oauth_redirect_uri,
    }
)


def get_oauth_client():
    """Get configured OAuth client for Google"""
    return oauth.google
