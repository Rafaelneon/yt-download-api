import requests
import time

BASE_URL = "http://127.0.0.1:8000/youtube"
CHECK_INTERVAL = 5

def get_queue():
    try:
        response = requests.get(f"{BASE_URL}/queue")

        if response.status_code == 200:
            queue = response.json()

            if not queue:
                print("A fila está vazia.")

            for item in queue:

                # 🔥 VERIFICA SE O ITEM É UM DICIONÁRIO
                if not isinstance(item, dict):
                    print("Item inválido recebido na fila:", item)
                    print("-" * 40)
                    continue

                print(f"URL: {item.get('url')}")
                print(f"Tipo: {item.get('type')}")
                print(f"Status: {item.get('status')}")

                result = item.get('result')
                if isinstance(result, dict):
                    print(f"Arquivo: {result.get('filename', 'não disponível')}")
                    print(f"Caminho: {result.get('path', 'não disponível')}")

                print("-" * 40)

        else:
            print(f"Erro {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Erro ao consultar fila: {e}")

def main():
    print("Iniciando monitoramento da fila de downloads...\n")
    while True:
        get_queue()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
