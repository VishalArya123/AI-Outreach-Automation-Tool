from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()
scheduler.start()

# In-memory store for job statuses keyed by job_id
job_statuses = {}

def update_job_status(job_id, status):
    if job_id in job_statuses:
        job_statuses[job_id]['status'] = status

def get_all_jobs():
    return job_statuses

def cancel_campaign(campaign_id):
    """
    Cancels all scheduled jobs for the specified campaign and removes their status entries.
    Returns the count of removed jobs.
    """
    to_remove = []
    for job_id, info in list(job_statuses.items()):
        if info.get('campaign_id') == campaign_id:
            try:
                scheduler.remove_job(job_id)
            except Exception:
                # Job might already be executed or removed
                pass
            to_remove.append(job_id)
    for job_id in to_remove:
        job_statuses.pop(job_id, None)
    return len(to_remove)

def schedule_batch_emails(send_func, start_datetime, end_datetime, total_emails, campaign_id, **kwargs):
    """
    Schedule emails evenly spaced between start_datetime and end_datetime, associating all emails
    with a campaign_id for tracking and cancellation.
    """
    interval_seconds = (end_datetime - start_datetime).total_seconds() / max(1, total_emails - 1)
    for i in range(total_emails):
        send_time = start_datetime + timedelta(seconds=i * interval_seconds)
        job_id = f"email_{send_time.timestamp()}_{campaign_id}_{i}"

        def job_wrapper(job_id=job_id, send_func=send_func, campaign_id=campaign_id, **kwargs):
            update_job_status(job_id, "sending")
            status, res = send_func(**kwargs)
            if status == 200:
                update_job_status(job_id, "sent ✅")
            else:
                update_job_status(job_id, "failed ❌")

            # Cleanup statuses when all jobs in the campaign are done
            campaign_jobs = [j for j, info in job_statuses.items() if info.get('campaign_id') == campaign_id]
            if all(job_statuses[j]['status'] in ['sent ✅', 'failed ❌'] for j in campaign_jobs):
                for j in campaign_jobs:
                    job_statuses.pop(j, None)

        kwargs_copy = kwargs.copy()
        job_statuses[job_id] = {
            "status": "scheduled",
            "send_time": send_time,
            "recipient": kwargs.get("recipient", "N/A"),
            "campaign_id": campaign_id
        }

        scheduler.add_job(
            job_wrapper,
            'date',
            run_date=send_time,
            id=job_id,
            kwargs=kwargs_copy,
            misfire_grace_time=300
        )
    return True
