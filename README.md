```md
# 🎵📹 API de Download YouTube — Pytubefix

Uma API simples e rápida para baixar vídeos e músicas do YouTube usando **pytubefix**.  
Ideal para automatizar processos em bots, sistemas internos e aplicações web.

---

# 🚀 Tecnologias utilizadas

- **FastAPI**
- **Uvicorn**
- **Python-dotenv**
- **Pytubefix**
- **HTTPX**

---

# 📁 Configuração inicial

Crie o arquivo `.env` na raiz do projeto:

```env
DOWNLOADS_PATH=/caminho/para/salvar/arquivos
```

A API criará automaticamente as pastas:

- `/video`
- `/music`

---

# 📦 Instalação

### 1️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Inicie a API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

# 🖥 Acesso ao Painel Web

Abra no navegador:

```
http://SEU_IP:8000
```

O painel inclui:

- 📥 Downloads  
- 📋 Fila  
- 📊 Status da API  
- 📚 Documentação  
- 🔎 Verificação de arquivos baixados  

---

# 🧪 Pasta de testes

Dentro da pasta **teste/** existem scripts para testar a API:

### ✔ `teste/downloads.py`
Script para enviar links e acionar downloads pela API.

### ✔ `teste/status.py`
Consulta o status da fila e os itens concluídos.

Esses arquivos ajudam a integrar a API em outras aplicações sem precisar abrir o painel web.

---

# 🎯 Funções principais

### ➤ Baixar vídeo ou música
- Informe o link  
- Escolha o formato (MP3 ou MP4)  
- O arquivo será salvo em:
  - `/video`
  - `/music`

### ➤ Download múltiplo
Aceita lista de URLs simultaneamente.

### ➤ Verificar se o link já foi baixado
Endpoint dedicado para consulta de downloads existentes.

---

# ⚠ Observação importante

❗ **A API não possui persistência de fila.**  
Ao reiniciar o servidor, **a fila é zerada** (somente os arquivos continuam salvos).

---

# 🤝 Contribuição

Melhorias são bem-vindas!  
Sinta-se livre para enviar **PRs**, abrir **issues** ou modificar o painel.

---

# 📄 Licença

Uso livre para qualquer projeto **pessoal ou profissional**.
```
