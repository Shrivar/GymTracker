# GymTracker

A simple web application to track your StrongLifts 5x5 strength training workouts.

## Features

- 🏋️ Log workouts with alternating A/B workout types
- 📊 Track weight and reps for each set
- 📝 Add notes to individual lifts
- 📈 View workout history and weekly progress
- 🔐 Secure login with Google authentication
- ☁️ Cloud-native deployment on Google Cloud Run

## Tech Stack

- **Backend**: Django 5.1
- **Database**: PostgreSQL (Cloud SQL)
- **Hosting**: Google Cloud Run
- **Authentication**: Google OAuth via django-allauth

## Local Development

### Prerequisites
- Python 3.14.3+
- PostgreSQL
- pip/venv

### Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd GymTracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update `.env` with your database credentials and Google OAuth credentials.

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` and sign in with your Google account.

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new OAuth 2.0 credential (Web Application)
3. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/` (local)
   - `https://your-cloud-run-url.run.app/accounts/google/login/callback/` (production)
4. Copy the Client ID and Client Secret
5. Add them to your `.env` file

## Cloud SQL Setup

1. Create a Cloud SQL PostgreSQL instance
2. Create a database named `gymtracker`
3. Add a user with password
4. Enable Cloud SQL Admin API
5. Set environment variables for Cloud Run

## Deployment to Cloud Run

1. Enable required GCP APIs:
```bash
gcloud services enable run.googleapis.com sqladmin.googleapis.com
```

2. Set your project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

3. Deploy using Cloud Build:
```bash
gcloud builds submit --config=cloudbuild.yaml
```

4. Configure environment variables in Cloud Run:
   - Set `ALLOWED_HOSTS` to your Cloud Run URL
   - Set database connection variables
   - Set `SECRET_KEY` to a secure random value
   - Set Google OAuth credentials

5. Set Cloud SQL connection:
```bash
gcloud run services update gymtracker \
  --add-cloudsql-instances PROJECT:REGION:INSTANCE \
  --region us-central1
```

6. Run migrations on Cloud Run instance:
```bash
gcloud run jobs create migrate --image gcr.io/PROJECT_ID/gymtracker --task-count 1 --set-env-vars DJANGO_SETTINGS_MODULE=config.settings -- python manage.py migrate
```

## Workout Structure

### Workout A
- Squat
- Bench Press
- Barbell Row

### Workout B
- Squat
- Deadlift
- Overhead Press

Each lift consists of 5 sets of 5 reps (configurable via `SETS_PER_LIFT` and `REPS_PER_SET` in `tracker/models.py`).

## Usage

1. **Log a Workout**: Click "Log Workout" to record today's session
2. **View History**: See all past workouts with detailed set information
3. **Check Progress**: Review weekly summaries to track improvements
4. **Admin Panel**: Access `/admin` to inspect/edit data directly

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT

