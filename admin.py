# admin.py
import db_operations as db_ops
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def scheduled_report_job():
    report_id = db_ops.generate_report()
    # Handle the report (e.g., saving, emailing, etc.)

scheduler.add_job(scheduled_report_job, 'interval', hours=24)
scheduler.start()

# Any other initialization and main routine as needed
