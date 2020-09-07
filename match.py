import requests
import json
import sys
from remerkleable.bitfields import Bitlist

GET_BLOCK_URL = "http://localhost:5052/beacon/block?slot="
GET_COM_URL = "http://localhost:5052/beacon/committees?epoch="

# Convert hex to bitlist
def hex_to_bitlist(s):
    return Bitlist[2048].decode_bytes(bytes.fromhex(s[2:]))

def get_committee_at_index(resps, slot, index):
    for resp in resps:
        if resp["slot"] == slot and resp["index"] == index:
            return resp["committee"]

def get_vals_from_committee(aggregate_bitlist: Bitlist, com_array):
    vals = []
    for i in range(aggregate_bitlist.length()):
        if aggregate_bitlist.get(i):
            vals.append(com_array[i])
    return vals

def get_block(slot):
    r = requests.get(GET_BLOCK_URL + str(slot))
    resp = r.json()
    attestations = resp['beacon_block']['message']['body']['attestations']

    com = requests.get(GET_COM_URL + str(slot // 32)).json()
    for attestation in attestations:
        data = attestation['data']
        print("slot", data['slot'])
        print("committee index", data['index'])
        print("block root", data['beacon_block_root'])
        aggregate_bits = hex_to_bitlist(attestation['aggregation_bits'])
        com_array = get_committee_at_index(com, data['slot'], data['index'])
        print("validators attested", get_vals_from_committee(aggregate_bits, com_array))
        print("\n\n")

get_block(int(sys.argv[1]))
