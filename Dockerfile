From python:3.12

WORKDIR /Ecom-Site

RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get install -y gcc g++ && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt
 
CMD [ "python", "app.py" ]