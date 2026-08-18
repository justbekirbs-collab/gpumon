import re

path = 'src/data/items.h'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('.name = _("MASTER BALL")', '.name = _("JustBekirRig")')
content = content.replace('.name = _("POKé BALL")', '.name = _("RIG")')
content = content.replace('.name = _("GREAT BALL")', '.name = _("SUPER RIG")')
content = content.replace('.name = _("ULTRA BALL")', '.name = _("ULTRA RIG")')
content = content.replace('.name = _("SAFARI BALL")', '.name = _("SAFARI RIG")')
content = content.replace('.name = _("NET BALL")', '.name = _("NET RIG")')
content = content.replace('.name = _("DIVE BALL")', '.name = _("DIVE RIG")')
content = content.replace('.name = _("NEST BALL")', '.name = _("NEST RIG")')
content = content.replace('.name = _("REPEAT BALL")', '.name = _("REPEAT RIG")')
content = content.replace('.name = _("TIMER BALL")', '.name = _("TIMER RIG")')
content = content.replace('.name = _("LUXURY BALL")', '.name = _("LUXURY RIG")')
content = content.replace('.name = _("PREMIER BALL")', '.name = _("PREMIER RIG")')

with open(path, 'w') as f:
    f.write(content)
