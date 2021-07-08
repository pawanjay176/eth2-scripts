import requests
import json
import sys
from remerkleable.bitfields import Bitvector

BLOCK_URL = "http://localhost:5052/eth/v1/beacon/blocks/"

def hex_to_bitvector(s):
    return Bitvector[512].decode_bytes(bytes.fromhex(s[2:]))

# Return number of set bits in sync aggregate for block at given slot
# Returns 0 if slot is skipped.
def sync_aggregate_count(slot):
    r = requests.get(BLOCK_URL + str(slot)).json()
    if "data" in r:
        sync_com_bitvector = hex_to_bitvector(r["data"]['message']["body"]["sync_aggregate"]["sync_committee_bits"])
        count = sum(iter(sync_com_bitvector))
        return count
    else:
        return 0

def index_to_client(i):
    if 0 <= i < 500 or 1000 <= i < 1500 or 5000 <= i < 5500 or 8000 <= i < 10000:
        return "Lighthouse"
    elif 500 <= i <= 1000 or 1500 <= i < 2000 or 5500 <= i < 8000:
        return "Teku"
    elif 2000 <= i < 4000:
        return "Prysm"
    elif 4000 <= i < 5000:
        return "Nimbus"
    else:
        return "Unknown"

def pubkey_to_indices(f):
    current_sync_committee_indices = list()
    
    vals = requests.get("http://localhost:5052/eth/v1/beacon/states/320/validators").json()["data"]
    d = {i["validator"]["pubkey"]: int(i["index"]) for i in vals}

    with open(f, "r") as r:
        lines = r.readlines()
        for line in lines:
            line = line.strip()
            current_sync_committee_indices.append(d[line])
    return current_sync_committee_indices

d = dict() 

def process_logs(logs):
    import json
    for log in logs:
        json_log = json.loads(log)
        if json_log["msg"] == "Stored unaggregated sync committee message":
            validator_index = int(json_log["index"])
            subnet_id = int(json_log["subnet_id"])
            slot = json_log["slot"]
            try:
                # d[slot].append((validator_index, subnet_id))
                d[slot].append(validator_index)
            except:
                d[slot] = list()
                # d[slot].append((validator_index, subnet_id))
                d[slot].append(validator_index)


current_sync_committee_indices = pubkey_to_indices("/home/pawan/eth2/lighthouse/sync_committee1.txt")

import sys

with open(sys.argv[1], "r") as f:
    logs = f.readlines()
    process_logs(logs)



for (slot, data) in d.items():
    not_received = list()
    for member in current_sync_committee_indices:
        if member not in data:
            not_received.append(member)
    clients = dict()
    for i in not_received:
        try:
            clients[index_to_client(i)] += 1
        except:
            clients[index_to_client(i)] = 1

    print("slot ", slot, ", unreceived: ", clients, ", received logs: ", len(data), ", sync_aggregate", sync_aggregate_count(slot))