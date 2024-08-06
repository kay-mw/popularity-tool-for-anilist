from dagster import DefaultScheduleStatus, ScheduleDefinition

from ..jobs import daily_upload_job

daily_upload_schedule = ScheduleDefinition(
    job=daily_upload_job,
    cron_schedule="0 0 * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)
