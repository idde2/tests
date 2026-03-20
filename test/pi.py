from decimal import Decimal, getcontext
import math

def pi_digits(n):
    getcontext().prec = n + 10

    C = 426880 * Decimal(10005).sqrt()

    def chudnovsky_term(k):
        numerator = Decimal(math.factorial(6*k)) * (13591409 + 545140134*k)
        denominator = Decimal(math.factorial(3*k)) * (Decimal(math.factorial(k))**3) * Decimal(640320)**(3*k)
        return Decimal((-1)**k) * numerator / denominator

    terms = n // 14 + 1

    series_sum = Decimal(0)
    for k in range(terms):
        series_sum += chudnovsky_term(k)

    pi = C / series_sum

    return str(pi)[:n+2]


if __name__ == "__main__":
    stellen = int(input("Wie viele Nachkommastellen von Pi möchtest du? "))
    print(pi_digits(stellen))
