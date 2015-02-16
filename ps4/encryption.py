# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")

    return word in wordlist

#print is_word(wordlist,'Hello')

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    coding_dict = {}

    coding_keys_lower = list(string.lowercase + ' ')

    coding_keys_upper = list(string.uppercase + ' ')


    for i,j in enumerate(coding_keys_upper):

        if j.isupper():
            num = i+shift

            if num<0:
                coding_dict[j] = (coding_keys_upper[num+27])

            elif num<=26:
                coding_dict[j] = (coding_keys_upper[num])

            elif num>26:
                coding_dict[j] = (coding_keys_upper[num-27])


    for i,j in enumerate(coding_keys_lower):
        num = i+shift

        if num<0:
            coding_dict[j] = (coding_keys_lower[num+27])

        elif num<=26:
            coding_dict[j] = (coding_keys_lower[num])

        elif num>26:
            coding_dict[j] = (coding_keys_lower[num-27])



    return coding_dict

#print build_coder(1)


def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """

    encoding_dict = {}

    encoding_dict = build_coder(shift)

    return encoding_dict


def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    assert shift in range(0,28)

    decoding_dict = {v: k for k, v in build_coder(shift).items()}

    return decoding_dict


def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    :rtype : string
    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    new_text = list(text)

    for index,letter in enumerate(new_text):

        if letter in coder.keys():
            new_text[index] = coder[letter]

    return ''.join(new_text)

#print apply_coder("Pmttw,hdwztl!", build_decoder(8))

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    new_text = list(text)

    for index,letter in enumerate(new_text):

        if letter in build_encoder(shift).keys():
            new_text[index] = build_encoder(shift)[letter]

    return ''.join(new_text)

#print apply_shift('This is a test.', 8)


#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    maximum_real_words = 0
    best_shift = 0

    for shift in range(0,28):
        valid_word = apply_coder(text, build_coder(shift))
        list_valid_word = valid_word.split()

        for word in list_valid_word:
            count_valid_word = 0
            if is_word(wordlist, word):
                count_valid_word += 1

        if count_valid_word > maximum_real_words:
            count_valid_word = maximum_real_words
            best_shift = shift

    return best_shift

#print find_best_shift(wordlist, 'Pmttw,hdwztl!')

# Problem 3: Multi-level encryption.

def encoder_multilayer(shift_num):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.)

    shift_num: int
    returns: dict
    """

    multi_coding_dict = {}

    coding_keys_lower = list(string.lowercase + ' ')

    coding_keys_upper = list(string.uppercase + ' ')

    for i, j in enumerate(coding_keys_upper):

        if j.isupper():

            num = i+shift_num

            if num < 0:
                multi_coding_dict[j] = coding_keys_upper[num+27]

            elif num <= 26:
                multi_coding_dict[j] = coding_keys_upper[num]

            elif num > 26:
                n = num/27
                if n >= 2:
                    multi_coding_dict[j] = coding_keys_upper[num-(27*int(n))]
                else:
                    multi_coding_dict[j] = coding_keys_upper[num-27]
                # print n
                # print num
                # print shift_num

    for i,j in enumerate(coding_keys_lower):

        num = i+shift_num

        if num < 0:
            multi_coding_dict[j] = coding_keys_lower[num+27]

        elif num <= 26:
            multi_coding_dict[j] = coding_keys_lower[num]

        elif num > 26:
            n = num/27
            if n >= 2:
                multi_coding_dict[j] = coding_keys_lower[num-(27*int(n))]
            else:
                multi_coding_dict[j] = coding_keys_lower[num-27]

    return multi_coding_dict


def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """

    new_text = list(text)

    shift_digits = 0

    for elements in shifts:
        location = elements[0]
        shift_digits = elements[1]

        for index, letter in enumerate(new_text):

            if index >= location:

                if letter in encoder_multilayer(shift_digits).keys():
                    new_text[index] = encoder_multilayer(shift_digits)[letter]

                #print new_text
                #print shift_digits
                #print encoder_multilayer(shift_digits)
    return ''.join(new_text)

#print apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)

    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """


def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scrambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """

    for shift in range(1, 28):
        before_start = text[:start]
        after_start = apply_shifts(text, [(start, shift)])
        s = before_start + after_start

        try:
            word_end_index = after_start[start:].index(' ')+1+start
        except ValueError:
            word_end_index = len(after_start)

        word = after_start[start:word_end_index]

        if is_word(wordlist, word):
            #print 'start=',start, 'shift=',shift,  word, 'after start=', after_start, 'len string=', len(after_start), 'word_end_index=', word_end_index
            if word_end_index == len(after_start):
                shifts = [(start, 27 - shift)]
                return shifts
            else:
                next_start = word_end_index
                value = find_best_shifts_rec(wordlist, after_start, next_start)

                if value:
                    if value[0][1] == 0:
                        value = value[1:]
                    return [(start, 27 - shift)] + value

print find_best_shifts_rec(wordlist, 'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?', 0)

# s = find_best_shifts_rec(wordlist, 'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?', 0)
#
# print apply_shifts('JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?',s)

def decrypt_fable():
     """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    ### TODO.




#What is the moral of the story?
#
#
#
#
#

