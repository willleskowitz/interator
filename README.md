# interator
Module for integer sequence generation and related conditional tests.

## Contents
### Fibonacci Sequence

| **Function**                                  | **Description**                                                                            |
|-----------------------------------------------|--------------------------------------------------------------------------------------------|
| `fibonacci_stream(start = (0,1))`             | Yield the next Fibonacci number starting with F(0)                                         |
| `negafibonacci_stream(start = (0,1))`         | Yield the next Fibonacci number in the negative index starting with F(0)                   |
| `nth_fibonacci(n, start = (0, 1))`            | Given an index n, find F(n)                                                                |
| `lucas_stream(P = 2, Q = -1, start = (0, 1))` | Yield the next number in the in the (P,−Q)-Lucas sequence starting with U<sub>0</sub>(P,Q) |
| `is_fibonacci(n, start=(0,1))`                | Determine if n is within the Fibonacci sequence                                            |
| `is_lucas(n, P = 2, Q = -1, start = (0, 1))`  | Determine if n is within the (P,−Q)-Lucas sequence                                         |

#### Generalizations
By default, `fibonacci_stream`, `negafibonacci_stream`, `nth_fibonacci`, and `is_fibonacci` work with the Fibonacci numbers and `lucas_stream` and `is_lucas` work with the Pell numbers. However, by changing start, any generalization of the these sequences can be generated. Here are some common examples:

```python
import interator

stop = 10
numbers = {'Lucas' : (2, 1),
           'Tribonacci' : (0, 0, 1),
           'Tetranacci' : (0, 0, 0, 1)}


for name, start in numbers.items():
    print('%s numbers:' % name)
    for i, n in enumerate(interator.fibonacci_stream(start=start)):
        print(n, end = ' ')
        if i == stop:
            print('\n')
            break
```

Please note the Lucas numbers should not be confused with the Lucas sequence. The Lucas numbers are a specific example of the Lucas sequence.

## Licensing
This project is licensed under the MIT License.
