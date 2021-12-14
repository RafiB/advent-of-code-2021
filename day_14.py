from collections import defaultdict


TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


PUZZLE_INPUT = """VHCKBFOVCHHKOHBPNCKO

SO -> F
OP -> V
NF -> F
BO -> V
BH -> S
VB -> B
SV -> B
BK -> S
KC -> N
SP -> O
CP -> O
VN -> O
HO -> S
PC -> B
CS -> O
PO -> K
KF -> B
BP -> K
VO -> O
HB -> N
PH -> O
FF -> O
FB -> K
CC -> H
FK -> F
HV -> P
CO -> S
OC -> N
KV -> V
SS -> O
FC -> O
NP -> B
OH -> B
OF -> K
KB -> K
BN -> C
OK -> C
NC -> O
NO -> O
FS -> C
VP -> K
KP -> S
VS -> B
VV -> N
NN -> P
KH -> P
OB -> H
HP -> H
KK -> H
FH -> F
KS -> V
BS -> V
SN -> H
CB -> B
HN -> K
SB -> O
OS -> K
BC -> H
OV -> N
PN -> B
VH -> N
SK -> C
PV -> K
VC -> N
PF -> S
NB -> B
PP -> S
NS -> F
PB -> B
CV -> C
HK -> P
PK -> S
NH -> B
SH -> V
KO -> H
NV -> B
HH -> V
FO -> O
CK -> O
VK -> F
HF -> O
BF -> C
BV -> P
KN -> K
VF -> C
FN -> V
ON -> C
SF -> F
SC -> C
OO -> S
FP -> K
PS -> C
NK -> O
BB -> V
HC -> H
FV -> V
CH -> N
HS -> V
CF -> F
CN -> S"""


def solve(template_and_rules_str):
    template = None
    rules = {}

    pair_counts = defaultdict(int)

    for line in template_and_rules_str.split("\n"):
        if template is None:
            template = line
        elif not line:
            continue
        else:
            pair, insertion = line.split(" -> ")
            rules[pair] = insertion

    for i, c in enumerate(template[:-1]):
        pair_counts[c+template[i+1]] += 1

    for step in range(40):
        new_pairs = defaultdict(int)
        for pair, count in pair_counts.items():
            """
            given a pair xy that maps to insertion z,
            the inserted string is xzy, which means we have
            2 new pairs: xz, zy
            xz and zy will both be added to the next version of the string
            for every time xy exists in the original string,
            which is why we add `count` for each of the new pairs
            """
            insertion = rules[pair]
            new_pairs[pair[0] + insertion] += count
            new_pairs[insertion + pair[1]] += count

        pair_counts = new_pairs

    char_freq = defaultdict(int)

    for pair, count in pair_counts.items():
        a, b = pair[0], pair[1]
        char_freq[a] += count
        char_freq[b] += count

    char_freq[template[0]] -= 1
    char_freq[template[-1]] -= 1

    for char in char_freq:
        assert char_freq[char] % 2 == 0
        char_freq[char] //= 2

    char_freq[template[0]] += 1
    char_freq[template[-1]] += 1

    min_count = float('inf')
    max_count = float('-inf')

    for count in char_freq.values():
        min_count = min(min_count, count)
        max_count = max(max_count, count)

    return max_count - min_count

if __name__ == "__main__":
    assert solve(TEST_INPUT) == 2188189693529
    print(solve(PUZZLE_INPUT))
