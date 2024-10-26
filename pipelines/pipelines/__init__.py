from dagster import Definitions

from pipelines.assets import upload_data
from pipelines.jobs import daily_upload_job
from pipelines.schedules import daily_upload_schedule
from pipelines.sensors.email import email_on_run_failure

defs = Definitions(
    assets=[upload_data],
    jobs=[daily_upload_job],
    schedules=[daily_upload_schedule],
    sensors=[email_on_run_failure],
)
