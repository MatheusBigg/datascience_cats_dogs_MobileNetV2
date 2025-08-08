# STRIDE Threat Model Analyzer UPDATE

Este projeto é uma solução completa para análise de ameaças baseada na metodologia STRIDE, composta por um backend em FastAPI (Python) e um front-end em HTML/CSS/JS com visualização de ameaças usando Cytoscape.js.

## Funcionalidades
- Upload de imagem de arquitetura e preenchimento de informações do sistema.
- Extração de texto da imagem usando OCR (easyocr).
- Geração automática de modelo de ameaças STRIDE usando Azure OpenAI.
- Visualização do modelo de ameaças em grafo interativo (Cytoscape.js).
- Sugestões de melhoria para o modelo de ameaças.
- Botão para imprimir/exportar o grafo gerado.

---

## Como executar o projeto

### 1. Pré-requisitos
- Python 3.10+
- Node.js (opcional, apenas se quiser servir o front-end com algum servidor local)
- Conta e deployment configurado no Azure OpenAI (veja variáveis de ambiente)

### 2. Clonando o repositório

```bash
# Clone o projeto
 git clone https://github.com/digitalinnovationone/stride-demo.git
 cd stride-demo
```

### 3. Configurando o backend (FastAPI)

1. Acesse a pasta do backend:
   ```bash
   cd module-1/01-introducao-backend
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` com as seguintes variáveis (preencha com seus dados do Azure OpenAI):
   ```env
   AZURE_OPENAI_API_KEY=xxxxxx
   AZURE_OPENAI_ENDPOINT=https://<seu-endpoint>.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2023-05-15
   AZURE_OPENAI_DEPLOYMENT_NAME=<nome-do-deployment>
   ```
5. Execute o backend:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```
   O backend estará disponível em http://localhost:8001

### 4. Configurando o front-end

1. Acesse a pasta do front-end:
   ```bash
   cd ../02-front-end
   ```
2. Basta abrir o arquivo `index.html` no navegador (duplo clique ou `open index.html`).
   - Se quiser servir via servidor local (opcional):
     ```bash
     npx serve .
     # ou
     python -m http.server 8080
     ```
3. O front-end espera que o backend esteja rodando em http://localhost:8001

---

## Cuidados e dicas
- **Azure OpenAI:** Certifique-se de que seu deployment está ativo e as variáveis do `.env` estão corretas.
- **CORS:** O backend já está configurado para aceitar requisições de qualquer origem, mas se for usar em produção, ajuste as origens permitidas.
- **Limite de tokens:** O modelo do Azure OpenAI pode ter limites de tokens. Ajuste `max_tokens` se necessário.
- **Impressão do grafo:** O botão "Imprimir Grafo" exporta a visualização atual do grafo como imagem para impressão ou PDF.
- **Formato do JSON:** O front-end espera o JSON no formato retornado pelo backend. Se mudar o backend, ajuste o front-end conforme necessário.
- **Portas:** Certifique-se de que as portas 8001 (backend) e 8080 (front-end, se usar servidor) estejam livres.

---

## Estrutura do projeto
```
stride-demo/
│
├── module-1/
│   ├── 01-introducao-backend/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── .env (crie este arquivo)
│   └── 02-front-end/
│       └── index.html
└── README.md
```