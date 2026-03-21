# GymTracker Setup & Deployment Guide

## 📋 Project Structure

```
GymTracker/
├── config/                      # Django project config
│   ├── __init__.py
│   ├── settings.py             # Django settings with Cloud SQL support
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI application for Cloud Run
├── tracker/                    # Main Django app
│   ├── migrations/             # Database migrations
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── models.py               # Data models (WorkoutSession, Lift, Set)
│   ├── urls.py                 # App URL routing
│   ├── views.py                # View handlers
│   └── __init__.py
├── templates/                  # HTML templates
│   ├── base.html               # Base template with navigation
│   ├── account/
│   │   └── login.html          # Google OAuth login page
│   └── tracker/
│       ├── workout_form.html   # Workout entry form
│       ├── history.html        # Workout history view
│       └── progress.html       # Weekly progress view
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env                        # Local environment variables
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── Dockerfile                  # Container image definition
└── cloudbuild.yaml             # Google Cloud Build configuration
```

## 🚀 Local Development Setup

### Prerequisites
- Python 3.14.3+
- PostgreSQL 12+
- pip and venv

### Step 1: Clone & Setup Environment

```bash
cd /Users/sramlakan/personal/GymTracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure PostgreSQL Locally

Create a local PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Run these commands in psql:
CREATE DATABASE gymtracker;
CREATE USER gymtracker_user WITH PASSWORD 'your_secure_password';
ALTER ROLE gymtracker_user SET client_encoding TO 'utf8';
ALTER ROLE gymtracker_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gymtracker_user SET default_transaction_deferrable TO on;
ALTER ROLE gymtracker_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gymtracker TO gymtracker_user;
\q
```

### Step 3: Update .env for Local Development

Edit `.env`:
```
SECRET_KEY=your-local-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

USE_CLOUD_SQL_SOCKET=False
DB_HOST=localhost
DB_PORT=5432
DB_USER=gymtracker_user
DB_PASSWORD=your_secure_password
DB_NAME=gymtracker

SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_ID=your-client-id.apps.googleusercontent.com
SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_SECRET=your-client-secret
```

### Step 4: Create Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create an admin account
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Web App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 🔐 Google OAuth Setup

### Step 1: Create OAuth Credentials in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth 2.0 Client ID**
5. Choose **Web Application**
6. Name it "GymTracker"

### Step 2: Configure Authorized Redirect URIs

Add these URIs:
- **Local Development**: `http://localhost:8000/accounts/google/login/callback/`
- **Cloud Run Production**: `https://gymtracker-XXXX.run.app/accounts/google/login/callback/`

### Step 3: Copy Credentials

Copy the **Client ID** and **Client Secret** and update `.env`:

```
SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_ID=your-client-id.apps.googleusercontent.com
SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_SECRET=your-client-secret
```

### Step 4: Configure django-allauth

django-allauth automatically picks up the credentials from environment variables. The login page at `http://localhost:8000/accounts/login/` will show the Google OAuth button.

## 🐳 Cloud Run Deployment

### Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Your GCP project ID

### Step 1: Create Cloud SQL PostgreSQL Instance

```bash
# Enable required APIs
gcloud services enable sqladmin.googleapis.com compute.googleapis.com run.googleapis.com

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create Cloud SQL PostgreSQL instance
gcloud sql instances create gymtracker-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --database-flags=cloudsql_iam_authentication=on
```

### Step 2: Create Database & User

```bash
# Create database
gcloud sql databases create gymtracker \
  --instance=gymtracker-db

# Create user
gcloud sql users create gymtracker_user \
  --instance=gymtracker-db \
  --password=your_secure_password
```

### Step 3: Prepare .env for Cloud Run

Create a secure environment configuration. You'll set these as environment variables in Cloud Run:

```
SECRET_KEY=generate-a-secure-random-key
DEBUG=False
ALLOWED_HOSTS=gymtracker-XXXX.run.app

USE_CLOUD_SQL_SOCKET=True
CLOUD_SQL_CONNECTION_NAME=YOUR_PROJECT:us-central1:gymtracker-db
DB_USER=gymtracker_user
DB_PASSWORD=your_secure_password
DB_NAME=gymtracker

SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_ID=your-client-id.apps.googleusercontent.com
SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_SECRET=your-client-secret
```

### Step 4: Deploy Using Cloud Build

```bash
gcloud builds submit --config=cloudbuild.yaml
```

This will:
1. Build the Docker image
2. Push it to Container Registry
3. Deploy to Cloud Run

### Step 5: Run Django Migrations on Cloud Run

```bash
# Get the Cloud Run service URL first
gcloud run services describe gymtracker --region=us-central1

# Create a Cloud Run job to run migrations
gcloud run jobs create migrate \
  --image=gcr.io/YOUR_PROJECT_ID/gymtracker:latest \
  --task-count=1 \
  --set-cloudsql-instances=YOUR_PROJECT:us-central1:gymtracker-db \
  --region=us-central1 \
  --command=python \
  --args=manage.py,migrate \
  --set-env-vars="DJANGO_SETTINGS_MODULE=config.settings,USE_CLOUD_SQL_SOCKET=True,CLOUD_SQL_CONNECTION_NAME=YOUR_PROJECT:us-central1:gymtracker-db,DB_USER=gymtracker_user,DB_PASSWORD=your_secure_password,DB_NAME=gymtracker"

# Execute the migration job
gcloud run jobs execute migrate --region=us-central1
```

### Step 6: Configure Cloud Run Environment Variables

```bash
gcloud run services update gymtracker \
  --set-env-vars SECRET_KEY=your-secret-key,\
DEBUG=False,\
ALLOWED_HOSTS=gymtracker-XXXX.run.app,\
USE_CLOUD_SQL_SOCKET=True,\
CLOUD_SQL_CONNECTION_NAME=YOUR_PROJECT:us-central1:gymtracker-db,\
DB_USER=gymtracker_user,\
DB_PASSWORD=your_secure_password,\
DB_NAME=gymtracker,\
SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_ID=your-client-id.apps.googleusercontent.com,\
SOCIALACCOUNT_PROVIDERS_GOOGLE_APP_SECRET=your-client-secret \
  --region=us-central1
```

### Step 7: Enable Cloud SQL Connection

```bash
gcloud run services update gymtracker \
  --add-cloudsql-instances=YOUR_PROJECT:us-central1:gymtracker-db \
  --region=us-central1
```

### Step 8: Create Cloud Run Service Account (Optional but Recommended)

```bash
gcloud iam service-accounts create gymtracker-service-account
gcloud projects add-iam-policy-binding YOUR_PROJECT \
  --member=serviceAccount:gymtracker-service-account@YOUR_PROJECT.iam.gserviceaccount.com \
  --role=roles/cloudsql.client
```

## 📝 Usage

### Logging Workouts

1. Navigate to http://localhost:8000 (or your Cloud Run URL)
2. Sign in with your Google account
3. Click "Log Workout"
4. The form automatically shows the next workout type (A or B)
5. Enter weight and reps for each set
6. Add optional notes for each lift
7. Click "Save Workout"

### Viewing History

- Click "History" to see all past workout sessions
- Each session shows all lifts and sets with their weights and reps
- Lift notes are displayed if provided

### Checking Progress

- Click "Progress" to see workouts grouped by week
- Weekly view shows workout dates and final set weight/reps for each lift
- Use this to track strength progression over time

### Admin Panel

- Visit http://localhost:8000/admin
- Log in with your superuser credentials
- Full CRUD interface for all data
- Useful for inspecting, editing, or deleting records

## 🔧 Configuration

### Model Configuration

Edit `tracker/models.py` to change set/rep defaults:

```python
SETS_PER_LIFT = 5  # Change to desired number
REPS_PER_SET = 5   # Change to desired reps
```

### Lift Names

Available lifts in the system:
- Squat
- Bench Press
- Barbell Row
- Deadlift
- Overhead Press

To add more, edit the `LIFT_NAMES` choices in `Lift` model.

## 🚨 Troubleshooting

### Local PostgreSQL Connection Issues

```bash
# Test connection
psql -h localhost -U gymtracker_user -d gymtracker
```

### Django Migration Errors

```bash
# Reset migrations (CAUTION: deletes local data)
rm tracker/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Cloud Run Deployment Issues

```bash
# View Cloud Build logs
gcloud builds log --limit=50

# View Cloud Run logs
gcloud run services describe gymtracker --region=us-central1
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gymtracker" --limit=50 --format=json
```

### Google OAuth Not Working

1. Verify Client ID and Secret are correct
2. Check `ALLOWED_HOSTS` includes your domain
3. Ensure redirect URI in Google Console matches exactly
4. Clear browser cookies and try again

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)

## 🎯 Next Steps

1. Set up local development and test the app
2. Create Google OAuth credentials
3. Deploy to Cloud Run
4. Update your Cloud Run URL in Google OAuth settings
5. Start logging your lifts!

