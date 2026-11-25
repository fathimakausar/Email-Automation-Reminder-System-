import argparse, csv
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import select
from src.database import Base, engine, SessionLocal
from src.models import Contact, Template, Campaign, Reminder, Message
from src.service import plan_due, dispatch_due
from src.logging_config import setup_logging

def import_contacts():
    with SessionLocal() as db, open("data/contacts.csv", newline="", encoding="utf-8") as f:
        added = 0
        for row in csv.DictReader(f):
            if not db.scalar(select(Contact).where(Contact.email == row["email"])):
                db.add(Contact(name=row["name"], email=row["email"], team=row.get("team") or "General",
                               timezone=row.get("timezone") or "Asia/Kolkata")); added += 1
        db.commit()
    print(f"Imported {added} contact(s).")

def import_reminders():
    with SessionLocal() as db, open("data/reminders.csv", newline="", encoding="utf-8") as f:
        added = 0
        for row in csv.DictReader(f):
            contact = db.scalar(select(Contact).where(Contact.email == row["email"]))
            if not contact:
                print(f"Skipped unknown contact: {row['email']}"); continue
            scheduled = datetime.fromisoformat(row["scheduled_at"])
            if scheduled.tzinfo is None:
                print(f"Skipped timezone-naive reminder: {row['title']}"); continue
            template = Template(name=f"CSV-{row['title']}", subject=row["subject"], body=row["body"])
            db.add(template); db.flush()
            campaign = Campaign(name=f"CSV-{row['title']}", template_id=template.id,
                                sender_name="Demo Team", sender_email="demo@example.com")
            db.add(campaign); db.flush()
            db.add(Reminder(title=row["title"], contact_id=contact.id, campaign_id=campaign.id,
                            scheduled_at=scheduled, recurrence=row.get("recurrence") or None))
            added += 1
        db.commit()
    print(f"Imported {added} reminder(s).")

def export_report():
    Path("outputs").mkdir(exist_ok=True)
    with SessionLocal() as db, open("outputs/email_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id","recipient","subject","scheduled_at","sent_at","status","error"])
        for m in db.scalars(select(Message).order_by(Message.id)):
            w.writerow([m.id,m.contact_email,m.subject,m.scheduled_at,m.sent_at,m.status,m.error or ""])
    print("Report: outputs/email_report.csv")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--import-contacts", action="store_true")
    p.add_argument("--import-reminders", action="store_true")
    p.add_argument("--process-due-now", action="store_true")
    p.add_argument("--export-report", action="store_true")
    a = p.parse_args(); setup_logging(); Base.metadata.create_all(engine)
    if a.import_contacts: import_contacts()
    if a.import_reminders: import_reminders()
    if a.process_due_now:
        with SessionLocal() as db:
            print("Planned:", plan_due(db, datetime.now(timezone.utc)))
            print("Processed:", dispatch_due(db, datetime.now(timezone.utc)))
    if a.export_report: export_report()
    if not any(vars(a).values()): p.print_help()

if __name__ == "__main__": main()
