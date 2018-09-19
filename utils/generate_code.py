import random


def generate_code():
    verification_code = []
    for i in range(1, 5):
        verification_code.append(random.randint(0, 9))
    code = ''.join(str(e) for e in verification_code)
    return code
