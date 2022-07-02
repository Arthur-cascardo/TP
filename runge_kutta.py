import math as m


# RK-4 method python program

# function to be solved
def f(h, qin):
    r0 = 1
    r1 = 2
    total_height = 4
    cv = 0.5

    alpha = (r1 - r0) / total_height
    den = (m.pi * pow((r0 + alpha * h), 2))
    return ((-cv * m.sqrt(h)) / den) + ((1 / den) * qin)


# RK-4 method
def rk4(x0, y0, xn, n):
    # Calculating step size
    h = (xn - x0) / n

    for i in range(n):
        k1 = h * (f(x0, y0))
        k2 = h * (f((x0 + h / 2), (y0 + k1 / 2)))
        k3 = h * (f((x0 + h / 2), (y0 + k2 / 2)))
        k4 = h * (f((x0 + h), (y0 + k3)))
        k = (k1 + 2 * k2 + 2 * k3 + k4) / 6
        yn = y0 + k
        y0 = yn
        x0 = x0 + h

    return yn