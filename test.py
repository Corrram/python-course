def decrement(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    return n - "1"


result = decrement(5)
