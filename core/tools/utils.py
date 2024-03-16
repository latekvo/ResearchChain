
def purify_name(name):
    return '_'.join('_'.join(name.split(':')).split('-'))


def is_text_junk(text: str):
    # checks if text contains any of junky keywords eg: privacy policy, subscribe, cookies etc.
    # do not expand this list, it has to be small to be efficient, and these words are grouped either way.
    trigger_list = [
        'sign in', 'privacy policy', 'skip to', 'newsletter', 'subscribe', 'related tags', 'share price'
    ]
    low_text = text.lower()
    for trigger in trigger_list:
        if trigger in low_text:
            return True
    return False


def extract_from_quote(text: str):
    if '"' in text:
        return text.split('"')[1]
    else:
        return text


def reduce(text: str, goal: str, match: str):
    if match in text:
        text = goal.join(text.split(match))
        return reduce(text, goal, match)
    return goal.join(text.split(match))


def remove(text: str, wordlist: list):
    for word in wordlist:
        text = ''.join(text.split(word))
    return text
