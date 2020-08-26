#!/usr/bin/env python
"""Module for integer sequence generation and related conditional tests."""

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
    skip = tuple([1 if n % c in mod else 0 for n in range(start, start + c, 2)])
            
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
    '''Yield the next number in the Fibonacci sequence starting with F(0).
    
    Parameters
    ----------
    start : tuple or list of intengers, optional
        Integers to initialize the Fibonacci sequence. By changing start, other 
        generalizations of the Fibonacci numbers can be generated. For instance, 
        with start = (0, 0, 1), the Tribonacci numbers will be generated. The 
        default is (0, 1). 
    
    Yields
    ------
    int
        After yielding the initial integers in start, the next value is the sum
        of the preceding values. The length of start determines how many  
        preceding values will be summed to generate the next value.
    '''
    for n in start:
        yield n
        
    last = collections.deque(start, len(start))
    
    while True:
        next_n = sum(last)
        yield next_n
        last.append(next_n)
            

def negafibonacci_stream(start = (0, 1)):
    '''Yield the next number in the negaFibonacci sequence staring with F(0).
    
    Parameters
    ----------
    start : tuple or list of integers, optional
        Integers to initialize the negaFibonacci sequence. By changing start, 
        other generalizations of the negaFibonacci numbers can be generated. For
        instance, with start = (0, 0, 1), the negaTribonacci numbers will be 
        generated. The default is (0, 1). 
    
    Yields
    ------
    int
        After yielding F(0), the sequence will proceed into the negative index
        with F(-1), F(-2), and so on. The length of start determines how many  
        preceding values will be subtracted to generate the next value.
    '''
    yield start[0]
    
    last = collections.deque(start, len(start))
    
    while True:
        next_n = last[-1] + last[-1] - sum(last)
        yield next_n
        last.appendleft(next_n)  
        

def pell_stream(start = (0, 1)):
    '''Yield the next Pell number starting with P(0).

    Parameters
    ----------
    start : tuple or list of integers, optional
        Integers to initialize the Pell sequence. The length of start must equal
        two. By changing start, other generalizations of the Pell numbers can 
        be generated. For instance, Pell–Lucas numbers can be generated with 
        start = (2, 2). The default is (0, 1).

    Yields
    ------
    int
        After yielding the initial integers in start, the next value is the sum
        of twice the previous Pell number and the Pell number before that.

    '''
    for n in start:
        yield n

    n1, n2 = start
    while True:
        next_n = n1 + n2 + n2
        yield next_n
        n1, n2 = n2, next_n
        

## TESTS
def is_prime(n):
    '''Test the primality of n by checking potential prime factors of n.

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
    '''The Miller-Rabin Primality Test. Probabilistically determine if n is prime.

    Parameters
    ----------
    n : int
        n is the number to be tested.
    k : int, optional
        k determines the test's accuracy. It describes the number of iterations
        of the test to be performed. The default is 8.

    Returns
    -------
    bool
        Return True if n passes the Miller-Rabin primality test and False 
        otherwise.

    '''
    if n < 2 or n % 1 != 0:
        return False
    
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
    '''Test if n is a composite number by checking potential prime factors of n.

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
    
    if n < 1 or n % 1 != 0:
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

def perfect_square(x):
    # FIXME! Test for perfect square without taking sqaure? Needs larger int processing
    sqaure = int(x**0.5)
    return sqaure * sqaure == x

def is_fibonacci(n):
    '''Test if n is a Fibonacci number.
    
    Parameters
    ----------
    n : int
        n is the number to be tested.

    Returns
    -------
    bool
        Return True if n is a positive Fibonacci number and False otherwise.

    '''
    if n < 0:
        return False
        
    return perfect_square(5*n*n + 4) or perfect_square(5*n*n - 4)

   
def is_pell(n, start = (0, 1)):
    '''Test if n is a Pell number.

    Parameters
    ----------
    n : int
        n is the number to be tested.
    start : tuple or list of integers, optional
        Integers to initialize the Pell sequence. The length of start must equal
        two. By changing start, other generalizations of the Pell numbers can 
        be generated. For instance, Pell–Lucas numbers can be generated with 
        start = (2, 2). The default is (0, 1).

    Returns
    -------
    bool
        Return True if n is a Pell number and False otherwise.

    '''
    for pell in pell_stream(start=start):
        if n == pell:
            return True
        if pell > n:
            return False
   

## INDEX
def nth_fibonacci(n, start = (0, 1)):
    '''Return the Fibonacci number at index F(n).
    
    Parameters
    ----------
    n : int, 
        Index of the Fibonacci number.
    
    start : tuple or list of intengers, optional
        Integers to initialize the Fibonacci sequence. By changing start, other 
        generalizations of the Fibonacci numbers can be found. For instance, 
        with start = (0, 0, 1), the Tribonacci number at index n will be 
        returned. The default is (0, 1). 
    
    Yields
    ------
    int
        After yielding the initial integers in start, the next value is the sum
        of the preceding values. The length of start determines how many  
        preceding values will be summed to generate the next value.
    '''
    if n < len(start):
        return start[n]
    
    adjust = len(start) - 2    
    a_str = []
    for i in range(-1, len(start) - 1):
        if i == -1:
            a_str.append(' '.join('1' for _ in range(len(start))))
        else:
            a_str.append(' '.join('1' if i == j else '0' for j in range(len(start))))
    
    a = np.matrix('; '.join(a_str), dtype=np.object)
    b = np.matrix('; '.join([str(i) for i in start]), dtype=np.object)     
    
    return np.matmul(np.linalg.matrix_power(a, n - adjust), b).item(0)
        
     
