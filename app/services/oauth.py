from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
import requests
from app.core.config import settings


async def verify_google_token(token: str) -> dict:
    """Verifica el token de Google y devuelve los datos del usuario"""
    try:
        # Verificar token con Google
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        return {
            "email": idinfo["email"],
            "name": idinfo.get("name"),
            "google_id": idinfo["sub"],
        }
    except Exception as e:
        raise ValueError(f"Invalid Google token: {str(e)}")


async def verify_apple_token(identity_token: str) -> dict:
    """Verifica el token de Apple y devuelve los datos del usuario"""
    try:
        # Apple usa JWT estándar
        # En producción deberías verificar con las claves públicas de Apple (JWKS)
        # Por ahora, decodificamos sin verificar firma (solo para desarrollo)

        # Decodificar header para obtener el kid (key id)
        unverified_header = jwt.get_unverified_header(identity_token)

        # Obtener las claves públicas de Apple
        keys_url = "https://appleid.apple.com/auth/keys"
        response = requests.get(keys_url)
        apple_keys = response.json()

        # Encontrar la clave correcta
        public_key = None
        for key in apple_keys['keys']:
            if key['kid'] == unverified_header['kid']:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                break

        if not public_key:
            raise ValueError("Public key not found")

        # Verificar y decodificar el token
        decoded = jwt.decode(
            identity_token,
            public_key,
            algorithms=['RS256'],
            audience=settings.APPLE_CLIENT_ID,  # Bundle ID de tu app
            issuer='https://appleid.apple.com'
        )

        return {
            "email": decoded.get("email"),
            "apple_id": decoded["sub"],
        }
    except jwt.ExpiredSignatureError:
        raise ValueError("Apple token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid Apple token: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error verifying Apple token: {str(e)}")