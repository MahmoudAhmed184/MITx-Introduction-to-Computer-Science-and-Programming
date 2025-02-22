import string
import math
from ps4a import get_permutations


def load_words(file_name: str) -> list[str]:
    """
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    inFile = open(file_name, "r")
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(" ")])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list: list[str], word: str) -> bool:
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    """

    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


WORDLIST_FILENAME = "words.txt"

VOWELS_LOWER = "aeiou"
VOWELS_UPPER = "AEIOU"
CONSONANTS_LOWER = "bcdfghjklmnpqrstvwxyz"
CONSONANTS_UPPER = "BCDFGHJKLMNPQRSTVWXYZ"


class SubMessage(object):
    def __init__(self, text: str):
        """
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """

        self.message_text = text
        self.valid_words = load_words(f"OpenCourseWare\Problem Set 4\{WORDLIST_FILENAME}")

    def get_message_text(self) -> str:
        """
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        """

        return self.message_text

    def get_valid_words(self) -> list[str]:
        """
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        """

        return self.valid_words.copy()

    def build_transpose_dict(self, vowels_permutation: str) -> dict[str, str]:
        """
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """

        transpose_dict = {letter: letter for letter in string.ascii_letters}
        for index, vowel in enumerate(VOWELS_LOWER):
            transpose_dict[vowel] = vowels_permutation[index]
            transpose_dict[vowel.upper()] = vowels_permutation[index].upper()

        return transpose_dict

    def apply_transpose(self, transpose_dict: dict[str, str]) -> str:
        """
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        """

        return "".join([transpose_dict.get(char, char) for char in self.message_text])


class EncryptedSubMessage(SubMessage):
    def __init__(self, text: str):
        """
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """

        super().__init__(text)

    def decrypt_message(self) -> str:
        """
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message

        Hint: use your function from Part 4A
        """

        permutations = get_permutations(VOWELS_LOWER)
        max_words = -math.inf

        for permutation in permutations:
            transpose_dict = self.build_transpose_dict(permutation)
            decoded_message = self.apply_transpose(transpose_dict)

            word_count = sum(is_word(self.valid_words, word) for word in decoded_message.split())

            if word_count > max_words:
                max_words, best_message = word_count, decoded_message

        return best_message if max_words > 0 else self.get_message_text()


if __name__ == "__main__":
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    print("\n--- Additional Test Cases ---")

    # Test Case 1: Check transpose dictionary mappings
    msg = SubMessage("Test")
    perm = "eaiuo"
    trans_dict = msg.build_transpose_dict(perm)
    print("\nTest Case 1: Transpose Dictionary")
    print("Expected a->e, e->a, i->i, o->u, u->o")
    print(f"Actual: a->{trans_dict['a']}, e->{trans_dict['e']}, i->{trans_dict['i']}, o->{trans_dict['o']}, u->{trans_dict['u']}")
    print(f"Upper case: A->{trans_dict['A']}, E->{trans_dict['E']}, I->{trans_dict['I']}, O->{trans_dict['O']}, U->{trans_dict['U']}")

    # Test Case 2: Apply transpose to all vowels
    msg = SubMessage("AEIOU aeiou")
    perm = "uoeai"
    trans_dict = msg.build_transpose_dict(perm)
    encrypted = msg.apply_transpose(trans_dict)
    print("\nTest Case 2: Encrypt All Vowels")
    print("Expected: UOEAI uoeai")
    print("Actual:", encrypted)

    # Test Case 3: No vowels in message
    msg = SubMessage("BCDFG bcdfg!")
    perm = "aeiou"
    encrypted = msg.apply_transpose(msg.build_transpose_dict(perm))
    print("\nTest Case 3: No Vowels Encryption")
    print("Expected: BCDFG bcdfg!")
    print("Actual:", encrypted)

    # Test Case 4: Decrypt a simple message
    original = "Cats and dogs"
    msg = SubMessage(original)
    perm = "eaiuo"
    encrypted = msg.apply_transpose(msg.build_transpose_dict(perm))
    enc_msg = EncryptedSubMessage(encrypted)
    decrypted = enc_msg.decrypt_message()
    print("\nTest Case 4: Decryption Check")
    print("Original:", original)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

    # Test Case 5: Decrypt message with no valid words
    encrypted_msg = "XyzzY zyxx!"
    enc_msg = EncryptedSubMessage(encrypted_msg)
    decrypted = enc_msg.decrypt_message()
    print("\nTest Case 5: No Valid Decryption")
    print("Encrypted:", encrypted_msg)
    print("Decrypted:", decrypted)

    # Test Case 6: Mixed case and punctuation
    msg = SubMessage("Hi! How's it going?")
    perm = "uoeai"
    encrypted = msg.apply_transpose(msg.build_transpose_dict(perm))
    expected_encrypted = "He! Haw's et gaeng?"
    print("\nTest Case 6: Mixed Case and Punctuation")
    print("Expected Encrypted:", expected_encrypted)
    print("Actual Encrypted:", encrypted)
    enc_msg = EncryptedSubMessage(encrypted)
    decrypted = enc_msg.decrypt_message()
    print("Decrypted Message:", decrypted)
