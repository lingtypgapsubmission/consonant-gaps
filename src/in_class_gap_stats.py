import json
import pandas as pd

with open('../json/stop_gaps_postprocessed.json', 'r', encoding='utf-8') as inp:
    stop_gaps_dict = json.load(inp)
stop_gaps_counts = [(k, len(v)) for k,v in stop_gaps_dict.items()]
stop_gaps_df = pd.DataFrame.from_records(
    stop_gaps_counts,
    columns=['gap', 'count'])
stop_gaps_df.sort_values(by='count', inplace=True, ascending=False)

stop_gaps_df.to_csv('../csv/stop_gaps_ranking.csv', index=False)