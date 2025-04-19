# Showroom App Web Based
Car showroom website powered by Django

# Tutorial

## Prerequisite

```bash
pip install -r requirements.txt
```

Make sure your Docker is updated

```bash
curl -fsSL https://get.docker.com | sh
sudo <your_package_repo, e.g., apt, yum> install docker-compose
```

Create and set .env.prod

```env
DEBUG=0
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-public-ip,domain.com,localhost
DATABASE_URL=postgres://USER:PASSWORD@YOUR-DATABASE-IP:5432/DB_NAME
```

## Start Docker

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Install PostgreSQL
- On local
  
  ```bash
  sudo <your_package_repo, e.g., apt> install postgresql
  ```
- On docker
  
  ```bash
  docker-compose -f docker-compose.prod.yml exec web <your_package_repo, e.g., apt> install postgresql
  ```

## Initiate database
- Login psql
  
  ```bash
  psql -h <your_database_ip> -p <port> -U <username>
  ```
- Create a database
  
  ```bash
  CREATE DATABASE <your_database_name>;
  ```
  **Note**:
  - Please use username that same with your DATABASE_URL env
  - If you install postgres on odcker, execute on bash
    
    ```bash
    # enter bash on docker before login psql
    docker-compose -f docker-compose.prod.yml exec web bash
    ```

## Initiate Django Model (migration)

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations showroom_app
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## Create admin user

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Install CA for HTTPS (if you haven't public domain)

```bash
sudo apt install libnss3-tools
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo mv mkcert-v*-linux-amd64 /usr/local/bin/mkcert
mkcert -install
mkcert -key-file key.pem -cert-file cert.pem <your_ip>
```
**Recommendation**: use nginx for web service (public domain needed) (future feature)

## Update gunicorn command in Dockerfile.prod
```bash
# at last line
CMD ["gunicorn", "showroom_project.wsgi:application", "--bind", "0.0.0.0:443", "--certfile", "cert.pem", "--keyfile", "key.pem"]
```

## Q/A and Bug report
If you have any questions or bug reports, please ask/report through the Issue feature. The title of the question should be `Q/A—Your Question`. The title of bug report should be `BUG-Bug Outlines`. Capture all error logs or submit the log file. Explain briefly.

Feel free to contribute guys ☻
