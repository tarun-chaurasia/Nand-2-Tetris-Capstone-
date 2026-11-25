#!/usr/bin/env python3
"""
assembler.py - Hack assembler (.asm -> .hack), two passes.

Extra feature for K = 67  (67 mod 3 = 1):
    A wrong line prints a clear message with its line number
    (e.g. "Line 7: invalid instruction") instead of crashing.
    All errors in the file are reported; no .hack file is written if any exist.

Usage:  python3 assembler.py Prog.asm [Prog.hack]
"""
import re
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})

SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


def clean(line):
    """Remove comments and all whitespace."""
    return re.sub(r"\s+", "", line.split("//", 1)[0])


def first_pass(lines, symbols, errors):
    """Remove comments/blank lines, record label addresses.
    Returns list of (source_line_number, instruction_text)."""
    program = []
    labels_seen = {}
    for number, raw in enumerate(lines, start=1):
        text = clean(raw)
        if not text:
            continue
        if text.startswith("("):
            if not (text.endswith(")") and SYMBOL_RE.match(text[1:-1] or " ")):
                errors.append(f"Line {number}: invalid label '{text}'")
                continue
            name = text[1:-1]
            if name in labels_seen:
                errors.append(f"Line {number}: label '{name}' already defined "
                              f"on line {labels_seen[name]}")
                continue
            labels_seen[name] = number
            symbols[name] = len(program)      # address of the NEXT instruction
        else:
            program.append((number, text))
    return program


def parse_c(text):
    """Return 16-bit string for a C-instruction, or None if invalid."""
    dest, comp, jump = "", text, ""
    if "=" in comp:
        dest, comp = comp.split("=", 1)
    if ";" in comp:
        comp, jump = comp.split(";", 1)
    if dest not in DEST or comp not in COMP or jump not in JUMP:
        return None
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def second_pass(program, symbols, errors):
    """Translate each instruction to 16 bits. New variables start at RAM 16."""
    out = []
    next_var = 16
    for number, text in program:
        if text.startswith("@"):
            sym = text[1:]
            if sym.isdigit():
                value = int(sym)
                if value > 32767:
                    errors.append(f"Line {number}: address {value} is too large "
                                  f"(max 32767)")
                    continue
            elif SYMBOL_RE.match(sym or " "):
                if sym not in symbols:
                    symbols[sym] = next_var
                    next_var += 1
                value = symbols[sym]
            else:
                errors.append(f"Line {number}: invalid instruction '{text}'")
                continue
            out.append(format(value, "016b"))
        else:
            code = parse_c(text)
            if code is None:
                errors.append(f"Line {number}: invalid instruction '{text}'")
                continue
            out.append(code)
    return out


def assemble(lines):
    symbols = dict(PREDEFINED)
    errors = []
    program = first_pass(lines, symbols, errors)
    binary = second_pass(program, symbols, errors)
    return binary, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py Prog.asm [Prog.hack]")
        return 2
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else re.sub(r"\.asm$", "", src) + ".hack"
    try:
        with open(src) as f:
            lines = f.read().splitlines()
    except OSError as e:
        print(f"Cannot open {src}: {e}")
        return 2

    binary, errors = assemble(lines)
    if errors:
        errors.sort(key=lambda e: int(e.split(":")[0].split()[1]))
        for e in errors:
            print(e)
        print(f"{len(errors)} error(s) - no output written.")
        return 1
    with open(dst, "w") as f:
        f.write("\n".join(binary) + "\n")
    print(f"{src} -> {dst}  ({len(binary)} instructions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
