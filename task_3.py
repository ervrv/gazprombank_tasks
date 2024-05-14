def solution(matrix: list[list]) -> None:
    """
    Prints list of lists converted to list of dicts.
    :param matrix: list of lists
    :return: None
    """
    b = [{f'k{i + 1}': lst[i] for i in range(len(lst))} for lst in matrix]
    print(f'b = {b}')


if __name__ == '__main__':
    solution([[1, 2, 3], [4, 5, 6]])
