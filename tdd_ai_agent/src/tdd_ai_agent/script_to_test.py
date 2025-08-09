# exemplo_codigo.py

def soma(a, b):
    """Retorna a soma de dois números."""
    return a + b

def divide(a, b):
    """Divide a pelo b, levanta ValueError se b for zero."""
    if b == 0:
        raise ValueError("Divisor não pode ser zero.")
    return a / b

def eh_par(num):
    """Retorna True se o número for par, False caso contrário."""
    return num % 2 == 0

if __name__ == "__main__":
    print(soma(10, 5))       # Esperado: 15
    print(divide(10, 2))     # Esperado: 5.0
    print(eh_par(4))         # Esperado: True
    try:
        divide(5, 0)
    except ValueError as e:
        print(f"Erro esperado: {e}")
