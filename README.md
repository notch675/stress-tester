# HTTP Stress Tester

Uma ferramenta simples e eficiente para realizar testes de estresse em servidores HTTP com suporte a múltiplas conexões assíncronas, requisições GET/POST personalizadas e uma interface gráfica amigável construída com `ttkbootstrap`.

## 📋 Recursos

- ✅ Interface gráfica com `ttkbootstrap`
- 🔁 Suporte a múltiplas conexões simultâneas usando `asyncio` e `aiohttp`
- 🔫 Métodos HTTP: `GET` e `POST`
- 🧠 Envio de payloads JSON (para POST)
- 🧾 Adição de headers personalizados
- 🍪 Suporte a cookies
- 📊 Exibição em tempo real de:
  - Total de requisições feitas
  - Requisições bem-sucedidas (status 2xx)
  - Requisições com erro (status 4xx/5xx)
  - Tempo médio de resposta

## 📦 Requisitos

- Python 3.9+
- Bibliotecas:

pip install aiohttp ttkbootstrap

Clone o repositório:
git clone https://github.com/seu-usuario/http-stress-tester.git
cd http-stress-tester

Execute o script principal:

python stress_tester_gui.py

Preencha os campos:

URL de destino

Método HTTP (GET ou POST)

Número de conexões simultâneas

Número total de requisições

(Opcional) Headers, cookies e payload JSON

Clique em "Iniciar Teste" e acompanhe os resultados em tempo real.

🖼️ Interface

<img width="767" height="968" alt="Captura de tela 2025-08-05 204336" src="https://github.com/user-attachments/assets/8327e401-2397-4b71-864b-4fae34c76ddb" />

⚠️ Aviso legal
Esta ferramenta é destinada apenas para testes autorizados. Nunca use este programa para atacar sistemas sem permissão expressa. O uso indevido pode violar leis locais e internacionais.

🛠️ Contribuindo
Contribuições são bem-vindas! Abra uma issue ou envie um pull request com melhorias.
