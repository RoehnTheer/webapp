def search4letters(phrase: str, letters: str='aeiou') -> set:
    """Search for letters"""
    return set(phrase).intersection(set(letters))