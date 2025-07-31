def f(x):
    return x**7 + 7.2*x - 8.4

def f_prime(x):
    return 7*x**6 + 7.2

def newton_raphson(initial_guess, tolerance=1e-7, max_iterations=100):
    x_n = initial_guess
    steps = []
    
    for iteration in range(max_iterations):
        f_x_n = f(x_n)
        f_prime_x_n = f_prime(x_n)
        
        # Avoid division by zero
        if f_prime_x_n == 0:
            steps.append(f'Iteration {iteration}: Derivative is zero, stopping iteration.')
            break
        
        x_n1 = x_n - f_x_n / f_prime_x_n
        steps.append(f'Iteration {iteration}: x_n = {x_n}, f(x_n) = {f_x_n}, x_n1 = {x_n1}')
        
        if abs(x_n1 - x_n) < tolerance:
            steps.append(f'Converged to {x_n1} within tolerance after {iteration} iterations.')
            break
        
        x_n = x_n1
    else:
        steps.append('Maximum iterations reached without convergence.')
    
    return x_n, steps

# Initial guess
initial_guess = 1.0
solution, reasoning_steps = newton_raphson(initial_guess)

# Write the steps to a text file
with open('steps.txt', 'w') as file:
    for step in reasoning_steps:
        file.write(step + '\n')

solution