import json
import sys
import pandas as pd

in_path = sys.argv[1]
out_path = sys.argv[2]

with open(in_path, 'r', encoding='utf-8') as inp:
    gltc_dict = json.load(inp)
records = []
for key, gltcs in gltc_dict.items():
    if key == 'null':
        continue
    records.append((key, len(gltcs)))
df = pd.DataFrame.from_records(records, columns=['Phoneme', 'Count'])
df.sort_values(by='Count', inplace=True, ascending=False)
df.to_csv(out_path, index=False)