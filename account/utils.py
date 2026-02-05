import hashlib 
# hexdigest() converts raw binary hash bytes into a human-readable hexadecimal string.
def hash_value(value):
    return hashlib.sha256( value.encode() ).hexdigest()

import random
def genrate_otp():
    
    return "".join( random.choice( "0123456789" ) for _ in range(6) )

print( genrate_otp() )