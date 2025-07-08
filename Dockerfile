# Use official python runtime as base image
FROM python:3.12

# Set enviromental variables 
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 
ENV ACCEPT_EULA=Y
ENV PATH="$PATH:/opt/mssql-tools18/bin"

# Install PostgreSQL client
RUN apt update \
 && apt install -y cifs-utils \
 && apt install -y postgresql-client \
 && apt install -y unixodbc unixodbc-dev \
 && rm -rf var/lib/apt/lists/*
# Install the Microsoft ODBC driver for SQL Server 
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN apt update
RUN apt install -y msodbcsql18 \
 && apt install -y mssql-tools18
# Add dependencies for ldap (for connecting to active directory)
RUN apt install -y python3-dev libldap2-dev libsasl2-dev libssl-dev

# Set the working directory inside the container
WORKDIR /mab

# Copy the project requirements file to the working directory
COPY requirements.txt .

# Make sure we are using the latest version of pip
RUN python -m pip install --upgrade pip
# RUN pip install --upgrade pip setuptools
# Install project dependencies
RUN pip install -r requirements.txt --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org

# Copy the project code to the working directory
COPY . .
