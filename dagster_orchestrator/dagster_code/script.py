import json
import os
from dagster import asset, define_asset_job, AssetSelection  # import the `dagster` library
import requests



topstory_ids = define_asset_job(name="topstory_ids",selection=AssetSelection.groups("topstory_ids"))
@asset(group_name="topstory_ids") # add the asset decorator to tell Dagster this is an asset
def topstory_ids_assets() -> None:
    newstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_new_story_ids = requests.get(newstories_url).json()[:100]

    os.makedirs("data", exist_ok=True)
    with open("data/topstory_ids.json", "w") as f:
        json.dump(top_new_story_ids, f)