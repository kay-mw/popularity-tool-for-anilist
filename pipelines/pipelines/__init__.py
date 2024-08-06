from dagster import Definitions

from pipelines.assets import upload_data
from pipelines.jobs import daily_upload_job
from pipelines.schedules import daily_upload_schedule

defs = Definitions(
    assets=[upload_data], jobs=[daily_upload_job], schedules=[daily_upload_schedule]
)
