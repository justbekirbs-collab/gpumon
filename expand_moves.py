import re

path = 'src/data/text/move_names.h'
with open(path, 'r') as f:
    content = f.read()

# 90 unique tech/AI/GPU moves (max 12 chars)
new_moves = [
    "OVERCLOCK", "BITCOIN MINE", "TRAIN AI", "RAY TRACING", "FRAME GEN", 
    "TENSOR SMASH", "WATER COOL", "LIQUID METAL", "THERML THROT", "BLUE SCREEN", 
    "DRIVER CRASH", "RGB BLAZE", "DLSS 3", "FSR 2", "HASH CRACK", 
    "VRAM ERROR", "KERNEL PANIC", "BOTNET", "DDOS ATTACK", "DEEP LEARN",
    "MACHINE LRN", "NEURAL NET", "DATA MINE", "SQL INJECT", "RANSOMWARE",
    "TROJAN HORSE", "MALWARE", "SPYWARE", "PHISHING", "ROOTKIT",
    "FIREWALL", "ENCRYPTION", "DECRYPTION", "BRUTE FORCE", "ZERO DAY",
    "EXPLOIT", "PAYLOAD", "BACKDOOR", "WIREGUARD", "VPN TUNNEL",
    "PROXY SERVER", "PACKET SNIFF", "PORT SCAN", "MAC SPOOF", "IP SPOOF",
    "ARP SPOOF", "MAN IN MID", "DNS POISON", "CACHE MISS", "PAGE FAULT",
    "SEG FAULT", "STACK OVER", "HEAP CORRUPT", "MEM LEAK", "NULL POINTER",
    "RACE COND", "DEADLOCK", "LIVELOCK", "MUTEX LOCK", "SEMAPHORE",
    "THREAD POOL", "ASYNC AWAIT", "PROMISE RES", "CALLBACK", "EVENT LOOP",
    "GARBAGE COL", "JIT COMPILE", "AOT COMPILE", "BYTECODE", "OPCODE",
    "ASSEMBLY", "MACHINE CODE", "MICROCODE", "FIRMWARE", "BIOS UPDATE",
    "UEFI BOOT", "SECURE BOOT", "TPM MODULE", "CPU CACHE", "L1 CACHE",
    "L2 CACHE", "L3 CACHE", "L4 CACHE", "RAM DISK", "SWAP SPACE",
    "SSD TRIM", "HDD DEFRAG", "RAID 0", "RAID 1", "RAID 5"
]

def replace_moves(content, new_moves):
    pattern = r'(\[MOVE_[A-Z0-9_]+\])\s*= _\("([^"]*)"\),'
    matches = re.finditer(pattern, content)
    
    new_content = content
    count = 0
    
    # We want to replace the first 90 matches (ignoring MOVE_NONE which is index 0 usually, but let's just replace from start)
    # Actually, MOVE_NONE is usually 0. Let's start from 1.
    
    # Find all matches
    all_matches = list(matches)
    
    for i, match in enumerate(all_matches):
        if i == 0:
            continue # Skip MOVE_NONE
        if count < len(new_moves):
            # Replace the string in the matched line
            old_line = match.group(0)
            new_line = f'{match.group(1)} = _("{new_moves[count]}"),'
            new_content = new_content.replace(old_line, new_line, 1)
            count += 1
        else:
            break
            
    return new_content

new_content = replace_moves(content, new_moves)

with open(path, 'w') as f:
    f.write(new_content)

print(f"Replaced 90 moves.")
