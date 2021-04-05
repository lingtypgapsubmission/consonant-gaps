import pandas as pd

d = pd.read_excel('../csv/sound_changes.xlsx')
d_source = d.groupby(['Source']).size()
d_reflex = d.groupby(['Reflex']).size()
ratios = {}
for segment in d_reflex.index:
    if segment in d_source.index and d_source[segment] + d_reflex[segment] >= 10:
        ratios[segment] = d_reflex[segment] / d_source[segment]
stops = 'g p d b ɟ c k'.split()
for s in stops:
    print(f'/{s}/: {ratios[s]:.3}', end=', ')
print('\b\b ')
fricatives = 'ɦ   ʒ   z   v   ɣ   x  f   ʁ  ʝ'.split()
for f in fricatives:
    print(f'/{f}/: {ratios[s]:.3}', end=', ')
print('\b\b ')