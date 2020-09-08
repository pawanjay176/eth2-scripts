import requests
import time

VALIDATORS = [6686, 6687, 6690, 6717, 6718, 6719, 6720, 6721]

# Time intervals for checking missed attestations in seconds
INTERVAL = 300

BASE_URL = "https://beaconcha.in/api/v1/validator/"

def check():
    while True:
        for validator in VALIDATORS:
            url = BASE_URL + str(validator) + "/attestations"
            data = requests.get(url).json()['data']
            # Check only last 3 epochs
            for i in range(1, 3):
                if data[i]['status'] == 0:
                    print("validator:", validator, " missed attestation: ", data[i]['attesterslot'])
                if data[i]['attesterslot'] % 32 == 0 or data[i]['attesterslot'] % 32 == 1:
                    print("validator: ", validator, "on epoch boundary: ", data[i]['epoch'])
        print("Completed check, sleeping\n\n")
        time.sleep(INTERVAL)
check()
