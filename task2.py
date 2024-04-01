import multiprocessing


def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize_parallel(numbers):
    with multiprocessing.Pool() as pool:
        result = pool.map(factorize, numbers)
    return result


if __name__ == "__main__":
    a, b, c, d = factorize_parallel([128, 255, 99999, 10651060])
    print(a)
    print(b)
    print(c)
    print(d)
