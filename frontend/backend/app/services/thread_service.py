from app.database.connection import SessionLocal
from app.database.models import Prospect, Thread


def create_prospect(name, email, status="NEW"):
    db = SessionLocal()
    prospect = Prospect(name=name, email=email, status=status)
    db.add(prospect)
    db.commit()
    db.refresh(prospect)
    db.close()
    return prospect


def list_prospects():
    db = SessionLocal()
    prospects = db.query(Prospect).all()
    db.close()
    return prospects


def get_prospect(prospect_id):
    db = SessionLocal()
    prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    db.close()
    return prospect


def create_thread(prospect_id, budget_ceiling, current_state="NEW", scheduled_time=None):
    db = SessionLocal()
    thread = Thread(
        prospect_id=prospect_id,
        current_state=current_state,
        budget_ceiling=budget_ceiling,
        scheduled_time=scheduled_time,
    )
    db.add(thread)
    db.commit()
    db.refresh(thread)
    db.close()
    return thread


def list_threads():
    db = SessionLocal()
    threads = db.query(Thread).all()
    db.close()
    return threads


def get_thread(thread_id):
    db = SessionLocal()
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    db.close()
    return thread


def update_thread(thread_id, current_state=None, budget_ceiling=None, scheduled_time=None):
    db = SessionLocal()
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        db.close()
        return None
    if current_state is not None:
        thread.current_state = current_state
    if budget_ceiling is not None:
        thread.budget_ceiling = budget_ceiling
    if scheduled_time is not None:
        thread.scheduled_time = scheduled_time
    db.commit()
    db.refresh(thread)
    db.close()
    return thread
