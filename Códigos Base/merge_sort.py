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

def merge(ord_esq, tam_esq, ord_dir, tam_dir):
    ord = array.array("i", [0]*(tam_esq + tam_dir))

    i = 0
    j = 0

    while (i < tam_esq and j < tam_dir):
        if (ord_esq[i] < ord_dir[j]):
            ord[i+j] = ord_esq[i]
            i += 1
        else:
            ord[i+j] = ord_dir[j]
            j += 1

    while (i < tam_esq):
        ord[i+j] = ord_esq[i]
        i += 1

    while (j < tam_dir):
        ord[i+j] = ord_dir[j]
        j += 1

    return ord

    
def merge_sort(vetor, fim):
    if fim <= 1:
        return vetor

    meio = fim//2
    v_esq = copiar(vetor, 0, meio)
    v_dir = copiar(vetor, meio, fim)

    ord_esq = merge_sort(v_esq, meio)
    ord_dir = merge_sort(v_dir, meio + (fim % 2))

    return merge(ord_esq, meio, ord_dir, meio + (fim % 2))
    

vetor = array.array("i", [0]*6)

vetor[0] = 6
vetor[1] = 5
vetor[2] = 12
vetor[3] = 10
vetor[4] = 9
vetor[5] = 1
    

imprimir_vetor(vetor, 6)

print("\n")
#imprimir_vetor(merge_sort(vetor, 6), 6)

print(merge_sort(vetor, 6))

    