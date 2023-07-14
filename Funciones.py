import numpy as np

#Pasar de decimal a binario

def abinario(numero_decimal):
    numero_binario = 0
    multiplicador = 1

    while numero_decimal != 0:
        # se almacena el módulo en el orden correcto
        numero_binario = numero_binario + numero_decimal % 2 * multiplicador
        numero_decimal //= 2
        multiplicador *= 10

    return numero_binario



  # ejemplos de uso

##print(abinario(255))


#Pasar de binario a decimal

def adecimal(numero_binario):
	numero_decimal = 0

	for posicion, digito_string in enumerate(numero_binario[::-1]):
		numero_decimal += int(digito_string) * 2 ** posicion

	return numero_decimal
#print(adecimal('101'))
    
def abool(s):
    x = 0
    if s == 2:
        x = 1 
    return x
##print(abool(2))

def checkBox(a,b):
    '''Todos los checkBox, llama con la función check al botón que se necesite
    Ej.: check(2) = checkBox1_3 (nombre en QtDesigner)'''
    r = range(32)
    numero = 0
    pin = []
    for i in r:
       numero += 1
       pin.append("checkBox1_"+ str(numero))
    return pin[a:b]
##print(checkBox(0,1))

def bina(c,posicion):
    l = c*(2**posicion)
    return l
##print(bina(1,2))

def pin(m,posicion):
    k = bina(abool(m),posicion)
    return k
##print(pin(1,2))

def potencia(base, exponente):
    resultado = 1
    r = [1]
    for i in range(exponente):
        resultado *=base
        r.append(resultado)     
    return r

def frecuencia(NumeroDec):
    '''Cambia de nùmero entero a frecuencia en MHz'''
    Freq = NumeroDec*500/(2^(23))
    return Freq

def numero(Freq):
     '''Cambia de frecuencia en MHz a nùmero entero'''
     N = np.uint32(Freq*(2**(23))/(500))
     return N
