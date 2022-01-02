import sys

NEXT_NOTE = {
    'C': 'D',
    'D': 'E',
    'E': 'F',
    'F': 'G',
    'G': 'A',
    'A': 'B',
    'B': 'C',
}
NOTE_INTERVALS = {
    'C': 2,
    'D': 2,
    'E': 1,
    'F': 2,
    'G': 2,
    'A': 2,
    'B': 1,
}


class Scale(object):
    def __init__(self, root: str, intervals: [int]):
        self.root = root
        self.intervals = intervals

    def notes(self) -> [str]:
        notes = [self.root]
        last_whole_note = self.root[0]
        for interval in self.intervals:
            next_whole_note = NEXT_NOTE[last_whole_note]
            last_whole_note = next_whole_note
            if notes[-1] in NOTE_INTERVALS:
                if NOTE_INTERVALS[notes[-1]] == interval:
                    notes.append(next_whole_note)
                elif NOTE_INTERVALS[notes[-1]] < interval:
                    notes.append(next_whole_note + '#')
                elif NOTE_INTERVALS[notes[-1]] > interval:
                    notes.append(next_whole_note + 'b')
            else:
                if NOTE_INTERVALS[notes[-1][0]] == interval:
                    notes.append(next_whole_note + notes[-1][1])
                else:
                    notes.append(next_whole_note)
        return notes


def parse_scale() -> Scale:
    root = sys.stdin.readline().strip()
    string_intervals = sys.stdin.readline().strip()
    intervals = [1 if si == 's' else 2 for si in string_intervals]
    return Scale(root, intervals)


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        scale = parse_scale()
        print("Case #{}: {}".format(test + 1, "".join(scale.notes())))


if __name__ == '__main__':
    solve()

