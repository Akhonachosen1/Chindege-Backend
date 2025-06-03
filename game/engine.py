import hashlib
import random
from decimal import Decimal, getcontext

getcontext().prec = 8
HOUSE_EDGE = Decimal('0.02')

def generate_crash_point(server_seed, client_seed):
    combined = f"{server_seed}-{client_seed}"
    hash_result = hashlib.sha256(combined.encode()).hexdigest()
    hash_value = int(hash_result[:8], 16)
    random_value = Decimal(hash_value) / Decimal(0xffffffff)

    # Game logic with house edge
    crash_point = Decimal(1) / (Decimal(1) - (Decimal(1 - HOUSE_EDGE) * random_value))
    crash_point = max(crash_point, Decimal('1.01'))
    return float(crash_point.quantize(Decimal('0.01')))
