import array
import tkinter as tk

# --- Sistema de Rastreamento (Motor) ---
historico_estados = []
pilha_atual = []
logs_acumulados = []

def registrar_estado(mensagem_evento):
    """Tira uma 'foto' da pilha de chamadas e do último evento ocorrido."""
    logs_acumulados.append(mensagem_evento)
    historico_estados.append({
        "pilha": list(pilha_atual),
        "log": mensagem_evento
    })

# --- O Seu Código Original (com Rastreadores) ---

def copiar(vetor, inicio, fim):
    assinatura = f"copiar(inicio={inicio}, fim={fim})"
    pilha_atual.append(assinatura)
    registrar_estado(f"-> Preparando para copiar subvetor de índices {inicio} até {fim-1}.")
    
    tamanho = fim - inicio
    v = array.array("i", [0] * tamanho)
    i = 0
    while i < tamanho:
        v[i] = vetor[inicio + i]
        i += 1
        
    pilha_atual.pop()
    registrar_estado(f"<- Cópia concluída. Resultado: {list(v)}")
    return v

def merge(ord_esq, tam_esq, ord_dir, tam_dir):
    assinatura = f"merge(esq={list(ord_esq)}, dir={list(ord_dir)})"
    pilha_atual.append(assinatura)
    registrar_estado(f"-> Iniciando merge entre {list(ord_esq)} e {list(ord_dir)}.")

    ord = array.array("i", [0] * (tam_esq + tam_dir))
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

    pilha_atual.pop()
    registrar_estado(f"<- Merge concluído. Vetor ordenado resultante: {list(ord)}")
    return ord

def merge_sort(vetor, fim):
    assinatura = f"merge_sort(vetor={list(vetor)}, fim={fim})"
    pilha_atual.append(assinatura)
    registrar_estado(f"-> Entrando no merge_sort com vetor {list(vetor)}.")

    if fim <= 1:
        pilha_atual.pop()
        registrar_estado(f"<- Caso Base atingido! Vetor de tamanho 1 retornado: {list(vetor)}")
        return vetor

    meio = fim // 2
    
    # Chamadas de cópia
    v_esq = copiar(vetor, 0, meio)
    v_dir = copiar(vetor, meio, fim)

    # Chamadas recursivas
    ord_esq = merge_sort(v_esq, meio)
    ord_dir = merge_sort(v_dir, meio + (fim % 2))

    # Chamada de união
    resultado = merge(ord_esq, meio, ord_dir, meio + (fim % 2))
    
    pilha_atual.pop()
    registrar_estado(f"<- Saindo de merge_sort. Retornando: {list(resultado)}")
    return resultado


# --- Interface Gráfica (Tkinter) ---

class AppVisualizador:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Call Stack - Merge Sort")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f4f4f4")
        
        self.passo_atual = 0
        self.total_passos = len(historico_estados)
        
        self.construir_interface()
        self.atualizar_tela()

    def construir_interface(self):
        # Topo: Informações
        frame_topo = tk.Frame(self.root, bg="#f4f4f4", pady=10)
        frame_topo.pack(fill=tk.X)
        
        self.lbl_passo = tk.Label(frame_topo, text="", font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#333")
        self.lbl_passo.pack()
        
        # Centro: Dividido em duas colunas (Pilha e Log)
        frame_central = tk.Frame(self.root, bg="#f4f4f4", padx=20, pady=10)
        frame_central.pack(fill=tk.BOTH, expand=True)
        
        # Coluna Esquerda (Call Stack)
        frame_pilha = tk.LabelFrame(frame_central, text=" Call Stack (Pilha de Chamadas) ", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#0056b3")
        frame_pilha.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Dica visual de onde é o topo
        tk.Label(frame_pilha, text="▲ TOPO (Última função chamada)", font=("Segoe UI", 9), bg="#ffffff", fg="gray").pack(pady=5)
        
        self.lista_pilha = tk.Listbox(frame_pilha, font=("Consolas", 12), bg="#1e1e1e", fg="#56b6c2", highlightthickness=0, borderwidth=0)
        self.lista_pilha.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        tk.Label(frame_pilha, text="▼ BASE DA PILHA (Início)", font=("Segoe UI", 9), bg="#ffffff", fg="gray").pack(pady=5)

        # Coluna Direita (Log de Eventos)
        frame_log = tk.LabelFrame(frame_central, text=" Log de Execução ", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#d9534f")
        frame_log.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.texto_log = tk.Text(frame_log, font=("Segoe UI", 11), bg="#fdfdfd", fg="#333", state=tk.DISABLED, highlightthickness=0, borderwidth=0, wrap=tk.WORD)
        self.texto_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Base: Botões de navegação
        frame_botoes = tk.Frame(self.root, bg="#f4f4f4", pady=20)
        frame_botoes.pack(fill=tk.X)
        
        estilo_btn = {"font": ("Segoe UI", 12, "bold"), "width": 15, "cursor": "hand2"}
        
        self.btn_anterior = tk.Button(frame_botoes, text="◀ Anterior", command=self.voltar, **estilo_btn)
        self.btn_anterior.pack(side=tk.LEFT, padx=50)
        
        self.btn_proximo = tk.Button(frame_botoes, text="Próximo ▶", command=self.avancar, **estilo_btn)
        self.btn_proximo.pack(side=tk.RIGHT, padx=50)

    def atualizar_tela(self):
        estado = historico_estados[self.passo_atual]
        
        # 1. Atualizar Título de Progresso
        self.lbl_passo.config(text=f"Passo {self.passo_atual + 1} de {self.total_passos}")
        
        # 2. Atualizar Call Stack (inserimos de trás pra frente para o topo ficar em cima)
        self.lista_pilha.delete(0, tk.END)
        for assinatura_funcao in reversed(estado["pilha"]):
            self.lista_pilha.insert(tk.END, f"  {assinatura_funcao}")
            
        if not estado["pilha"]:
            self.lista_pilha.insert(tk.END, "  [ Pilha Vazia ]")

        # 3. Atualizar Log (mostramos todos os logs até o passo atual)
        self.texto_log.config(state=tk.NORMAL)
        self.texto_log.delete(1.0, tk.END)
        for i in range(self.passo_atual + 1):
            evento = historico_estados[i]["log"]
            self.texto_log.insert(tk.END, f"Passo {i+1}: {evento}\n\n")
        
        self.texto_log.see(tk.END) # Rola automaticamente para o fim
        self.texto_log.config(state=tk.DISABLED)

        # 4. Controle dos botões
        self.btn_anterior.config(state=tk.NORMAL if self.passo_atual > 0 else tk.DISABLED)
        self.btn_proximo.config(state=tk.NORMAL if self.passo_atual < self.total_passos - 1 else tk.DISABLED)

    def avancar(self):
        if self.passo_atual < self.total_passos - 1:
            self.passo_atual += 1
            self.atualizar_tela()

    def voltar(self):
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self.atualizar_tela()


if __name__ == "__main__":
    # 1. Preparar vetor
    vetor_inicial = array.array("i", [6, 5, 12, 10, 9, 1])
    
    # 2. Registrar o início
    registrar_estado("Início da execução. Vetor não ordenado recebido.")
    
    # 3. Executar o algoritmo para mapear todo o histórico
    merge_sort(vetor_inicial, 6)
    
    # 4. Registrar fim
    registrar_estado("Fim da execução. Vetor completamente ordenado.")
    
    # 5. Iniciar Interface Gráfica
    root = tk.Tk()
    app = AppVisualizador(root)
    root.mainloop()