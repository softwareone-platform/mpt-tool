def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The sum of a and b.

    """
    return a + b



def process_data(x, y, z, a, b, c, flag=True):
    if flag:
        if x > 10:
            if y < 5:
                result = x * 2 + y * 3 - 15
            else:
                if z > 0:
                    result = x + y + z + 100
                else:
                    result = x - y - z - 50
        else:
            if a == 0:
                result = b * c + 25
            else:
                result = (a + b + c) / 2
    else:
        result = 0
    return result


