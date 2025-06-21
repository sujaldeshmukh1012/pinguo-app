Here's a **comprehensive `README.md`** for the **backend Django repository** of the Pinguo Dashboard app.

---


# 🐧 Pinguo Dashboard Backend

The **Pinguo Dashboard Backend** powers the core functionality of the teacher-side admin interface in the Pinguo language learning platform. Built using **Django** and **Django REST Framework**, this backend handles content creation, test management, media storage, JWT authentication, and integration with a React frontend dashboard.

---

## 🚀 Key Features

- 📚 **Course & Lesson Management**
- 🗣️ **Dialogue Groups with Audio & Image Modals**
- 🧠 **Custom Test Cards with Multiple Answer Types**
- 🔐 **JWT-Based Authentication**
- 🌍 **Cloud Media Storage (DigitalOcean Spaces via S3)**
- 📤 **REST API Endpoints for Frontend Integration**
- 🧩 **Dynamic Drag & Drop Item Management**
- 🎛️ **Admin Interface via Django + Jazzmin**

---

## 🧱 Project Structure

```

dashboard\_backend/
├── dashboard\_backend/       # Project settings & root config
├── course/                  # Lessons, metadata & course-related models
├── dialogue/                # Dialogue, Balloons, Images, Test Cards
├── word\_card/               # Word flashcards or related resources
├── dictionary/              # Dictionary entries and utilities
├── alerts/                  # Notification & alert system
├── authorization/           # JWT Auth & User profile extensions
└── media/ / static/         # (Optional) Local storage fallback

````

---

## 🧑‍🏫 Functional Overview

### 📘 Dialogue Module

Handles conversational data:
- `DialogueGroup`: A container for dialogues in a lesson
- `Dialogue`: Contains audio, image, and text balloon entries
- `Ballon`: Holds text + audio + ideogram + pronunciation
- `ImageModal`: Hints-based image cards for visual learning
- `TestCard` and `TestAnswer`: Custom quiz system per dialogue

### 🧪 Test System

Each `TestCard` belongs to a `DialogueGroup`, referencing:
- Dialogue
- Related Balloon
- Answers (`ideogram`, `pinyin`, or `meaning` type)

Includes automatic linking in the dialogue arrangement list.

---

## ⚙️ Setup Instructions

### 🔐 Prerequisites

- Python 3.10+
- Django 4.1+
- PostgreSQL / SQLite
- `pipenv` or `venv` for environment management

### 📦 Installation

```bash
git clone https://github.com/your-org/pinguo-dashboard-backend.git
cd pinguo-dashboard-backend

# Create virtual env
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (use .env file)
cp .env.example .env
````

### 🛠️ Environment Variables (`.env`)

```env
SECRET_KEY=your_secret_key
DEBUG=True

# AWS S3 (DigitalOcean Spaces or other)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_ENDPOINT_URL=...
AWS_LOCATION=static
AWS_MEDIA_LOCATION=media
```

### 🗄️ Migrations & Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 🔄 Run Server

```bash
python manage.py runserver
```

### 🧪 API Auth Test

Use JWT via `/api/token/` and `/api/token/refresh/` endpoints.
Headers for authenticated routes:

```http
Authorization: Bearer <your_access_token>
```

---

## ☁️ Cloud Storage

Uses **DigitalOcean Spaces** (or any S3-compatible service) for:

* Media: `MEDIA_URL`
* Static files: `STATIC_URL`

Uses Django's `storages` and `boto3`.

---

## 🔒 Security

* JWT Authentication via `rest_framework_simplejwt`
* CORS open to all (`CORS_ORIGIN_ALLOW_ALL=True`) — **restrict in production**

---

## 🧰 Admin Panel

Powered by [Jazzmin](https://github.com/farridav/django-jazzmin), for an enhanced Django Admin UI.

---

## 🧪 API Stack

* `rest_framework`
* `rest_framework_simplejwt`
* `corsheaders`
* `decouple` for config
* `storages` + `boto3` for file hosting

---

## 🧠 Models Snapshot

> Dialogue Content Models

* `DialogueGroup` → `Dialogue` → `Ballon`, `ImageModal`
* `TestCard` → `TestAnswer`
* `DGItemListMain` → handles drag-n-drop ordering & dynamic updates

---


## 🐳 Docker Support

### 1. `Dockerfile`

```Dockerfile
# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the app
CMD ["gunicorn", "dashboard_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 2. `docker-compose.yml`

```yaml
version: "3.9"

services:
  web:
    build: .
    command: gunicorn dashboard_backend.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: pinguo
      POSTGRES_USER: rootuser
      POSTGRES_PASSWORD: rootuser9683
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3. `.dockerignore`

```
__pycache__/
*.pyc
*.pyo
*.pyd
*.sqlite3
env/
venv/
*.env
/media
/static
```

---

## 🔁 GitHub Actions CI/CD

### `.github/workflows/deploy.yml`

```yaml
name: Django CI/CD

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: pinguo
          POSTGRES_USER: rootuser
          POSTGRES_PASSWORD: rootuser9683
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DEBUG: 0
      SECRET_KEY: ${{ secrets.SECRET_KEY }}
      DB_NAME: pinguo
      DB_USER: rootuser
      DB_PASSWORD: rootuser9683
      DB_HOST: localhost

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run migrations
        run: |
          python manage.py makemigrations
          python manage.py migrate

      - name: Run tests
        run: |
          python manage.py test
```

> 🔒 Store sensitive variables (e.g., `SECRET_KEY`, DB creds) in **GitHub repo secrets**.

---
## 🧾 License

This project is **private and proprietary** to the Pinguo development team. Unauthorized use or distribution is prohibited.

---

## 👨‍💻 Contributors

Maintained by the SUJAL DATTARAO BHAKARE.

---

