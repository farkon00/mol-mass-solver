import sys

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator

from elements import dict_el

class TokenKind(Enum):
    ELEM = auto()
    NUM = auto()
    L_BRACK = auto()
    R_BRACK = auto()

@dataclass
class Token:
    kind: TokenKind
    val: str

def get_generic_tok_type(tok: str) -> TokenKind:
    if tok.isnumeric():
        return TokenKind.NUM
    else:
        return TokenKind.ELEM

def lex(string: str) -> list[Token]:
    tokens = []
    tok = ""
    for char in string:
        if char == "(":
            if tok:
                tokens.append(Token(get_generic_tok_type(tok), tok))
            tokens.append(Token(TokenKind.L_BRACK, "("))
            tok = ""
        elif char == ")":
            if tok:
                tokens.append(Token(get_generic_tok_type(tok), tok))
            tokens.append(Token(TokenKind.R_BRACK, ")"))
            tok = ""
        elif char.isupper() or char.isnumeric():
            if tok:
                tokens.append(Token(get_generic_tok_type(tok), tok))
            tok = char
        elif char.isspace():
            if tok:
                tokens.append(Token(get_generic_tok_type(tok), tok))
            tok = ""
        else:
            tok += char
    
    if tok:
        tokens.append(Token(get_generic_tok_type(tok), tok))

    return tokens

def add_elem(elems: list[tuple[int, str]], elem: tuple[int, str]):
    elem_index = None
    for index, e in enumerate(elems):
        if e[1] == elem[1]:
            elem_index = index
    if elem_index is not None:
        elems[elem_index] = (elem[0] + elems[elem_index][0], elem[1])
    else:
        elems.append(elem)

def parse(tokens: Iterator[Token], nested: bool = False) -> list[tuple[int, str]]:
    elems: list[tuple[int, str]] = []
    elem = None
    elem_bracks = None

    for tok in tokens:
        if tok.kind == TokenKind.ELEM:
            if elem:
                add_elem(elems, (1, elem))
            elem = tok.val
        elif tok.kind == TokenKind.NUM:
            if elem:
                add_elem(elems, (int(tok.val), elem))
                elem = None
            elif elem_bracks:
                for e in elem_bracks:
                    add_elem(elems, (e[0]*int(tok.val), e[1]))
                elem_bracks = None
            else:
                print("Invalid position of an index")
                exit(1)
        elif tok.kind == TokenKind.L_BRACK:
            elem_bracks = parse(tokens, nested=True)
        elif tok.kind == TokenKind.R_BRACK:
            if not nested:
                print("Bracket wasn't matched")
                exit(1)
            break
    else:
        if nested:
            print("Bracket was not closed")
            exit(1)

    if elem is not None:
        add_elem(elems, (1, elem))

    if elem_bracks is not None:
        for e in elem_bracks:
            add_elem(elems, e)

    return elems

def get_atom_mass(elem: str) -> int:
    if elem in dict_el:
        return dict_el[elem]
    else:
        print(f"Element \"{elem}\" was not found")
        exit(1)

def compute_molecular_mass(elems: list[tuple[int, str]]) -> int:
    return sum(map(
        lambda elem: get_atom_mass(elem[1]) * elem[0], 
        elems
    ))

def get_verbose_output(elems: list[tuple[int, str]]) -> str:
    return " + ".join([f"{elem[0]} * {get_atom_mass(elem[1])}" for elem in elems]) +\
        f" = {compute_molecular_mass(elems)}"

def get_output(elems: list[tuple[int, str]]) -> int | str:
    return (get_verbose_output(elems) if "-v" in sys.argv
        else compute_molecular_mass(elems))

def main():
    while True:
        print(get_output(parse(iter(lex(input())))))

if __name__ == "__main__":
    main()