from .script import topstory_ids_assets,topstory_ids

from dagster import Definitions, ScheduleDefinition

defs = Definitions(

    schedules=[

        ScheduleDefinition(
            job =topstory_ids,
            cron_schedule="2 * * * 1-5",
            execution_timezone="Europe/Paris"
        ),
    ],
    assets=[topstory_ids_assets]

)

