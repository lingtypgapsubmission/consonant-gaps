# Find inventories with one voiced stop

from collections import Counter
import pandas as pd
import query_lib as ql
from IPAParser_2_0 import parse_consonant

d = pd.read_csv('../csv/phoible_working_sample.csv', low_memory=False)
voiced_stops = Counter()
voiced_stops_single = Counter()
voiced_stop_combs = Counter()
for gltc in d.Glottocode.unique():
    inv = ql.get_inventory(d, gltc)
    tmp = 0
    tmp_stops = []
    has_implosives = False
    for p in inv:
        parse = parse_consonant(p)
        if parse.get('voice', '') == 'voiced' and \
                parse.get('manner', '') == 'stop' and \
                parse['nasal'] == False and \
                parse['place'] == 'bilabial':
            tmp_stops.append(p)
            tmp += 1
            if parse.get('implosive', False) == True:
                has_implosives = True
    if not has_implosives:
        continue
    voiced_stops[tmp] += 1
    if tmp == 1:
        voiced_stops_single[tmp_stops[0]] += 1
    else:
        voiced_stop_combs[tuple(sorted(tmp_stops))] += 1
print(sorted(voiced_stops.items()))
print(sorted(voiced_stops_single.items(), key=lambda x: x[1], reverse=True))
print(sorted(voiced_stop_combs.items(), key=lambda x: x[1], reverse=True))
