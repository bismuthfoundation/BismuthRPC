"""
Simple test script to test the rpckeys module
"""

import rpckeys


# Create object
my_key = rpckeys.key()

#Ask for a new set
# This takes some time, has to gather some entropy
my_key.generate()

# Display
print("New key:",my_key.as_dict)

# A test only IV, do not use irl
IV = 16 * '\x00'
passphrase = "Test Only"

# This return my_key.as_dict
crypted = my_key.crypt(IV,passphrase)

print("Crypted",crypted)

# This return my_key.as_dict
clear = my_key.decrypt(IV,passphrase)

print("Clear again",clear)

