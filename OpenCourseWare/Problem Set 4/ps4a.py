def get_permutations(sequence: str) -> list[str]:
    """
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    """
    if len(sequence) == 1:
        return [sequence]

    first_char = sequence[0]

    rest_permutations = get_permutations(sequence[1:])

    permutations = []

    for permutation in rest_permutations:
        for i in range(len(permutation) + 1):
            new_perm = permutation[:i] + first_char + permutation[i:]
            permutations.append(new_perm)

    return permutations


if __name__ == "__main__":
    example_input = "abc"
    print("Input:", example_input)
    print("Expected Output:", ["abc", "acb", "bac", "bca", "cab", "cba"])
    print("Actual Output:", get_permutations(example_input))

    test1 = "a"
    print("Input:", test1)
    print("Expected Output:", ["a"])
    print("Actual Output:", get_permutations(test1))

    test2 = "ab"
    print("Input:", test2)
    print("Expected Output:", ["ab", "ba"])
    print("Actual Output:", get_permutations(test2))
