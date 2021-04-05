import json
import sys
from collections import defaultdict

gap_file_name = sys.argv[1]
filler_file_name = sys.argv[2]
postprocessed_file_name = sys.argv[3]

with open(gap_file_name, 'r', encoding='utf-8') as inp:
    gap_dict = json.load(inp)
with open(filler_file_name, 'r', encoding='utf-8') as inp:
    filler_dict = json.load(inp)

result = defaultdict(set)
for gap_triple, lang_list in gap_dict.items():
    gap_filler = filler_dict[gap_triple]
    for glottocode in lang_list:
        result[gap_filler].add(glottocode)

result = { k: sorted(v) for k, v in result.items() }
with open(postprocessed_file_name, 'w', encoding='utf-8') as out:
    json.dump(result, out, indent=2, ensure_ascii=False)
