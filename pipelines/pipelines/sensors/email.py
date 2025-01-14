import os

from dagster import DefaultSensorStatus, make_email_on_run_failure_sensor

email_on_run_failure = make_email_on_run_failure_sensor(
    email_from=os.environ["SENDER_EMAIL"],
    email_password=os.environ["APP_PASSWORD"],
    email_to=[os.environ["RECEIVER_EMAIL"]],
    default_status=DefaultSensorStatus.RUNNING,
)
