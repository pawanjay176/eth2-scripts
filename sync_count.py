import requests
import json
import sys
from remerkleable.bitfields import Bitvector

BLOCK_URL = "http://localhost:9001/eth/v1/beacon/blocks/"
START_BLOCK = 17
END_BLOCK = 1355


def hex_to_bitvector(s):
    return Bitvector[32].decode_bytes(bytes.fromhex(s[2:]))

total = 0

for block_num in range(START_BLOCK, END_BLOCK+1):
    r = requests.get(BLOCK_URL + str(block_num)).json()
    sync_com_bitvector = hex_to_bitvector(r["data"]['message']["body"]["sync_aggregate"]["sync_committee_bits"])
    count = sum(iter(sync_com_bitvector))
    if count != 32:
        print("Sync count for block ", block_num,": ", count)
        total+=1
print(total)