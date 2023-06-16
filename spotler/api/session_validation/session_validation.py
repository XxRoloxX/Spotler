from ..spotify_wrapper.spotify_wrapper import SpotifyWrapper


def validate_cookies_presence(session):
    """
    Validates that the session is valid.
    """
    if "code" not in session or "refresh_token" not in session:
        return False
    
def verify_cookies_correctness(session):
    """
    Check if code and refresh token in cookie are correct.
    """

    if not validate_cookies_presence(session):
        return False
    
    code = session["code"]
    refresh_token = session["refresh_token"]

    spotify_wrapper = SpotifyWrapper(code=code, refresh_token=refresh_token)

    if not spotify_wrapper.validate_refresh_token():
        return False
    
    return True

def create_spotify_wrapper_from_session(session):
    """
    Creates a SpotifyWrapper object from the session.
    """
    if not verify_cookies_correctness(session):
        return None
    
    code = session["code"]
    refresh_token = session["refresh_token"]

    spotify_wrapper = SpotifyWrapper(code=code, refresh_token=refresh_token)

    if not spotify_wrapper.validate_refresh_token():
        return None
    
    return spotify_wrapper

