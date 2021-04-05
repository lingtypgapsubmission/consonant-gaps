import json
import sys
import query_lib as ql

def check_gaps(input_path, feature1='place', feature2='manner'):
    with open(
        input_path, 
        'r', 
        encoding='utf-8'
    ) as inp:
        gap_fillers = json.load(inp)

    for k, x in gap_fillers.items():
        if x is None:
            continue
        a, b, c = k[1:-1].split()
        quadruple = a, b, c, x
        # print(quadruple)
        if not len(ql.oppositions(quadruple, feature1)) == 2 and \
            len(ql.oppositions(quadruple, feature2)) == 2:
            print(quadruple)
            print('Error!')
            sys.exit(1)
    print('Passed.')


if __name__ == "__main__":
    fn1 = '../json/fricative_affricate_direct_gaps_voiced_fillers.json'
    fn2 = '../json/fricative_affricate_direct_gaps_voiceless_fillers.json'
    fn3 = '../json/fricative_affricate_inverse_gaps_voiced_fillers.json'
    fn4 = '../json/fricative_affricate_inverse_gaps_voiceless_fillers.json'
    for fn in [fn1, fn2, fn3, fn4]:
        print(fn)
        check_gaps(fn)