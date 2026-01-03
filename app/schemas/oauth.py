from pydantic import BaseModel

class AppleAuthRequest(BaseModel):
    identity_token: str
    user_id: str  # Apple user ID
    email: str | None = None
    full_name: str | None = None

class GoogleAuthRequest(BaseModel):
    id_token: str