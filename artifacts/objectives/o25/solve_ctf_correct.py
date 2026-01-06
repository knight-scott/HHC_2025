import random
import binascii

# Mountain data from constants
mountains = {
    'Mount Snow': {
        'encoded_flag': b'\x90\x00\x1d\xbc\x17b\xed6S"\xb0<Y\xd6\xce\x169\xae\xe9|\xe2Gs\xb7\xfdy\xcf5\x98',
        'height': 3586,
    },
    'Aspen': {
        'encoded_flag': b'U\xd7%x\xbfvj!\xfe\x9d\xb9\xc2\xd1k\x02y\x17\x9dK\x98\xf1\x92\x0f!\xf1\\\xa0\x1b\x0f',
        'height': 11211,
    },
    'Whistler': {
        'encoded_flag': b'\x1cN\x13\x1a\x97\xd4\xb2!\xf9\xf6\xd4#\xee\xebh\xecs.\x08M!hr9?\xde\x0c\x86\x02',
        'height': 7156,
    },
    'Mount Baker': {
        'encoded_flag': b'\xac\xf9#\xf4T\xf1%h\xbe3FI+h\r\x01V\xee\xc2C\x13\xf3\x97ef\xac\xe3z\x96',
        'height': 10781,
    },
    'Mount Norquay': {
        'encoded_flag': b'\x0c\x1c\xad!\xc6,\xec0\x0b+"\x9f@.\xc8\x13\xadb\x86\xea{\xfeS\xe0S\x85\x90\x03q',
        'height': 6998,
    },
    'Mount Erciyes': {
        'encoded_flag': b'n\xad\xb4l^I\xdb\xe1\xd0\x7f\x92\x92\x96\x1bq\xca`PvWg\x85\xb21^\x93F\x1a\xee',
        'height': 12848,
    },
    'Dragonmount': {
        'encoded_flag': b'Z\xf9\xdf\x7f_\x02\xd8\x89\x12\xd2\x11p\xb6\x96\x19\x05x))v\xc3\xecv\xf4\xe2\\\x9a\xbe\xb5',
        'height': 16282,
    }
}

mountain_width = 1000

def get_treasure_locations(mountain_name, height):
    """Replicate GetTreasureLocations algorithm from the bytecode"""
    locations = {}
    
    # Seed with CRC32 of mountain name (line 238)
    random.seed(binascii.crc32(mountain_name.encode('utf-8')))
    
    prev_height = height
    prev_horiz = 0
    
    # Generate 5 treasures (line 241)
    for i in range(5):
        e_delta = random.randint(200, 800)
        h_delta = random.randint(int(0 - e_delta / 4), int(e_delta / 4))
        
        # Store location
        treasure_height = prev_height - e_delta
        treasure_horiz = prev_horiz + h_delta
        locations[treasure_height] = treasure_horiz
        
        prev_height = treasure_height
        prev_horiz = treasure_horiz
    
    return locations

def calculate_treasure_values(mountain_name, height):
    """Calculate treasure values as they would be collected in the game"""
    locations = get_treasure_locations(mountain_name, height)
    treasure_list = []
    
    # From line 380: treasure_value = row * mountain_width + horiz_offset
    for row, horiz in locations.items():
        treasure_value = row * mountain_width + horiz
        treasure_list.append(treasure_value)
    
    return treasure_list

def decode_flag(encoded_flag, treasure_list):
    """Decode flag using the SetFlag algorithm"""
    # Calculate product (lines 304-306)
    product = 0
    for treasure_val in treasure_list:
        product = (product << 8) ^ treasure_val
    
    # Seed random (line 307)
    random.seed(product)
    
    # Decode (lines 310-312)
    decoded = []
    for byte in encoded_flag:
        r = random.randint(0, 255)
        decoded.append(chr(byte ^ r))
    
    flag_text = 'Flag: %s' % ''.join(decoded)
    return flag_text

# Try all mountains and find the real flag
print("="*70)
print("SOLVING: FreeSki CTF Challenge")
print("="*70)
print("\nTrying each mountain to find the valid flag...\n")

for name, data in mountains.items():
    print(f"{name}:")
    treasure_list = calculate_treasure_values(name, data['height'])
    print(f"  Treasures: {treasure_list}")
    flag = decode_flag(data['encoded_flag'], treasure_list)
    print(f"  {flag}")
    
    # Check if this looks like a real flag
    flag_lower = flag.lower()
    if any(keyword in flag_lower for keyword in ['flare', '@flare', 'flareon', '{', '}']):
        print(f"  >>> THIS IS LIKELY THE REAL FLAG! <<<")
    print()
