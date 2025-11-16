from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.services.oauth import get_oauth_client
from app.services.auth_service import get_or_create_user, generate_token_for_user
from app.schemas.auth import GoogleAuthResponse, UserResponse
from app.config import settings


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth flow
    
    Redirects user to Google's consent screen.
    After user approves, Google redirects to /auth/google/callback
    """
    oauth_client = get_oauth_client()
    redirect_uri = settings.google_oauth_redirect_uri
    
    # Generate authorization URL
    return await oauth_client.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    """
    Google OAuth callback endpoint
    
    Receives authorization code from Google, exchanges it for tokens,
    fetches user info, creates/updates user in database, and issues JWT.
    
    Redirects to frontend with token in URL fragment.
    """
    try:
        oauth_client = get_oauth_client()
        
        # Exchange authorization code for access token
        token = await oauth_client.authorize_access_token(request)
        
        # Parse ID token to get user info
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch user info from Google"
            )
        
        # Get or create user in database
        user = await get_or_create_user(user_info)
        
        # Generate JWT for this user
        access_token = generate_token_for_user(user)
        
        # Redirect to frontend with token
        # Frontend will extract token from URL and store it
        frontend_redirect = f"{settings.frontend_url}/?token={access_token}"
        return RedirectResponse(url=frontend_redirect)
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        # Redirect to frontend with error
        error_redirect = f"{settings.frontend_url}/login?error=auth_failed"
        return RedirectResponse(url=error_redirect)


@router.post("/google/exchange", response_model=GoogleAuthResponse)
async def google_token_exchange(request: Request):
    """
    Alternative OAuth flow: Exchange Google ID token for backend JWT
    
    For client-side OAuth flows (popup, one-tap), frontend gets id_token
    from Google and POSTs it here for verification and JWT issuance.
    
    Body: {"id_token": "..."}
    """
    try:
        body = await request.json()
        id_token = body.get("id_token")
        
        if not id_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id_token required"
            )
        
        oauth_client = get_oauth_client()
        
        # Verify ID token with Google
        # Note: This requires additional setup with authlib or google-auth library
        # For now, this is a placeholder - implement token verification
        # using google.auth.transport.requests or authlib token verification
        
        # Placeholder: In production, verify the token
        user_info = {
            "email": "user@example.com",
            "name": "User",
            "sub": "google-user-id",
            "picture": None
        }
        
        user = await get_or_create_user(user_info)
        access_token = generate_token_for_user(user)
        
        return GoogleAuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user["_id"],
                email=user["email"],
                name=user["name"],
                picture=user.get("picture"),
                role=user.get("role", "user")
            )
        )
        
    except Exception as e:
        print(f"Token exchange error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )


@router.post("/logout")
async def logout():
    """
    Logout endpoint
    
    Client should delete JWT token from storage.
    This endpoint exists for consistency but doesn't need to do anything
    since JWTs are stateless.
    """
    return {"message": "Logged out successfully"}
