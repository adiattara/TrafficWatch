from .ingestion import  near_real_time_data_ingestion

from dagster import Definitions, ScheduleDefinition

defs = Definitions(

    schedules=[
        ScheduleDefinition(
            job =near_real_time_data_ingestion,
            cron_schedule="* * * * *",
            execution_timezone="Europe/Paris"
        )
    ],
    jobs=[near_real_time_data_ingestion]

)

