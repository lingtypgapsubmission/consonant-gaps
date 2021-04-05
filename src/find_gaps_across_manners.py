"""
find_gaps.py finds gaps (asymmetries in voicing) inside stops, fricatives, and affricates.
This script aims at finding hierarchy reversals: it is expected to have fricatives at fewer
places of articulation than stops, and affricates at fewer places of articulation than
fricatives:

scipy.stats.describe(places['stops'])
Out[16]: DescribeResult(nobs=1694, minmax=(2, 8), mean=4.528925619834711, variance=0.9084953600874774, skewness=0.25705603227104074, kurtosis=-0.22411875080779442)
scipy.stats.describe(places['fricatives'])
Out[17]: DescribeResult(nobs=1694, minmax=(0, 8), mean=3.34297520661157, variance=2.2148443029879963, skewness=0.31448519634361677, kurtosis=0.07079096495351633)
scipy.stats.describe(places['affricates'])
Out[18]: DescribeResult(nobs=1694, minmax=(0, 5), mean=1.0348288075560803, variance=0.7826019494118082, skewness=0.7155790007792195, kurtosis=0.41654481205273886) 

Therefore, it is of interest to find fricatives lacking corresponding stops and affricates lacking
corresponding fricatives. We fix voice and group stops with fricatives or fricatives with affricates.
When looking for 'direct' gaps (fricatives/affricates are missing) we take triples with two elements
of the 'lower' class; when looking for 'inverse' gaps, we take triples with two elements of the
'higher' class.
"""

import json
from itertools import combinations
from collections import defaultdict
from typing import Tuple, List, Dict
import pandas as pd
import query_lib as ql
from IPAParser_2_0 import parse_consonant


def enumerate_triples(data_frame: pd.DataFrame, manners: Tuple[str, str], voice: str, direction: str) -> Dict[str, List[str]]:
    """
    @manners must have exactly two elements
    @direction can be either 'direct' or 'inverse'
    When @direction is 'direct', we take triples with two elements having the first manner.
    When @direction is 'inverse', we take triples with two elements having the second manner.
    """
    if direction not in {'direct', 'inverse'}:
        raise ValueError(f'Wrong direction: {direction}')
    result = defaultdict(list)
    for gltc in data_frame.Glottocode.unique():
        segments = ql.get_manners(
            ql.get_voices(ql.get_inventory(data_frame, gltc), [voice]), 
            manners)
        manner1, manner2 = manners
        for triple in combinations(segments, 3):
            manner1_count = 0
            manner2_count = 0
            for el in triple:
                parse = parse_consonant(el)
                if parse['manner'] == manner1:
                    manner1_count += 1
                elif parse['manner'] == manner2:
                    manner2_count += 1
            if direction == 'direct' and manner1_count != 2:
                continue
            elif direction == 'inverse' and manner2_count != 2:
                continue
            if len(ql.oppositions(triple, 'place')) == 1 and len(ql.oppositions(triple, 'manner')) == 1:
                a, b, c = triple
                plug_found = False
                for d in filter(lambda x: x not in triple, segments):
                    quadruple = a, b, c, d
                    if len(ql.oppositions(quadruple, 'place')) == 2 and len(ql.oppositions(quadruple, 'manner')) == 2:
                        plug_found = True
                        break
                if not plug_found:
                    result[f'/{" ".join(triple)}/'].append(gltc)
    return result

if __name__ == '__main__':
    data = pd.read_csv('../csv/phoible_working_sample.csv', low_memory=False)
    with open('../json/fricative_affricate_direct_gaps_voiceless.json', 'w', encoding='utf-8') as out:
        json.dump(
            enumerate_triples(data, ['fricative', 'affricate'], 'voiceless', 'direct'),
            out,
            ensure_ascii=False,
            indent=2
        )
    with open('../json/fricative_affricate_inverse_gaps_voiceless.json', 'w', encoding='utf-8') as out:
        json.dump(
            enumerate_triples(data, ['fricative', 'affricate'], 'voiceless', 'inverse'),
            out,
            ensure_ascii=False,
            indent=2
        )
    with open('../json/fricative_affricate_direct_gaps_voiced.json', 'w', encoding='utf-8') as out:
        json.dump(
            enumerate_triples(data, ['fricative', 'affricate'], 'voiced', 'direct'),
            out,
            ensure_ascii=False,
            indent=2
        )
    with open('../json/fricative_affricate_inverse_gaps_voiced.json', 'w', encoding='utf-8') as out:
        json.dump(
            enumerate_triples(data, ['fricative', 'affricate'], 'voiced', 'inverse'),
            out,
            ensure_ascii=False,
            indent=2
        )