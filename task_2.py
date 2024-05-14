from itertools import chain


def solution(list_of_sets: list[set]) -> None:
    """
    Prints number, sum, average value and flattened view
    of integers in sets in list.
    :param list_of_sets: list of sets of integers
    :return: None
    """
    total_amount = sum((len(_set) for _set in list_of_sets))
    total_sum = sum((sum(_set) for _set in list_of_sets))
    to_tuple = tuple(chain.from_iterable(list_of_sets))

    print(f'Total number: {total_amount}')
    print(f'Total sum: {total_sum}')
    print(f'Average: {total_sum / total_amount}')
    print(f'To tuple: {to_tuple}')


if __name__ == '__main__':
    solution([{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}])
