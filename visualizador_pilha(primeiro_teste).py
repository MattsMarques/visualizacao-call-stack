import tkinter as tk
import time

# --- Configurações Visuais ---
LARGURA_FRAME = 200
ALTURA_FRAME = 40
ESPACAMENTO = 10
Y_INICIAL = 50
VELOCIDADE = 1.0  # segundos entre cada passo

class VisualizadorPilha:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador da Call Stack - Fatorial")
        
        # Cria a tela em branco para desenhar
        self.canvas = tk.Canvas(root, width=400, height=500, bg="white")
        self.canvas.pack()
        
        # Pilha para guardar as IDs das caixas desenhadas (para podermos apagá-las)
        self.ids_das_caixas = []

    def desenhar_frame(self, n, profundidade):
        """Desenha uma 'caixa' representando o frame factorial(n)"""
        x = 100
        y = Y_INICIAL + (profundidade * (ALTURA_FRAME + ESPACAMENTO))
        
        # Desenha o retângulo (o frame da memória)
        box_id = self.canvas.create_rectangle(x, y, x + LARGURA_FRAME, y + ALTURA_FRAME, 
                                               fill="#add8e6", outline="blue", width=2)
        # Desenha o texto dentro
        text_id = self.canvas.create_text(x + LARGURA_FRAME/2, y + ALTURA_FRAME/2, 
                                          text=f"factorial({n})", fill="black", font=("Arial", 12, "bold"))
        
        # Guarda os IDs para apagar depois
        self.ids_das_caixas.append((box_id, text_id))
        
        # Força a tela a se atualizar
        self.root.update()
        time.sleep(VELOCIDADE) # Pausa para a plateia conseguir ver

    def apagar_frame(self):
        """Apaga a caixa do topo da pilha"""
        if self.ids_das_caixas:
            box_id, text_id = self.ids_das_caixas.pop()
            self.canvas.delete(box_id)
            self.canvas.delete(text_id)
            
            self.root.update()
            time.sleep(VELOCIDADE / 2) # Pausa mais rápida no retorno

# --- O ALGORITMO RECURSIVO ADAPTADO ---
def factorial_visual(n, visualizador, profundidade=0):
    # PUSH: Empilhando um novo frame
    visualizador.desenhar_frame(n, profundidade)
    
    # Caso Base
    if n <= 1:
        time.sleep(VELOCIDADE) # Destaca o caso base
        visualizador.apagar_frame() # POP do caso base
        return 1
    
    # Chamada Recursiva
    result = n * factorial_visual(n - 1, visualizador, profundidade + 1)
    
    # POP: Desempilhando após o retorno
    visualizador.apagar_frame()
    return result

# --- Execução Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizadorPilha(root)
    
    # Botão para iniciar
    def iniciar():
        app.canvas.delete("all") # Limpa a tela
        app.ids_das_caixas = []
        n = 4 # Caso de teste
        factorial_visual(n, app)
        print("Fim da execução.")

    btn = tk.Button(root, text=f"Iniciar factorial(4)", command=iniciar)
    btn.pack(pady=10)
    
    root.mainloop()