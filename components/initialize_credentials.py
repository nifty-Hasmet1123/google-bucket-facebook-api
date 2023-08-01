from google.oauth2.credentials import Credentials
import gspread

def init_credentials(access_token: str, refresh_token: str, client_id: str, client_secret: str, token_uri: str) -> gspread.client.Client:
    creds = Credentials.from_authorized_user_info(
        info = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "token_uri": token_uri
        }
    )

    return gspread.authorize(creds)