# Use uma imagem oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências e instale-as
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto do código do seu backend para o container
COPY . .

# Exponha a porta que o Gunicorn irá usar
EXPOSE $PORT

# Comando para rodar a aplicação
CMD gunicorn --bind 0.0.0.0:$PORT app:app