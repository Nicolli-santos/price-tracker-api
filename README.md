# 📈 Price Tracker API

Uma API RESTful desenvolvida em **Python** com **FastAPI** para monitorar preços de produtos na web e salvar o histórico de variações em um banco de dados relacional.

---

## 🚀 Tecnologias Utilizadas

- **Python 3**
- **FastAPI**: Framework web de alta performance para construção das APIs.
- **SQLAlchemy**: ORM para manipulação do banco de dados relacional.
- **SQLite**: Banco de dados leve e embarcado.
- **Pydantic**: Validação de dados e esquemas.
- **HTTPX & BeautifulSoup4**: Scraping para extração de preços diretamente de páginas da web.

---

## 📌 Funcionalidades da API

- **`POST /products`**: Cadastra um novo produto informando nome, URL e preço-alvo.
- **`GET /products`**: Lista todos os produtos cadastrados na base de dados.
- **`POST /products/{product_id}/check-price`**: Executa o robô de raspagem (scraper) na URL do produto, lê o preço atualizado da internet e salva um novo registro no histórico.

---

## 🛠️ Como Executar o Projeto Localmente

1. **Clone o repositório:**
