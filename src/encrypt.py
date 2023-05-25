#!/usr/bin/env python3
"""
Encryption Algorithms for the project

Author:  Frederik Beimgraben (github/frederikbeimgraben)
Created: 2023-05-16

Contains:
    - Simple Caesar Shift
    - Vigenere Cipher
"""

# Standard imports
from math import log
import random
import string
from typing import Callable, Dict, Generator, Iterable, List, Sized, SupportsIndex, Optional, Tuple

# Type Hints  (I just like type hints, okay?)
S = str | bytes | int

A = List[S] | str | Tuple[S]

T = Iterable[S]

class KeyStr(List[S], Sized, SupportsIndex, Iterable[S]):
    pass

KS = KeyStr | str

K = int

# Functions
## Invert the Alphabet Table
def invert_table(table: A) -> Dict[S, int]:
    """
    Inverts an alphabet table.

    Args:
        table (A, optional): The alphabet to invert. Defaults to alphabet.

    Returns:
        A: The inverted alphabet.
    """
    return {
        value: key
        for key, value in enumerate(table)
    }

## Hashing Algorithm to convert a sequence of symbols to an offset value 
## (For Caesar Shift by Word Key)
def hash_sequence(text: T | KS | S, table: A) -> int:
    """
    Hashes a sequence of symbols to an offset value.

    Args:
        text (T): The text to hash.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        int: The hashed offset value.
    """

    if isinstance(text, S):
        if isinstance(text, str):
            return table.index(text)
        elif isinstance(text, int):
            return text
        elif isinstance(text, bytes):
            return table.index(text)
        else:
            raise TypeError(f"Cannot hash sequence of type {type(text)}")

    
    inverted: Dict[S, int] = invert_table(table)

    return sum(
        inverted[symbol]
        for symbol in text if symbol in inverted
    ) % len(table)

## Shifting Algorithms
### Simple Caesar Shift
def shift_symbol(symbol: S, shift: int, table: A) -> S:
    """
    Shifts a symbol by a given shift value.

    Args:
        symbol (S): The symbol to shift.
        shift (int): The shift value.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        S: The shifted symbol.
    """

    if symbol not in table:
        # if isinstance(symbol, str):
        #     symbol = str(symbol.encode("utf-8"))[2:-1]
        # raise ValueError(f"The symbol '{symbol}' is not in the alphabet.")
        return symbol

    index: int = table.index(symbol)

    return table[(index + shift) % len(table)]

def caesar_shift_sequence(text: T, offset: int, table: A) -> Generator[S, None, None]:
    """
    Shifts a Sequence by a given offset value.

    Args:
        text (T): The text to shift.
        offset (int): The offset value.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        Generator[S, None, None]: The shifted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """

    return (
        shift_symbol(symbol, offset, table)
        for symbol in text
    )

def caesar_encrypt_sequence(text: T, key: int, table: A) -> Generator[S, None, None]:
    """
    Encrypts a sequence using a Caesar Shift.

    Args:
        text (T): The text to encrypt.
        key (int): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        Generator[S, None, None]: The encrypted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """

    return caesar_shift_sequence(text, key, table)

def caesar_decrypt_sequence(text: T, key: int, table: A) -> Generator[S, None, None]:
    """
    Decrypts a sequence using a Caesar Shift.

    Args:
        text (T): The text to decrypt.
        key (int): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        Generator[S, None, None]: The decrypted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """

    return caesar_shift_sequence(text, -key, table)

def caesar_encrypt_str(text: str, key: int, table: A) -> str:
    """
    Encrypts a text using a Caesar Shift.

    Args:
        text (T): The text to encrypt.
        key (int): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        str: The encrypted text.
    """

    return "".join(
        str(symbol) for symbol in
        caesar_encrypt_sequence(text, key, table)
    )

def caesar_decrypt_str(text: str, key: int, table: A) -> str:
    """
    Decrypts a text using a Caesar Shift.

    Args:
        text (T): The text to decrypt.
        key (int): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        str: The decrypted text.
    """

    return "".join(
        str(symbol) for symbol in
        caesar_decrypt_sequence(text, key, table)
    )


### Vigenere Cipher
def vigenere_shift_sequence(
        text: T,
        key: KS,
        reverse: bool=False,
        table: Optional[A]=None,
        assert_len=False) -> Generator[S, None, None]:
    """
    Shifts a sequence by a given key.

    Args:
        text (T): The text to shift.
        key (T): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        Generator[S, None, None]: The shifted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """
    
    if table is None:
        raise ValueError("The alphabet must be specified.")

    
    return (
        shift_symbol(
            symbol,
            (
                (
                    hash_sequence(skey, table)
                    if not isinstance(skey := key[i % len(key)], int)
                    else skey
                )
                * (-1 if reverse else 1)
            ),
            table
        ) for i, symbol in enumerate(text)
    )

def vigenere_encrypt_sequence(text: T, key: KS, table: A) -> Generator[S, None, None]:
    """
    Shifts a sequence by a given key.

    Args:
        text (T): The text to shift.
        key (T): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        Generator[S, None, None]: The shifted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """

    return vigenere_shift_sequence(
        text=text,
        key=key,
        table=table
    )

def vigenere_decrypt_sequence(text: T, key: KS, table: A) -> Generator[S, None, None]:
    """
    Shifts a sequence by a given key.

    Args:
        text (T): The text to shift.
        key (T): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        Generator[S, None, None]: The shifted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """

    return vigenere_shift_sequence(
        text=text,
        key=key,
        reverse=True,
        table=table
    )

def vigenere_encrypt_str(text: str, key: str, table: A) -> str:
    """
    Encrypts a text using a Vigenere Cipher.

    Args:
        text (T): The text to encrypt.
        key (T): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        str: The encrypted text.
    """

    return "".join(
        str(symbol) for symbol in
        vigenere_encrypt_sequence(text, key, table)
    )

def vigenere_decrypt_str(text: str, key: str, table: List[str] | str) -> str:
    """
    Decrypts a text using a Vigenere Cipher.

    Args:
        text (T): The text to decrypt.
        key (T): The key to use.
        table (A, optional): The alphabet to use. Defaults to alphabet.

    Returns:
        str: The decrypted text.
    """

    return "".join(
        str(symbol) for symbol in
        vigenere_decrypt_sequence(text, key, table)
    )

def vigenere_monogram_freq(
        text: str,
        alphabet: str | List[str]) -> Dict[S, float]:
    """
    Calculates the monogram frequency of a text.

    Args:
        text (T): The text to calculate the monogram frequency of.
        alphabet (A): The alphabet to use.

    Returns:
        Dict[S, float]: The monogram frequency.
    """

    return {
        symbol: text.count(symbol) / len(text)
        for symbol in alphabet
    }

def vigenere_tetragram_freq(
        text: str,
        alphabet: str | List[str]) -> Dict[S, float]:
    """
    Calculates the tetragram frequency of a text.

    Args:
        text (T): The text to calculate the tetragram frequency of.
        alphabet (A): The alphabet to use.

    Returns:
        Dict[S, float]: The tetragram frequency.
    """

    tetrafrequencies: List[int] = [0] * (len(alphabet)**4)
    for i in range(len(text) - 3):
        x: int = (
            alphabet.index(text[i])*(len(alphabet)**3) +
            alphabet.index(text[i+1])*(len(alphabet)**2) +
            alphabet.index(text[i+2])*len(alphabet) +
            alphabet.index(text[i+3])
        )
        tetrafrequencies[x] += 1
    for i, _ in enumerate(tetrafrequencies):
        tetrafrequencies[i] = tetrafrequencies[i] / (len(text)-3) # type: ignore

def vigenere_fitness(
        text: str,
        alphabet: str | List[str],):
    
    result = 0

    tetrafrequencies = vigenere_tetragram_freq(text, alphabet)

    for i in range(len(text)-3):
        tetragram = text[i:i+4]
        x = (
            alphabet.index(tetragram[0])*(len(alphabet)**3) +
            alphabet.index(tetragram[1])*(len(alphabet)**2) +
            alphabet.index(tetragram[2])*(len(alphabet)) +
            alphabet.index(tetragram[3])
        )

        y = tetrafrequencies[x]
        if y == 0:
            result += -15 # some large negative number
        else:
            result += log(y)
    result = result / (len(text) - 3)
    return result

def index_of_coincidence(
        text: str,
        alphabet: str | List[str]) -> float:
    counts = [0]*len(alphabet)
    for char in text:
        counts[alphabet.index(char)] += 1
    numer = 0
    total = 0
    for i, _ in enumerate(alphabet):
        numer += counts[i]*(counts[i]-1)
        total += counts[i]
    return len(alphabet)*numer / (total*(total-1))

def find_period(
        text: str,
        alphabet: str | List[str]) -> int:
    """
    Finds the period of a text.

    Args:
        text (str): The text to find the period of.
        alphabet (str | List[str]): The alphabet to use.

    Returns:
        int: The period of the text.
    """

    period: int = 0
    while True:
        period += 1
        slices = ['']*period
        for i in range(len(text)):
            slices[i%period] += text[i]
        sum = 0
        for i in range(period):
            sum += index_of_coincidence(
                slices[i],
                alphabet
            )
        ioc = sum / period
        if ioc > 1.6:
            return period

def vigenere_break_vari(
        text: str,
        alphabet: str | List[str]) -> Tuple[str, str]:
    """
    Breaks a Vigenere Cipher using the Variational Method.

    Args:
        text (str): The text to break.
        alphabet (str | List[str]): The alphabet to use.

    Returns:
        Tuple[str, str]: The key and the decrypted text.
    """

    period = find_period(text, alphabet)

    key = ['A']*period
    fit = -99 # some large negative number
    while fit < -10:
        print("Trying key: " + "".join(key))
        K = key[:]
        x = random.randrange(period)
        for i, _ in enumerate(alphabet):
            K[x] = alphabet[i]
            pt = vigenere_decrypt_str(
                text,
                "".join(K),
                alphabet
            )

            F = vigenere_fitness(pt, alphabet)
            if (F > fit):
                key = K[:]
                fit = F
    
    return ("".join(key), vigenere_decrypt_str(text, "".join(key), alphabet))


### Enigma
class EnigmaRotor(Iterable[S]):
    alphabet: A
    position: int
    init_mapping: List[S]

    def __init__(self, alphabet: A, position: int, mapping: List[S]):
        self.alphabet = alphabet
        self.position = position
        self.init_mapping = mapping

    @property
    def mapping_list(self) -> List[S]:
        return self.init_mapping[self.position:] + self.init_mapping[:self.position]
    
    @property
    def mapping(self) -> Dict[S, S]:
        return dict(zip(self.alphabet, self.mapping_list))
    
    @property
    def reverse_mapping(self) -> Dict[S, S]:
        return dict(zip(self.mapping_list, self.alphabet))

    def __call__(self, key: S) -> S:
        """
        Encrypts a single symbol.
        """

        if key not in self.mapping:
           return key

        return self.mapping[key]
    
    def __getitem__(self, key: S) -> S:
        """
        Decrypts a single symbol.
        """

        if key not in self.reverse_mapping:
            return key

        return self.reverse_mapping[key]

    def __repr__(self) -> str:
        return f"<EnigmaRotor {self.position} {hash(self)}>"

    def __iter__(self) -> Iterable[S]:
        return self
    
    def __next__(self) -> 'EnigmaRotor':
        self.position = (self.position + 1) % len(self.alphabet)
        return self
    
    def __hash__(self) -> int:
        return sum(
            hash(symbol) * (i + 1)
            for i, symbol in enumerate(self.mapping_list)
        ) % 2**32

def enigma_encrypt_sequence(
        text: T,
        rotors: Tuple[EnigmaRotor, ...],
        offsets: Tuple[int, ...]) -> Generator[S, None, None]:
    """
    Encrypts a text using an Enigma Machine.

    Args:
        text (T): The text to encrypt.
        rotors (Tuple[EnigmaRotor, ...]): The rotors to use.
        offsets (Tuple[int, ...]): The offsets to use.

    Returns:
        Generator[S, None, None]: The encrypted text.
            We use a generator here to allow for lazy evaluation of eg. a stream of characters.
    """

    rotor_a, rotor_b, rotor_c = rotors

    # Copy the rotors
    rotor_a, rotor_b, rotor_c = (
        EnigmaRotor(
            alphabet=rotor.alphabet,
            position=offset,
            mapping=rotor.init_mapping
        ) for rotor, offset in zip(
            (rotor_a, rotor_b, rotor_c),
            offsets
        )
    )

    return (
        rotor_c(
            rotor_b(
                rotor_a(
                    symbol
                )
            )
        )
        for symbol, *_ in zip(
            text, 
            rotor_a, 
            rotor_b, 
            rotor_c
        )
    )

def enigma_decrypt_sequence(
        text: T,
        rotors: Tuple[EnigmaRotor, ...],
        offsets: Tuple[int, ...]) -> Generator[S, None, None]:
    """
    Decrypts a text using an Enigma Machine.

    Args:
        text (T): The text to decrypt.
        rotors (Tuple[EnigmaRotor, ...]): The rotors to use.
        offsets (Tuple[int, ...]): The offsets to use.

    Returns:
        Generator[S, None, None]: The decrypted text.

    Raises:
        ValueError: If the text contains a symbol not in the alphabet.
    """

    rotor_a, rotor_b, rotor_c = rotors

    # Copy the rotors
    rotor_a, rotor_b, rotor_c = (
        EnigmaRotor(
            alphabet=rotor.alphabet,
            position=offset,
            mapping=rotor.init_mapping
        ) for rotor, offset in zip(
            (rotor_a, rotor_b, rotor_c),
            offsets
        )
    )

    return (
        rotor_a[
            rotor_b[
                rotor_c[
                    symbol
                ]
            ]
        ]
        for symbol, *_ in zip(
            text,
            rotor_a,
            rotor_b,
            rotor_c
        )
    )

DEFAULT_alphabet = string.ascii_letters + string.digits + string.punctuation + ' '
BYTE_alphabet = tuple(i for i in range(256))

pseudo_random = random.Random(0)

# Pseudo randomize 5 alphabets
alphabetS = tuple(
    ''.join(pseudo_random.sample(DEFAULT_alphabet, len(DEFAULT_alphabet)))
    for _ in range(5)
)

BYTE_alphabetS = tuple(
    tuple(pseudo_random.sample(BYTE_alphabet, len(BYTE_alphabet)))
    for _ in range(5)
)

# Pseudo randomize 5 rotors
ROTORS = tuple(
    EnigmaRotor(
        alphabet=DEFAULT_alphabet,
        position=pseudo_random.randint(0, len(alphabet) - 1),
        mapping=list(alphabet)
    )
    for alphabet in alphabetS
)

BYTE_ROTORS = tuple(
    EnigmaRotor(
        alphabet=BYTE_alphabet,
        position=pseudo_random.randint(0, len(alphabet) - 1),
        mapping=list(alphabet)
    )
    for alphabet in BYTE_alphabetS
)

REPLACEMENTS = {
    ' ': '␣',
    '\n': '↵',
    '\t': '⇥',
    '\r': '⇤',
}


REPLACEMENTS_2 = {
    '\n': '↵\n',
    '\t': '⇥\t',
    '\r': '⇤',
}

# prettifying
def prettify(text: str) -> str:
    """
    Prettyfies a text.

    Args:
        text (str): The text to prettify.

    Returns:
        str: The prettyfied text.
    """

    return ''.join(
        REPLACEMENTS.get(char, char) for char in text
    )

def prettify2(text: str) -> str:
    """
    Prettyfies a text.

    Args:
        text (str): The text to prettify.

    Returns:
        str: The prettyfied text.
    """

    return ''.join(
        REPLACEMENTS_2.get(char, char) for char in text
    )

TEST_TEXT = \
"""Hello World! This is a test message.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
\t- Lorem Ipsum

0123456789()[]{}<>.,;:?!+-*/=\\|&%$#@^~`"'_
Wrong\rRight"""

TEST_TEXT_BYTES = tuple(
    ord(char) for char in TEST_TEXT
)