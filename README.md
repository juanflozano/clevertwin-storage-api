# CleverTwin Storage API

Backend API for managing storage events across companies, built with FastAPI, PostgreSQL, and deployed on AWS.

## Architecture
Frontend (S3 + CloudFront)
↓
API Gateway
↓
Lambda (FastAPI + Mangum)
↓
RDS PostgreSQL

## Project Structure
├── backend/          # FastAPI application
│   ├── routers/      # API endpoints
│   ├── main.py       # App entry point
│   ├── database.py   # DB connection
│   ├── models.py     # DB tables
│   ├── schemas.py    # Request validation
│   └── auth.py       # JWT authentication
├── frontend/         # HTML/CSS/JS client
├── scripts/          # Build scripts
└── .github/          # CI/CD workflows

## Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** PostgreSQL (AWS RDS)
- **Auth:** JWT
- **Infrastructure:** AWS Lambda, API Gateway, S3, CloudFront
- **CI/CD:** GitHub Actions

## Local Development

```bash
cd backend
py -m uvicorn main:app --reload
```

## Environment Variables
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=

## Deployment

Push to `main` branch triggers automatic deployment via GitHub Actions.