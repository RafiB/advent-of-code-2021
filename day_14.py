from collections import defaultdict
import threading


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

    for line in template_and_rules_str.split("\n"):
        if template is None:
            template = list(line)
        elif not line:
            continue
        else:
            pair, insertion = line.split(" -> ")
            rules[pair] = insertion

    def chunk(template):
        every = len(template) // 3

        max_size = min(every, 1000000)

        chunks = []

        start = 0
        end = max_size
        while start <= len(template):
            chunks.append(template[start:end + 1])
            start += max_size
            end += max_size

        return chunks


    def run_insertions(pos, template, answers):
        insertions = []
        for c in range(len(template)-1):
            insertions.append(rules[template[c]+template[c+1]])

        new_template = template + insertions
        i = 0
        for c in range(len(template)):
            new_template[i] = template[c]
            i += 1
            if c < len(template) - 1:
                new_template[i] = insertions[c]
                i += 1
        answers[pos] = new_template

    for i in range(40):
        print("step", i, len(template))
        threads = []
        chunks = chunk(template)
        answers = [None for _ in range(len(chunks))]
        for i, c in enumerate(chunks):
            t = threading.Thread(target=run_insertions, args=(i, c, answers))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        template = answers[0]
        for a in answers[1:]:
            template += a[1:]

    most_common_count = float('-inf')
    least_common_count = float('inf')
    most_common = None
    least_common = None

    counts = defaultdict(int)
    print("counting")
    for c in template:
        counts[c] += 1

    print("minning")
    for c, count in counts.items():
        if count > most_common_count:
            most_common_count = count
            most_common = c
        if count < least_common_count:
            least_common_count = count
            least_common = c

    return most_common_count - least_common_count

if __name__ == "__main__":
    assert solve(TEST_INPUT) == 2188189693529
    print(solve(PUZZLE_INPUT))
