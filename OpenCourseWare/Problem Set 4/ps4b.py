import string
import math


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


def get_story_string() -> str:
    """
    Returns: a story in encrypted text.
    """

    f = open("OpenCourseWare\Problem Set 4\story.txt", "r")
    story = str(f.read())
    f.close()
    return story


WORDLIST_FILENAME = "words.txt"


class Message(object):
    def __init__(self, text: str):
        """
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
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

    def build_shift_dict(self, shift: int) -> dict[str, str]:
        """
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """

        shift_dict = {}
        
        for index, letter in enumerate(string.ascii_lowercase):
            encoded_letter = string.ascii_lowercase[(index + shift) % 26]
            shift_dict[letter] = encoded_letter
            shift_dict[letter.upper()] = encoded_letter.upper()

        return shift_dict

    def apply_shift(self, shift: int) -> str:
        """
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        """

        shift_dict = self.build_shift_dict(shift)

        return "".join([shift_dict.get(char, char) for char in self.message_text])


class PlaintextMessage(Message):
    def __init__(self, text: str, shift: int):
        """
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        """

        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self) -> int:
        """
        Used to safely access self.shift outside of the class

        Returns: self.shift
        """

        return self.shift

    def get_encryption_dict(self) -> dict[str, str]:
        """
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        """

        return self.encryption_dict.copy()

    def get_message_text_encrypted(self) -> str:
        """
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        """

        return self.message_text_encrypted

    def change_shift(self, shift):
        """
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        """

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        """
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        """

        super().__init__(text)

    def decrypt_message(self) -> tuple[int, str]:
        """
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """

        max_words = -math.inf
        for shift in range(26):
            decoded_message = self.apply_shift(shift)
            word_count = sum(is_word(self.valid_words, word) for word in decoded_message.split())
            if word_count > max_words:
                max_words, best_fit, best_shift = word_count, decoded_message, shift

        return (best_shift, best_fit)


if __name__ == "__main__":
    # Original test cases
    plaintext = PlaintextMessage("hello", 2)
    print("Test 1 - Basic Encryption:")
    print("Expected Output: jgnnq")
    print("Actual Output:  ", plaintext.get_message_text_encrypted())
    print("------")

    ciphertext = CiphertextMessage("jgnnq")
    print("Test 2 - Basic Decryption:")
    print("Expected Output:", (24, "hello"))
    print("Actual Output:  ", ciphertext.decrypt_message())
    print("------")

    # New test cases
    # Test 3: Empty string
    plaintext = PlaintextMessage("", 5)
    print("Test 3 - Empty String:")
    print("Expected Output: ")
    print("Actual Output:  ", f"{plaintext.get_message_text_encrypted()}")
    print("------")

    # Test 4: Non-alphabetic characters
    plaintext = PlaintextMessage("Python3.8!", 4)
    print("Test 4 - Non-alphabetic Characters:")
    print("Expected Output: Tcxlsr3.8!")
    print("Actual Output:  ", plaintext.get_message_text_encrypted())
    print("------")

    # Test 5: Upper/lower case mix with punctuation
    plaintext = PlaintextMessage("Hello, World!", 13)
    print("Test 5 - Case Mix with Punctuation:")
    print("Expected Output: Uryyb, Jbeyq!")
    print("Actual Output:  ", plaintext.get_message_text_encrypted())
    print("------")

    # Test 6: Large shift value (32 ≡ 6 mod 26)
    plaintext = PlaintextMessage("secret", 32)
    print("Test 6 - Large Shift Value:")
    print("Expected Output: ykixkz")
    print("Actual Output:  ", plaintext.get_message_text_encrypted())
    print("------")

    # Test 7: Shift 0 (no change)
    plaintext = PlaintextMessage("NoChange", 0)
    print("Test 7 - Zero Shift:")
    print("Expected Output: NoChange")
    print("Actual Output:  ", plaintext.get_message_text_encrypted())
    print("------")

    # Test 8: Change shift after initialization
    plaintext = PlaintextMessage("apple", 2)
    print("Test 8 - Change Shift:")
    print("Original Shift (2):", plaintext.get_message_text_encrypted())
    plaintext.change_shift(5)
    print("New Shift (5):     ", plaintext.get_message_text_encrypted())
    print("------")

    # Story decryption
    print("Final Story Decryption:")
    story = get_story_string()
    ciphertext = CiphertextMessage(story)
    decrypted = ciphertext.decrypt_message()
    print(f"Best Shift: {decrypted[0]}")
    print("Decrypted Story:")
    print(decrypted[1])