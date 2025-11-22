import sys
import requests

# =========================
# CONFIGURAÇÃO
# =========================
BASE_URL = "http://192.168.15.10:8000/youtube"  # URL base da API

# =========================
# FUNÇÃO PARA ADICIONAR DOWNLOAD
# =========================
def add_download(url: str, type_: str):
    """
    Adiciona um download à fila.
    type_: 'video' ou 'music'
    """
    payload = {"url": url, "type_": type_}
    try:
        response = requests.post(f"{BASE_URL}/download", params=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Download adicionado: {data['url']} ({data['type']})")
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Erro ao adicionar download: {e}")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python fazerdownload.py [video|music] <URL>")
        sys.exit(1)

    type_ = sys.argv[1].lower()
    url = sys.argv[2]

    if type_ not in ["video", "music"]:
        print("Tipo inválido! Use 'video' ou 'music'.")
        sys.exit(1)

    add_download(url, type_)
