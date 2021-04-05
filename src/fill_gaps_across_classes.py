import json
import pandas as pd
import query_lib as ql


def similar_places(p1, p2):
    fd = ql.feature_difference(p1, p2)
    if len(fd) == 1 and 'place' in fd and sorted(
        [fd['place']['p1'], fd['place']['p2']]
    ) in [
        ['alveolar', 'dental'],
        ['bilabial', 'labio-dental']
    ]:
        return True
    else:
        return False


def different(a, b, c, x):
    """
    Checks if the phoneme x is not too close
    to a, b, c to constitute a meaningful opposition.
    """
    if x in (a, b, c):
        return False
    if ql.feature_difference(a, x) == {} or ql.feature_difference(b, x) == {} or ql.feature_difference(c, x) == {}:
        return False
    if similar_places(a, x) or similar_places(b, x) or similar_places(c, x):
        return False
    return True


def fill_gaps(
        input_path,
        output_path,
        manner, 
        voice, 
        feature1 = 'place', 
        feature2 = 'manner'):
    print(input_path)
    with open(input_path, 'r', encoding='utf-8') as inp:
        gaps = json.load(inp)
    reference_segments = ql.get_manners(segments, [manner])
    reference_segments = ql.get_voices(reference_segments, [voice])

    result = {}
    for key in gaps:
        a, b, c = key[1:-1].split()
        for d in filter(lambda x: different(a, b, c, x), reference_segments):
            quadruple = a, b, c, d
            opps_list_voice = list(ql.oppositions(quadruple, feature1))
            opps_list_place = list(ql.oppositions(quadruple, feature2))
            if len(opps_list_voice) == 2 and len(opps_list_place) == 2:
                print(f'{key} -> {d}')
                result[key] = d
                break
        else:
            print(f'{key} cannot be filled.')
            result[key] = None
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(result, out, indent=2, ensure_ascii=False)


# With direct gaps in stops->fricatives, we need fricatives to fill gaps, 
# with inverse gaps in stops->fricatives, we need stops, &c.
if __name__ == '__main__':
    d = pd.read_csv('../csv/phoible_working_sample.csv', low_memory=False)
    segments = list(d.Phoneme.unique())
    fill_gaps(
        '../json/fricative_affricate_direct_gaps_voiced.json',
        '../json/fricative_affricate_direct_gaps_voiced_fillers.json',
        'affricate',
        'voiced'
    )
    fill_gaps(
        '../json/fricative_affricate_direct_gaps_voiceless.json',
        '../json/fricative_affricate_direct_gaps_voiceless_fillers.json',
        'affricate',
        'voiceless'
    )
    fill_gaps(
        '../json/fricative_affricate_inverse_gaps_voiced.json',
        '../json/fricative_affricate_inverse_gaps_voiced_fillers.json',
        'fricative',
        'voiced'
    )
    fill_gaps(
        '../json/fricative_affricate_inverse_gaps_voiceless.json',
        '../json/fricative_affricate_inverse_gaps_voiceless_fillers.json',
        'fricative',
        'voiceless'
    )
    