FROM python:3.10-slim

WORKDIR /Ecom-Site


# Install basic tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    lsb-release \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft ODBC driver repo using new method
RUN curl https://packages.microsoft.com/config/debian/11/prod.list \
    -o /etc/apt/sources.list.d/mssql-release.list && \
    curl https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt
 
COPY . .
# Expose Flask port
EXPOSE 5000
CMD [ "python", "app.py" ]
