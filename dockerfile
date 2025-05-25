# Imagem base
FROM python:3.10-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt primeiro para otimizar o cache do Docker
# Se requirements.txt não mudar, esta camada não será reconstruída.
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação para o diretório de trabalho
# O '.' no destino significa o WORKDIR (/app)
COPY . .

# Expõe a porta da aplicação Flask (de acordo com seu config.py, você usa 5003)
# Certifique-se de que a porta no config.py e aqui no Dockerfile correspondam.
EXPOSE 5003

# Comando para rodar a aplicação Flask
# Use 0.0.0.0 para que a aplicação seja acessível de fora do container
# O Flask precisa ser instruído a usar a porta do config.py
CMD ["python", "app.py"]