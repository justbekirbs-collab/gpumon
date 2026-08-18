import re

path = 'src/data/text/move_names.h'
with open(path, 'r') as f:
    content = f.read()

def truncate(match):
    name = match.group(2)
    if len(name) > 12:
        name = name[:12]
    return f'{match.group(1)} = _("{name}"),'

new_content = re.sub(r'(\[MOVE_[A-Z0-9_]+\])\s*= _\("([^"]+)"\),', truncate, content)

with open(path, 'w') as f:
    f.write(new_content)

print("Fixed moves.")
