# Email Automation & Reminder System

A full-stack student portfolio project for creating email campaigns, scheduling one-off or recurring reminders, personalizing messages, simulating/sending email through SMTP, and monitoring message status.

## What it does
1. Stores contacts and teams in SQLite (or imports them from CSV).
2. Uses reusable Jinja2 templates to personalize subject and body.
3. Groups a template into a campaign.
4. Schedules a reminder for one contact, either once or with an RRULE recurrence.
5. A Python worker checks due reminders and dispatches messages.
6. Records `scheduled`, `sent`, or `failed` status and errors.
7. Exposes a FastAPI REST API and a Next.js dashboard.
8. Exports a CSV activity report.

## Technology
Python 3.11+, FastAPI, SQLAlchemy, SQLite, Jinja2, smtplib, python-dateutil, logging, CSV, Next.js, React and TypeScript.

## Project layout
```text
Email-Automation-Reminder-System/
├── api/                 # FastAPI routes and validation
├── apps/web/             # Next.js dashboard
├── data/                 # Demo contacts and reminder CSVs
├── docs/                 # Architecture, plan and interview notes
├── images/               # Add your own project screenshots here
├── logs/                  # Runtime logs (not committed)
├── outputs/               # Generated CSV reports
├── src/                   # Python config, DB, models, mailer and worker logic
├── templates/              # Reusable email templates
├── tests/                  # Small automated tests
├── main.py                 # CSV import and report CLI
├── run_worker.py           # Background scheduler/dispatcher
├── requirements.txt
├── .env.example
└── README.md
```

## Setup
### Windows PowerShell
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS / Linux
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run the backend
Import the sample contacts and reminders:
```bash
python main.py --import-contacts --import-reminders
```
Start the API in terminal 1:
```bash
uvicorn api.app:app --reload
```
API documentation: http://127.0.0.1:8000/docs

Start the worker in terminal 2:
```bash
python run_worker.py
```
The worker checks for due reminders every 10 seconds.

Run one scheduler cycle manually:
```bash
python main.py --process-due-now
```
Export the report:
```bash
python main.py --export-report
```

## Run the dashboard
In terminal 3:
```bash
cd apps/web
npm install
npm run dev
```
Open http://localhost:3000. The dashboard connects to `http://localhost:8000` by default. To use another API URL, create `apps/web/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`.

The dashboard lets you add a contact, create a template, create a campaign, schedule a personal reminder, schedule a reminder for every subscribed member of a team, and view reminder/message activity. The API can also be used directly through `/docs`. Team reminders use `POST /team-reminders`.

## Email safety
`DRY_RUN=true` is the default. In dry-run mode, the application records a successful simulated send but does not contact an SMTP server. This is the recommended mode for screenshots and GitHub.

For real SMTP sending, edit your local `.env`:
```env
DRY_RUN=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_16_character_google_app_password
SMTP_FROM_NAME=Email Automation Demo
```
Use a Google App Password where available, not your normal Google password. Only test with your own address or recipients who have explicitly agreed to receive the email. Never commit `.env`, passwords, real contact details or private logs.

## Recurrence examples
- Daily: `FREQ=DAILY`
- Weekly: `FREQ=WEEKLY`
- Every Monday: `FREQ=WEEKLY;BYDAY=MO`
- Monthly: `FREQ=MONTHLY`

The reminder `scheduled_at` value must include a timezone. The dashboard converts its local date/time selection to an ISO timestamp.

## Tests
```bash
pytest
```

## Reports and status meaning
- `logs/app.log`: worker and application logs
- `outputs/email_report.csv`: exported message report
- `scheduled`: due time has not been processed yet
- `sent`: SMTP server accepted the message (or dry-run simulation succeeded)
- `failed`: sender returned an error

SMTP acceptance does **not** confirm inbox delivery. True delivery, bounce, open and click events need a mail provider that exposes delivery webhooks and tracking APIs.

## Production improvements
This is an educational local project, not a production-ready bulk mail platform. A production deployment should add authentication and authorization, unsubscribe and consent management, rate limiting, retry/backoff, a durable queue, provider webhooks, monitoring, database migrations, audit logs, and stronger timezone/recurrence test coverage.

## Screenshots to add
Save your own screenshots under `images/`: project tree, CSV sample, API docs, dashboard forms, worker dry-run output, status table and exported CSV report.

## Learning outcomes
Python modules, CSV processing, SMTP, email templates, scheduling, recurring rules, error handling, logging, environment variables, REST APIs, SQLAlchemy, relational data modelling, React/Next.js, testing and Git/GitHub.
