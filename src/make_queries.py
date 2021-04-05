import pandas as pd
from query_lib import *


if __name__ == '__main__':
    from collections import defaultdict

    contributors = pd.read_csv('phoible-v2.0.1/cldf-datasets-phoible-f36deac/cldf/contributions.csv')
    name_and_source = {}
    for t in contributors.itertuples():
        name_and_source[t.ID] = (t.Name, t.Contributor_ID)

    d = pd.read_csv('phoible.csv')
    d = d.loc[d.SegmentClass == 'consonant']
    sample = one_inventory_per_glottocode(d)

    # Check that all consonants can be parsed.
    parsable_sample = set()
    for inv_id in sample:
        inventory = list(d.loc[ d.InventoryID == inv_id ].Phoneme)
        if all_segments_parsable(inventory):
            parsable_sample.add(inv_id)
    print(f'Sample size: {len(parsable_sample)}')
    d = d.loc[d.apply(lambda row: row.InventoryID in parsable_sample, axis=1)]

    for gltc in d.Glottocode.unique():
        inv_id = list(d.loc[ d.Glottocode == gltc ].InventoryID)[0]
        inv  = get_inventory(d, gltc)
        if not voice_opp_in(inv, ['stop']):
            continue
        opps = voice_opp_in(inv, ['affricate'])
        if opps:
            fricatives = get_manners(inv, ['fricative'])
            affricates = get_manners(inv, ['affricate'])
            voiced_affricates = list(filter(
                lambda x: parse_consonant(x)['voice'] == 'voiced',
                affricates))
            voiceless_affricates = list(filter(
                lambda x: parse_consonant(x)['voice'] == 'voiceless',
                affricates))
            # Check for voiced affricates that have paired
            # voiceless affricates and voiceless fricatives
            # but do not have paired voiced fricatives.
            result = []
            for affr_vcd in voiced_affricates:
                if oppositions([affr_vcd] + fricatives, 'manner'):
                    continue
                # Find the corresponding voiceless affricate.
                opps_tmp = oppositions([affr_vcd] + voiceless_affricates, 'voice')
                if opps_tmp:
                    for _, affr_vcl in opps_tmp:
                        # Does this voiceless affricate has a paired fricative?
                        if oppositions([affr_vcl] + fricatives, 'manner'):
                            result.append(affr_vcd)
            if result:
                remainder = list(filter(lambda x: x not in result, voiced_affricates))
                print(gltc, name_and_source[inv_id][0], name_and_source[inv_id][1])
                print('Fricatives:', ', '.join(fricatives))
                print('Affricates:', ', '.join(affricates))
                print('Result:', ', '.join(result))
                print(f'Remainder: {", ".join(remainder)}')
                print()
