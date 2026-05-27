import array 

def imprimir_vetor(vetor, tamanho):
    for i in range(tamanho):
        print(vetor[i])

def copiar(vetor, inicio, fim):
    tamanho = fim-inicio
    v = array.array("i", [0]*tamanho)
    i = 0
    while i < tamanho:
        v[i] = vetor[inicio+i]
        i+=1

    return v

def merge(o_esq, tam_esq, o_dir, tam_dir):
    o = array.array("i", [0]*(tam_esq + tam_dir))

    i = 0
    j = 0

    while (i < tam_esq and j < tam_dir):
        if (o_esq[i] < o_dir[j]):
            o[i+j] = o_esq[i]
            i += 1
        else:
            o[i+j] = o_dir[j]
            j += 1

    while (i < tam_esq):
        o[i+j] = o_esq[i]
        i += 1

    while (j < tam_dir):
        o[i+j] = o_dir[j]
        j += 1

    return o

    
def merge_sort(vetor, fim):
    if fim <= 1:
        return vetor

    meio = fim//2
    v_esq = copiar(vetor, 0, meio)
    v_dir = copiar(vetor, meio, fim)

    o_esq = merge_sort(v_esq, meio)
    o_dir = merge_sort(v_dir, meio + (fim % 2))

    return merge(o_esq, meio, o_dir, meio + (fim % 2))
    

vetor = array.array("i", [0]*6)

vetor[0] = 6
vetor[1] = 5
vetor[2] = 12
vetor[3] = 10
vetor[4] = 9
vetor[5] = 1
    

print("\nVETOR PRÉ O MERGE_SORT")
print("-"*30)
imprimir_vetor(vetor, 6)

print("\nVETOR PÓS O MERGE_SORT")
print("-"*30)
imprimir_vetor(merge_sort(vetor, 6), 6)