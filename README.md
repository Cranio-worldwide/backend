## Cranio-WorldWide project - backend
**Web-site for internation federation of therapists: helps patients to find a therapist nearby**
### Technologies
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
### MVP Features
- Internationalization using i18n (English & Russian);
- Automated translation/transliteration of models into supported languages;
- Determine user geolocation by IP-address;
- Authentification using JWT;
- Models: Users with Addresses & Services, News;  
- Search via geolocation with flexible radius and price range; 

### Setup for developers
```
>>> Clone project repository:
git clone git@github.com:Cranio-worldwide/backend.git
```
```
>>> Open folder with project, create docker container and apply migrations:
cd backend
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
```
### Fill DB with fixtures for tests
```
>>> csv files with users, addresses, services, news
docker-compose exec backend python manage.py import_csv
>>> json with translation of static content for frontend
docker-compose exec backend python manage.py import_json
```
### .env file template
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='djangosercretkey!!1'
```
### API Documentation
http://127.0.0.1:8000/redoc/
http://127.0.0.1:8000/swagger/
### New features coming up soon
TBD