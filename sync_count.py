import requests
import json
import sys
from remerkleable.bitfields import Bitvector

BLOCK_URL = "http://localhost:5052/eth/v1/beacon/blocks/"
START_BLOCK = 321
END_BLOCK = 1355


def pubkey_to_indices(f):
    current_sync_committee_indices = list()
    
    vals = requests.get("http://localhost:5052/eth/v1/beacon/states/320/validators").json()["data"]
    d = {i["validator"]["pubkey"]: i["index"] for i in vals}

    with open(f, "r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.strip()
            current_sync_committee_indices.append(d[line])
    return current_sync_committee_indices



def hex_to_bitvector(s):
    return Bitvector[512].decode_bytes(bytes.fromhex(s[2:]))

total = 0

current_sync_committee_indices = pubkey_to_indices("/home/pawan/eth2/lighthouse/sync_committee1.txt")

l = list()

for block_num in range(START_BLOCK, END_BLOCK+1):
    r = requests.get(BLOCK_URL + str(block_num)).json()
    if "data" in r:
        proposer = r["data"]["message"]["proposer_index"]
        sync_com_bitvector = hex_to_bitvector(r["data"]['message']["body"]["sync_aggregate"]["sync_committee_bits"])
        count = [current_sync_committee_indices[i] for (i, bit) in enumerate(iter(sync_com_bitvector)) if bit == False]
        l.append((int(proposer), len(count)))

from statistics import median, mean

l.sort(key=lambda x: x[1], reverse=True)
d = {0: [], 2000: [], 4000: [], 6000: [], 8000: []}
for i in l:
    num = i[0]
    count = i[1]
    if 0 < num < 2000:
        d[0].append(count)
    elif 2000 < num < 4000:
        d[2000].append(count)
    elif 4000 < num < 6000:
        d[4000].append(count)
    elif 6000 < num < 8000:
        d[6000].append(count)
    elif 8000 < num < 10000:
        d[8000].append(count)
    
for (k, v) in d.items():
    print(k, mean(v), median(v), len(v))
