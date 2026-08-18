"""
Replace ALL user-visible 'Pokemon/POKéMON/Pokémon' text with 'GPU' 
ONLY inside string literals. Never touches C identifiers, includes, or comments.
"""
import os
import re
import subprocess

BASE = "/Users/bekirkarakose/Documents/ProjectAlascatra"

# Variants to replace (most specific first)
REPLACEMENTS = [
    ("POKéMON", "GPU"),
    ("POKÉMON", "GPU"),
    ("Pokémon", "GPU"),
    ("pokémon", "GPU"),
    ("POKEMON", "GPU"),
    ("Pokemon", "GPU"),
    ("pokemon", "GPU"),
]

def replace_in_string_literals_c(content):
    """Replace only inside _("...") macros"""
    def replace_in_match(m):
        inner = m.group(1)
        for old, new in REPLACEMENTS:
            inner = inner.replace(old, new)
        return '_("' + inner + '")'
    return re.sub(r'_\("(.*?)"\)', replace_in_match, content, flags=re.DOTALL)

def replace_in_string_literals_inc(content):
    """Replace inside .string "..." and format strings in .inc files"""
    def replace_match(m):
        inner = m.group(1)
        for old, new in REPLACEMENTS:
            inner = inner.replace(old, new)
        return m.group(0)[:m.start(1)-m.start(0)] + inner + '"'
    # Replace inside quoted strings
    result = []
    i = 0
    while i < len(content):
        if content[i] == '"':
            j = i + 1
            while j < len(content) and content[j] != '"':
                if content[j] == '\\':
                    j += 1
                j += 1
            inner = content[i+1:j]
            for old, new in REPLACEMENTS:
                inner = inner.replace(old, new)
            result.append('"' + inner + '"')
            i = j + 1
        else:
            result.append(content[i])
            i += 1
    return ''.join(result)

total_files = 0
total_changes = 0

# 1. src/data/text/*.h — these are ENTIRELY text, replace everything
text_dir = os.path.join(BASE, "src/data/text")
for fname in os.listdir(text_dir):
    if not fname.endswith(".h"):
        continue
    fpath = os.path.join(text_dir, fname)
    with open(fpath, encoding='utf-8', errors='replace') as f:
        content = f.read()
    new = replace_in_string_literals_c(content)
    if new != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new)
        total_files += 1
        print(f"  ✓ {fname}")

# 2. src/strings.c — replace inside _("...") only
strings_c = os.path.join(BASE, "src/strings.c")
with open(strings_c, encoding='utf-8', errors='replace') as f:
    content = f.read()
new = replace_in_string_literals_c(content)
if new != content:
    with open(strings_c, 'w', encoding='utf-8') as f:
        f.write(new)
    total_files += 1
    print(f"  ✓ strings.c")

# 3. data/maps/**/text.inc and scripts.inc — replace inside quoted strings
for root, dirs, files in os.walk(os.path.join(BASE, "data")):
    for fname in files:
        if not fname.endswith(".inc"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, encoding='utf-8', errors='replace') as f:
            content = f.read()
        new = replace_in_string_literals_inc(content)
        if new != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new)
            total_files += 1
            rel = os.path.relpath(fpath, BASE)
            print(f"  ✓ {rel}")

# 4. src/data/easy_chat/*.h — easy chat word lists (user-visible)
easy_chat_dir = os.path.join(BASE, "src/data/easy_chat")
for fname in os.listdir(easy_chat_dir):
    if not fname.endswith(".h"):
        continue
    fpath = os.path.join(easy_chat_dir, fname)
    with open(fpath, encoding='utf-8', errors='replace') as f:
        content = f.read()
    new = replace_in_string_literals_c(content)
    if new != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new)
        total_files += 1
        print(f"  ✓ easy_chat/{fname}")

# 5. src/data/pokemon/pokedex_text*.h — pokedex descriptions
poke_dir = os.path.join(BASE, "src/data/pokemon")
for fname in os.listdir(poke_dir):
    if not (fname.startswith("pokedex_text") and fname.endswith(".h")):
        continue
    fpath = os.path.join(poke_dir, fname)
    with open(fpath, encoding='utf-8', errors='replace') as f:
        content = f.read()
    new = replace_in_string_literals_c(content)
    if new != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new)
        total_files += 1
        print(f"  ✓ pokemon/{fname}")

print(f"\n=== Done! Patched {total_files} files ===")
