def apply_leetspeak(word):
    leet_map = {
        'a': '4', 'e': '3', 'i': '1',
        'o': '0', 's': '5', 't': '7'
    }
    return ''.join(leet_map.get(c.lower(), c) for c in word)