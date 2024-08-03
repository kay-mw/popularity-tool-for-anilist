from dagster import AssetSelection, define_asset_job

upload_data = AssetSelection.assets(["upload_data"])

daily_upload_job = define_asset_job(
    name="daily_upload_job",
    selection=upload_data,
)
