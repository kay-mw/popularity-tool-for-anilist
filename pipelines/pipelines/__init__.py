from dagster import Definitions, load_assets_from_modules

import pipelines.assets as assets
from pipelines.jobs import daily_upload_job
from pipelines.schedules import daily_upload_schedule

upload_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=[*upload_assets], jobs=[daily_upload_job], schedules=[daily_upload_schedule]
)
