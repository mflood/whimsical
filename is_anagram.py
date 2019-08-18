

def is_anagram(s1, s2):

    size = len(s1)
    if len(s2) != size:
        return False

    tracker = {}
    for i in range(size):
        tracker.setdefault(s1[i], 0)
        tracker[s1[i]] += 1
        if not tracker[s1[i]]:
            del tracker[s1[i]]

        tracker.setdefault(s2[i], 0)
        tracker[s2[i]] -= 1
        if not tracker[s2[i]]:
            del tracker[s2[i]]

        print(tracker)

    return len(tracker) == 0


print(is_anagram("tree", "eert"))
print(is_anagram("footballfootball", "ooballtfotobelfl"))
