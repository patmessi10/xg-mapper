# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 23:19:36 2023

@author: patmf
"""
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os

'''
1. Read in competitions
2. Iterate through each competitions
3. Check if gender is female, if so store competition in list
'''


def find_womens_comp_ids():
    filename = "C:/data/Statsbomb/data/competitions.json"
    print(f"find all women's comp ids: filename={filename}")
    with open(filename, encoding="utf8") as f:
        competitions = json.load(f)

    womens_comp_ids = set()

    for competition in competitions:
        if competition["competition_gender"] == "female":
            womens_comp_ids.add(competition["competition_id"])

    return womens_comp_ids


def find_match_ids(comp_ids):
    print(f"finding all match ids: comp_ids={comp_ids}")
    match_ids = []

    for comp_id in comp_ids:
        filenames = os.listdir(f"C:/data/Statsbomb/data/matches/{comp_id}")
        for filename in filenames:
            print(f"loading match ids: comp_id={comp_id}, filename={filename}")
            with open(f"C:/data/Statsbomb/data/matches/{comp_id}/{filename}", encoding="utf8") as f:
                matches = json.load(f)
            for match in matches:
                match_ids.append(match["match_id"])

    print(f"finished finding match ids: match_ids={match_ids}")
    return match_ids


def read_events_data(match_ids) -> pd.DataFrame:
    all_dfs = []
    for i, match_id in enumerate(match_ids):
        filename = f"C:/data/Statsbomb/data/events/{match_id}.json"
        print(f"reading data ({i / len(match_ids) * 100:.2f}%): match_id={match_id}, filename={filename}")
        df = pd.read_json(filename, encoding="utf8")
        # TODO Filter by Shot Type
        all_dfs.append(df)

    events_df = pd.concat(all_dfs, ignore_index=True)
    print(f"finished reading event data: num_rows={events_df.shape[0]}")

    # Pulls out event name from type column into its own column for later filtering
    events_df["event_name"] = events_df["type"].apply(lambda x: x["name"])

    return events_df


# def main():
womens_comp_ids = find_womens_comp_ids()
match_ids = find_match_ids(womens_comp_ids)

events_df = read_events_data(match_ids[0:50])

shots_df = events_df[events_df["event_name"] == "Shot"]
events_df.query("event_name == 'Shot'")



# if __name__ == "__main__":
#     main()