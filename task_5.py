def get_connected_words(user_word: str, words: tuple[str, ...]) -> list[str]:
    """
    Connects user word with words from list
    if user word ending is equal to beginning of word from list.
    :param user_word: word inputted by user
    :param words: tuple of words
    :return: list of connected words
    """
    result = []
    for word in words:
        if word != user_word:
            for i in range(1, len(user_word)):
                if word.startswith(user_word[i:]):
                    result.append(f'{user_word[:i]}{word}')
    return result


def solution(file_name: str) -> None:
    """
    Collects words from file, accepts user word input,
    connects user word with collected words and prints connected words.
    :param file_name: path to file with words
    :return: None
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        words = tuple(line.strip() for line in f.readlines())
    while True:
        print('Press Ctrl + C to exit...')
        user_word = input('Input word: ')
        connected_words = get_connected_words(user_word, words)
        for word in connected_words:
            print(word)


if __name__ == '__main__':
    solution('test.txt')
