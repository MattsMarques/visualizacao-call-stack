import tkinter as tk
from tkinter import ttk
import array

class AppBuscaBinaria:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pilha de Recursão - Busca Binária")
        self.root.geometry("800x600")
        
        # --- Dados do seu código ---
        self.vetor = array.array("i", [1, 3, 4, 6, 9, 13, 14])
        self.numero_alvo = 14
        
        # Estado da animação/passos
        self.passos = []
        self.passo_atual = 0
        
        # Gerar os passos da recursão antes de desenhar
        self.generar_passos_recursao(0, len(self.vetor) - 1, nivel=0)
        
        # --- Interface Gráfica (Layout) ---
        # Painel Superior: Dados do Vetor
        self.frame_topo = ttk.LabelFrame(root, text=" Vetor e Alvo ", padding=10)
        self.frame_topo.pack(fill="x", padx=15, pady=10)
        
        lbl_vetor = ttk.Label(self.frame_topo, text=f"Vetor: {list(self.vetor)}", font=("Courier", 12, "bold"))
        lbl_vetor.pack(side="left", padx=10)
        
        lbl_alvo = ttk.Label(self.frame_topo, text=f"Buscando número: {self.numero_alvo}", font=("Arial", 11))
        lbl_alvo.pack(side="right", padx=10)
        
        # Painel Central: Dividido em Pilha (Visual) e Logs (Texto)
        self.frame_central = ttk.Frame(root, padding=10)
        self.frame_central.pack(fill="both", expand=True, padx=15)
        
        # Sub-frame Esquerdo: Representação da Pilha
        self.frame_pilha = ttk.LabelFrame(self.frame_central, text=" Pilha de Execução (Call Stack) ", padding=10)
        self.frame_pilha.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.canvas_pilha = tk.Canvas(self.frame_pilha, bg="#f0f0f0", highlightthickness=0)
        self.canvas_pilha.pack(fill="both", expand=True)
        
        # Sub-frame Direito: Explicação em Texto
        self.frame_texto = ttk.LabelFrame(self.frame_central, text=" O que está acontecendo? ", padding=10)
        self.frame_texto.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.txt_log = tk.Text(self.frame_texto, wrap="word", font=("Arial", 11), bg="#fafafa", state="disabled")
        self.txt_log.pack(fill="both", expand=True)
        
        # Painel Inferior: Controles
        self.frame_botoes = ttk.Frame(root, padding=10)
        self.frame_botoes.pack(fill="x", side="bottom")
        
        self.btn_anterior = ttk.Button(self.frame_botoes, text="↩ Passo Anterior", command=self.passo_anterior, state="disabled")
        self.btn_anterior.pack(side="left", padx=20)
        
        self.btn_proximo = ttk.Button(self.frame_botoes, text="Próximo Passo ↪", command=self.proximo_passo)
        self.btn_proximo.pack(side="right", padx=20)
        
        self.lbl_status = ttk.Label(self.frame_botoes, text=f"Passo 0 de {len(self.passos)-1}", font=("Arial", 10))
        self.lbl_status.pack(side="bottom")
        
        # Renderizar o estado inicial
        self.atualizar_tela()

    def generar_passos_recursao(self, inicio, fim, nivel):
        """ Simula a busca binária salvando os estados de 'Ida' e 'Volta' da pilha """
        
        # 1. Caso base: Não encontrado
        if inicio > fim:
            self.passos.append({
                'tipo': 'ida', 'nivel': nivel, 'inicio': inicio, 'fim': fim, 'meio': None,
                'msg': f"Chamada {nivel}: inicio ({inicio}) > fim ({fim}). O número não está aqui! Retornando -1."
            })
            self.passos.append({
                'tipo': 'volta', 'nivel': nivel, 'retorno': -1,
                'msg': f"Chamada {nivel} finalizada. Devolvendo -1 para quem a chamou."
            })
            return -1

        meio = (inicio + fim) // 2
        valor_meio = self.vetor[meio]
        
        # Registra a ENTRADA na pilha (Ida)
        self.passos.append({
            'tipo': 'ida', 'nivel': nivel, 'inicio': inicio, 'fim': fim, 'meio': meio,
            'msg': f"Chamada {nivel}: busca_binaria(inicio={inicio}, fim={fim})\nCalculou meio = {meio} (Valor: {valor_meio})."
        })

        # 2. Caso base: Encontrou
        if valor_meio == self.numero_alvo:
            self.passos.append({
                'tipo': 'ida', 'nivel': nivel, 'inicio': inicio, 'fim': fim, 'meio': meio,
                'msg': f"💥 Encontrou! vetor[{meio}] é igual a {self.numero_alvo}.\nIniciando o retorno do índice {meio}..."
            })
            self.passos.append({
                'tipo': 'volta', 'nivel': nivel, 'retorno': meio,
                'msg': f"Chamada {nivel} finalizada. Devolvendo índice {meio} para cima."
            })
            return meio

        # 3. Casos Recursivos
        elif valor_meio < self.numero_alvo:
            self.passos[-1]['msg'] += f"\nComo {valor_meio} < {self.numero_alvo}, busca na metade DIREITA (inicio vira {meio + 1})."
            resultado = self.generar_passos_recursao(meio + 1, fim, nivel + 1)
        else:
            self.passos[-1]['msg'] += f"\nComo {valor_meio} > {self.numero_alvo}, busca na metade ESQUERDA (fim vira {meio - 1})."
            resultado = self.generar_passos_recursao(inicio, meio - 1, nivel + 1)
            
        # Registra a SAÍDA da pilha (Volta/Desempilhamento)
        self.passos.append({
            'tipo': 'volta', 'nivel': nivel, 'retorno': resultado,
            'msg': f"Chamada {nivel} recebeu o retorno [{resultado}] da sua sub-chamada.\nRepassando [{resultado}] para a chamada anterior."
        })
        return resultado

    def atualizar_tela(self):
        """ Desenha a pilha visual e atualiza os textos com base no passo atual """
        self.canvas_pilha.delete("all")
        passo = self.passos[self.passo_atual]
        
        # Atualiza logs textuais
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.insert(tk.END, passo['msg'])
        self.txt_log.configure(state="disabled")
        
        # Atualiza label inferior
        self.lbl_status.config(text=f"Passo {self.passo_atual} de {len(self.passos)-1}")
        
        # Controla ativação dos botões
        self.btn_anterior.config(state="normal" if self.passo_atual > 0 else "disabled")
        self.btn_proximo.config(state="normal" if self.passo_atual < len(self.passos)-1 else "disabled")
        
        # --- Desenhar a Pilha Graficamente ---
        largura_canvas = self.canvas_pilha.winfo_width() if self.canvas_pilha.winfo_width() > 10 else 350
        altura_bloco = 70
        espacamento = 10
        base_y = 450 # Fundo da pilha
        
        # Descobrir quais níveis estão ativos neste passo da animação
        niveis_ativos = {}
        for p in range(self.passo_atual + 1):
            inf = self.passos[p]
            if inf['tipo'] == 'ida':
                niveis_ativos[inf['nivel']] = inf
            elif inf['tipo'] == 'volta':
                # Se completou a volta desse nível, remove ele da visualização ativa
                if inf['nivel'] in niveis_ativos and p == self.passo_atual and self.passos[p]['tipo'] == 'volta':
                    # Mantém mas pinta de cor diferente para mostrar saindo
                    niveis_ativos[inf['nivel']]['saindo'] = inf['retorno']
                elif inf['nivel'] in niveis_ativos:
                    del niveis_ativos[inf['nivel']]

        # Desenhar os blocos ativos
        for nivel, dados in sorted(niveis_ativos.items()):
            # Calcula a posição vertical (níveis mais altos ficam em cima)
            y2 = base_y - (nivel * (altura_bloco + espacamento))
            y1 = y2 - altura_bloco
            
            x1 = 30
            x2 = largura_canvas - 30
            
            # Define as cores baseadas no estado (Ida ou Volta)
            if 'saindo' in dados:
                cor_fundo = "#ff8c00" # Laranja: desempilhando / retornando dado
                texto_status = f"Retornando: {dados['saindo']}"
            elif nivel == max(niveis_ativos.keys()):
                cor_fundo = "#4ade80" # Verde: chamada que está executando agora
                texto_status = "Executando..."
            else:
                cor_fundo = "#60a5fa" # Azul: aguardando resposta da filha
                texto_status = "Aguardando sub-recursão..."
                
            # Desenha o bloco da memória
            self.canvas_pilha.create_rectangle(x1, y1, x2, y2, fill=cor_fundo, outline="#333", width=2)
            
            # Textos internos do bloco
            txt_funcao = f"busca_binaria(inicio={dados['inicio']}, fim={dados['fim']})"
            self.canvas_pilha.create_text(x1 + 15, y1 + 20, anchor="w", text=txt_funcao, font=("Arial", 11, "bold"), fill="black")
            
            if dados['meio'] is not None:
                txt_detalhe = f"Meio calculado: índice {dados['meio']} (valor {self.vetor[dados['meio']]})"
            else:
                txt_detalhe = "Verificando limites..."
            self.canvas_pilha.create_text(x1 + 15, y1 + 40, anchor="w", text=txt_detalhe, font=("Arial", 10), fill="#222")
            
            # Tag de Status do bloco
            self.canvas_pilha.create_text(x2 - 15, y1 + 20, anchor="e", text=texto_status, font=("Arial", 9, "italic"), fill="black")
            self.canvas_pilha.create_text(x2 - 15, y1 + 45, anchor="e", text=f"Nível {nivel}", font=("Courier", 12, "bold"), fill="#333")

    def proximo_passo(self):
        if self.passo_atual < len(self.passos) - 1:
            self.passo_atual += 1
            self.atualizar_tela()

    def passo_anterior(self):
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self.atualizar_tela()

# --- Execução do App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppBuscaBinaria(root)
    
    # Pequena gambiarra para esperar a janela desenhar e ajustar as larguras do canvas corretamente
    root.update()
    app.atualizar_tela()
    
    root.mainloop()