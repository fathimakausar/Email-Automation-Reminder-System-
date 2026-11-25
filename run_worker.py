import time, logging
from src.database import Base, engine, SessionLocal
from src.service import plan_due, dispatch_due
from src.logging_config import setup_logging

def main():
    setup_logging()
    Base.metadata.create_all(engine)
    logging.info("Worker started; checking due reminders every 10 seconds.")
    while True:
        with SessionLocal() as db:
            created = plan_due(db)
            sent = dispatch_due(db)
            if created or sent: logging.info("Created=%s Processed=%s", created, sent)
        time.sleep(10)

if __name__ == "__main__": main()
