from collections import Counter, defaultdict
import numpy as np
import pandas as pd
import scipy.stats
import query_lib as ql

np.random.seed(42)
d = pd.read_csv('phoible_working_sample.csv')

# Sample size
print('Sample size: ', end='')
print(len(set(d.Glottocode.unique())))

stops_fricatives = []
fricatives_affricates = []

# Statistics for different places of articulation
places = defaultdict(list)
for gltc in d.Glottocode.unique():
    segments = ql.get_inventory(d, gltc)
    stops = ql.get_manners(segments, ['stop'])
    fricatives = ql.get_manners(segments, ['fricative'])
    affricates = ql.get_manners(segments, ['affricate'])
    stops_places = ql.count_places(stops)
    fricatives_places = ql.count_places(fricatives)
    affricates_places  = ql.count_places(affricates)
    places['stops'].append(stops_places)
    places['fricatives'].append(fricatives_places)
    places['affricates'].append(affricates_places)
    stops_fricatives.append(stops_places-fricatives_places)
    fricatives_affricates.append(fricatives_places-affricates_places)
print('Stops:')
print(scipy.stats.describe(places['stops']))
print('Fricatives:')
print(scipy.stats.describe(places['fricatives']))
print('Affricates:')
print(scipy.stats.describe(places['affricates']))
stops_fricatives_boot = [
    np.mean(np.random.choice(stops_fricatives, size=len(stops_fricatives)))
    for i in range(10000)
]
fricatives_affricates_boot = [
    np.mean(np.random.choice(fricatives_affricates, size=len(fricatives_affricates)))
    for i in range(10000)
]
print('Stops minus fricatives bootstrap:')
print(scipy.stats.mstats.mquantiles(stops_fricatives_boot, prob=[0.025, 0.975]))
print('Fricatives minus affricates bootstrap:')
print(scipy.stats.mstats.mquantiles(fricatives_affricates_boot, prob=[0.025, 0.975]))

# Phylum and macro-area breakdown
language_meta = pd.read_csv('phoible-v2.0.1/cldf-datasets-phoible-f36deac/cldf/languages.csv')
data_dict = {
    t.Glottocode: {
        'macroarea': str(t.Macroarea),
        'phylum': str(t.Family_Name)
    } for t in language_meta.itertuples()
}
macro_areas = Counter()
phyla = Counter()
for gltc in d.Glottocode.unique():
    if gltc == 'sout2965':
        macro_areas['North America'] += 1
        phyla['Salishan'] += 1
        continue
    elif gltc == 'begb1241':
        macro_areas['Africa'] += 1
        phyla['Atlantic-Congo'] += 1
        continue
    elif gltc == 'lule1238':
        macro_areas['South America'] += 1
        phyla['Isolate'] += 1
        continue
    elif gltc == 'wich1264':
        macro_areas['South America'] += 1
        phyla['Matacoan'] += 1
        continue
    elif gltc == 'shan1283':
        macro_areas['South America'] += 1
        phyla['Pano-Tacanan'] += 1
        continue
    elif gltc == 'yaro1235':
        macro_areas['South America'] += 1
        phyla['Yanomamic'] += 1
        continue
    elif gltc == 'chal1275':
        macro_areas['Eurasia'] += 1
        phyla['Afro-Asiatic'] += 1
        continue
    elif gltc == 'pand1265':
        gltc = 'madi1260'
    try:
        macro_areas[data_dict[gltc]['macroarea']] += 1
        phyla[data_dict[gltc]['phylum']] += 1
    except KeyError:
        print(f'Missing: {gltc}')

for area, count in sorted(macro_areas.items()):
    print(f'{area},{count}')
print()
for phylum, count in sorted(phyla.items()):
    print(f'{phylum},{count}')