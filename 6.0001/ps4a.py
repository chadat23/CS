# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    # >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) == 1:
        return [sequence]

    first_letter = sequence[0]
    all_permutations = []
    permutations = get_permutations(sequence[1:])
    for word in permutations:
        for i in range(len(word) + 1):
            beginning_letters = word[:i] if i > 0 else ''
            ending_letters = word[i:] if i < len(word) else ''
            all_permutations.append(beginning_letters + first_letter + ending_letters)

    return all_permutations


if __name__ == '__main__':
    #    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    example_input = 'cat'
    print('Input:', example_input)
    print('Expected Output:', ['cat', 'act', 'atc', 'cta', 'tca', 'tac'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'dog'
    print('Input:', example_input)
    print('Expected Output:', ['dog', 'odg', 'ogd', 'dgo', 'gdo', 'god'])
    print('Actual Output:', get_permutations(example_input))

    example_input = 'hen'
    print('Input:', example_input)
    print('Expected Output:', ['hen', 'ehn', 'enh', 'hne', 'nhe', 'neh'])
    print('Actual Output:', get_permutations(example_input))
