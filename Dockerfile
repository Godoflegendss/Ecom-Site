FROM python:3.10-slim

WORKDIR /Ecom-Site

# Install system dependencies for ODBC + build tools
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft SQL ODBC driver repo
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list \
    -o /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt
 
COPY . .
# Expose Flask port
EXPOSE 5000
CMD [ "python", "app.py" ]
