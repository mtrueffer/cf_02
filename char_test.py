import unicodedata

def print_unicode_block(start, end, columns=16):
    for code in range(start, end):
        ch = chr(code)
        name = unicodedata.name(ch, "Unknown")
        print(f"{code:04X} {ch} ", end="")
        if (code - start + 1) % columns == 0:
            print()
    print("\n")

print("Box Drawing (U+2500-U+257F)")
print_unicode_block(0x2500, 0x257F)

print("Block Elements (U+2580-U+259F)")
print_unicode_block(0x2580, 0x259F)

print("Geometic Shapes (U+25A0-U+25FF)")
print_unicode_block(0x25A0, 0x25FF)

print("Arrows (U+2190-U+21FF)")
print_unicode_block(0x2190, 0x21FF)
