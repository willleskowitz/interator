#!/usr/bin/env python
'''Module for integer sequence generation and related conditional tests.'''

import math
import itertools as it
import random
import collections
import numpy as np


## SEQUENCE GENERATORS
def prime_stream():
    '''Yield the next prime number starting with 2.'''
    start = 13
    c = 2*3*5*7*11
    yield 2; yield 3; yield 5; yield 7; yield 11

    sieve = {}
    mod = frozenset(i for i in range(c) if math.gcd(i, c) == 1)
    skip = tuple([1 if n % c in mod else 0 for n in range(start, start+c, 2)])

    for n in it.compress(it.count(start, 2), it.cycle(skip)):
        if n not in sieve:
            sieve[n*n] = n; yield n
        else:
            prime = sieve.pop(n)
            m = n + 2*prime
            while m in sieve or m % c not in mod:
                m += 2*prime
            sieve[m] = prime


def composite_stream():
    '''Yield the next composite number starting with 1.'''
    primes = prime_stream()
    next_prime = next(primes)

    for n in it.count(1):
        if n != next_prime:
            yield n
        else:
            next_prime = next(primes)


def polygonal_stream(s):
    '''Yield the next s-gonal number starting with 1.

    Parameters
    ----------
    s : int
        s is the number of sides in the polygon.

    Yields
    ------
    int
        Yield P(s, 1), P(s, 2), P(s, 3)... and so on.
    '''
    for n in it.count(1):
        yield int(((s - 2)*n*n - (s - 4)*n) / 2)


def fibonacci_stream(start = (0, 1)):
    '''Yield the next number in the Fibonacci sequence.

    Parameters
    ----------
    start : tuple or list of intengers, optional
        Integers to initialize the Fibonacci sequence. By changing
        start, other generalizations of the Fibonacci numbers can be
        generated. For instance, with start = (0, 0, 1), the Tribonacci
        numbers will be generated. The default is (0, 1).

    Yields
    ------
    int
        After yielding the initial integers in start, the next value is
        the sum of the preceding values. The length of start determines
        how many preceding values will be summed to generate the next
        value.
    '''
    for n in start:
        yield n

    last = collections.deque(start, len(start))

    while True:
        next_n = sum(last)
        yield next_n
        last.append(next_n)


def negafibonacci_stream(start = (0, 1)):
    '''Yield the next number in the negaFibonacci sequence.

    Parameters
    ----------
    start : tuple or list of integers, optional
        Integers to initialize the negaFibonacci sequence. By changing
        start, other generalizations of the negaFibonacci numbers can
        be generated. For instance, with start = (0, 0, 1), the
        negaTribonacci numbers will be generated. The default is
        (0, 1).

    Yields
    ------
    int
        After yielding F(0), the sequence will proceed into the
        negative index with F(-1), F(-2), and so on. The length of
        start determines how many preceding values will be subtracted
        to generate the next value.
    '''
    yield start[0]

    last = collections.deque(start, len(start))

    while True:
        next_n = last[-1] + last[-1] - sum(last)
        yield next_n
        last.appendleft(next_n)


def lucas_stream(P = 2, Q = -1, start = (0, 1)):
    '''Yield the next number in the (P,−Q)-Lucas sequence.

    Parameters
    ----------
    P : int, optional
        Fixed integer coefficient defining the sequence. By changing P,
        other generalizations of the Lucas sequence can be generated.
        For instance, the 3-Fibonacci sequence can be generated with
        P = 3. The default is 2.
    Q : int, optional
        Fixed integer coefficient defining the sequence. By changing Q,
        other generalizations of the Lucas sequence can be generated.
        For instance, the Jacobsthal numbers can be generated with
        P = 1 and Q = -2. The default is -1.
    start : tuple or list of integers, optional
        Integers to initialize the Lucas sequence. The length of start
        must equal two. By changing start, other generalizations of the
        Lucas sequence can be generated. For instance, Pell–Lucas
        numbers can be generated with start = (2, 2). The default is (0, 1).

    Yields
    ------
    int
        Yields U(0), U(1), ... U(n) where U(n) is defined by

        U(0) = start[0]
        U(1) = start[1]
        U(n + 2) = P*U(n + 1) − Q*U(n)

        By default, the Pell numbers will be generated.
    '''
    for n in start:
        yield n

    n1, n2 = start
    while True:
        next_n = P*n2 - Q*n1
        yield next_n
        n1, n2 = n2, next_n


## TESTS
def is_prime(n):
    '''Test the primality of n by checking potential prime factors.

    Parameters
    ----------
    n : int
        n is the number to be tested.

    Returns
    -------
    bool
        Return True if n is a prime number and False otherwise.

    '''
    if n == 2:
        return True

    if n < 2 or n % 1 != 0:
        return False

    stop = n ** 0.5
    for prime in prime_stream():
        if n % prime == 0:
            return False
        if stop < prime:
            break
    return True


def miller_rabin(n, k = 8):
    '''Perform the Miller-Rabin Primality Test on n.

    Parameters
    ----------
    n : int
        n is the number to be probabilistically tested.
    k : int, optional
        k determines the test's accuracy. It describes the number of
        iterations of the test to be performed. The default is 8.

    Returns
    -------
    bool
        Return True if n passes the Miller-Rabin primality test and
        False otherwise.

    '''
    if n < 2 or n % 1 != 0:
        return False

    if n in (2, 3):
        return True

    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1: continue

        cont = False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: cont = True; break

        if cont: continue

        return False

    return True


def is_composite(n):
    '''Test if n is a composite by checking potential prime factors.

    Parameters
    ----------
    n : int
        n is the number to be tested.

    Returns
    -------
    bool
        Return True if n is a composite number and False otherwise.
    '''
    if n == 1:
        return True

    if n < 1 or n % 1 != 0 or n == 2:
        return False

    stop = n ** 0.5
    for prime in prime_stream():
        if n % prime == 0:
            return True
        if stop < prime:
            break
    return False


def is_polygonal(n, s):
    '''Test if n is an s-gonal number.

    Parameters
    ----------
    n : int
        n is the number to be tested.
    s : int
        s is the number of sides in the polygon.

    Returns
    -------
    bool
        Return True if n is an s-gonal number and False otherwise.

    '''
    numerator = (8*n*(s - 2) + (s - 4)**2)**0.5 + s - 4
    denominator = 2*(s - 2)
    return (numerator / denominator) % 1 == 0


def is_fibonacci(n, start = (0, 1)):
    '''Test if n is a Fibonacci number.

    Parameters
    ----------
    n : int
        n is the number to be tested.
    start : tuple or list of intengers, optional
        Integers to initialize the Fibonacci sequence. By changing
        start, other generalizations of the Fibonacci numbers can be
        generated. For instance, with start = (0, 0, 1), the Tribonacci
        numbers will be generated. The default is (0, 1).

    Returns
    -------
    bool
        Return True if n is a positive Fibonacci number and False
        otherwise.

    '''
    if n in start:
        return True

    if n < max(start):
        return False

    if n <= nth_fibonacci(1475) and tuple(start) == (0, 1):
        phi = 0.5 + 0.5 * math.sqrt(5.0)
        a = phi * n
        return n == 0 or abs(round(a) - a) < 1.0 / n

    for fib in fibonacci_stream(start=start):
        if n == fib:
            return True
        if fib > n:
            return False


def is_lucas(n, P = 2, Q = -1, start = (0, 1)):
    '''Test if n is within the (P,−Q)-Lucas sequence.

    Parameters
    ----------
    U(n + 2) = P*U(n + 1) − Q*U(n)

    P : int, optional
        Fixed integer coefficient defining the sequence. By changing P,
        other generalizations of the Lucas sequence can be generated.
        For instance, the 3-Fibonacci sequence can be generated with
        P = 3. The default is 2.
    Q : int, optional
        Fixed integer coefficient defining the sequence. By changing Q,
        other generalizations of the Lucas sequence can be generated.
        For instance, the Jacobsthal numbers can be generated with
        P = 1 and Q = -2. The default is -1.
    start : tuple or list of integers, optional
        Integers to initialize the Lucas sequence. The length of start
        must equal two. By changing start, other generalizations of the
        Lucas sequence can be generated. For instance, Pell–Lucas
        numbers can be generated with start = (2, 2). The default is
        (0, 1).

    Returns
    -------
    bool
        Return True if n is within the within the (P,−Q)-Lucas sequence
        and False otherwise.

    '''
    for lucas in lucas_stream(P = P, Q = Q, start = start):
        if n == lucas:
            return True
        if lucas > n:
            return False


## INDEX
def nth_fibonacci(n, start = (0, 1)):
    '''Return the Fibonacci number at index n or F(n).

    Parameters
    ----------
    n : int,
        Index of the Fibonacci number. Negative indexes are supported.
    start : tuple or list of intengers, optional
        Integers to initialize the Fibonacci sequence. By changing
        start, other generalizations of the Fibonacci numbers can be
        found. For instance, with start = (0, 0, 1), the Tribonacci
        number at index n will be returned. The default is (0, 1).

    Returns
    -------
    int
        Return F(n).

    '''
    if 0 <= n < len(start):
        return start[n]

    elif n > 0:
        adjust = len(start) - 1

        a_str = []
        for i in range(0, len(start)):
            if i == 0:
                a_str.append(' '.join('1' for j in start))
            else:
                a_lst = ['1' if i-1 == j else '0' for j in range(len(start))]
                a_str.append(' '.join(a_lst))

        a = np.matrix('; '.join(a_str), dtype=np.object)
        b_lst = [str(i) for i in start[::-1]]
        b = np.matrix('; '.join(b_lst),dtype=np.object)

        return np.matmul(np.linalg.matrix_power(a, n - adjust), b).item(0)

    elif tuple(start) == (0, 1):
        if n % 2 == 0:
            c = -1
        else:
            c = 1

        return c*nth_fibonacci(abs(n), start=start)

    elif tuple(start) == (2, 1):
        if n % 2 == 1:
            c = -1
        else:
            c = 1
        return c*nth_fibonacci(abs(n), start=start)

    else:
        for i, f in enumerate(negafibonacci_stream(start=start)):
            if i == abs(n):
                return f
