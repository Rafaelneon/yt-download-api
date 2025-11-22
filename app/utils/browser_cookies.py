from yt_dlp.utils import get_browser_cookies

def get_firefox_cookies():
    """
    Extrai cookies do Firefox.
    Retorna o caminho do cookiefile ou None em caso de falha.
    """
    try:
        cookies = get_browser_cookies("firefox")
        return cookies  # yt-dlp aceita cookiefile ou dict
    except Exception as e:
        print(f"⚠ Falha ao extrair cookies do Firefox: {e}")
        return None
