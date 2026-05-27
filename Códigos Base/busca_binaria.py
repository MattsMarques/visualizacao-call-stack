import array

def busca_binaria(vetor, numero, inicio, fim):
    meio = (inicio+fim)//2
    
    if inicio > fim:
        return -1
    
    if vetor[meio]==numero:
        return meio
        
    if vetor[meio] < numero:
        return busca_binaria(vetor, numero, meio+1, fim)
    else:
        return busca_binaria(vetor, numero, inicio, meio-1)    
        
        
vetor = array.array("i", [0]*7)

vetor[0] = 1
vetor[1] = 3
vetor[2] = 4
vetor[3] = 6
vetor[4] = 9
vetor[5] = 13
vetor[6] = 14

print("\nVETOR: ")
print("-"*40)
print(vetor)

num_buscado = 14

print("\nNÚMERO BUSCADO: ",num_buscado)
print("-"*40)
print("RESULTADO: ",busca_binaria(vetor, num_buscado, 0, 7))
        

        
    