import tkinter as tk
import subprocess
import sys
import os

COR_FUNDO = "#F1F1F1"
COR_CARD_BG = "#ffffff"
COR_VERDE = "#4ADE80"  
COR_TEXTO_ESCURO = "#000000"
COR_TEXTO_MUTED = "#666666"

FONTE_TITULO = "Cabinet Grotesk"
FONTE_TEXTO = "Inter"

class AppHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Principal - Algoritmos Recursivos")
        self.root.geometry("900x600")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(True, True)
        
        self.selecionado = None
        
        self.arquivos = {
            1: "./visualizadores/visualizador_fatorial.py",
            2: "./visualizadores/visualizador_merge_sort.py",       
            3: "./visualizadores/visualizador_busca_binaria.py"
        }
        
        self.construir_interface()

    def construir_interface(self):
        # --- CABEÇALHO ---
        self.lbl_titulo = tk.Label(
            self.root, 
            text="O QUE DESEJA FAZER?", 
            font=(FONTE_TITULO, 28, "bold"), 
            bg=COR_FUNDO, 
            fg=COR_TEXTO_ESCURO
        )
        self.lbl_titulo.pack(pady=(60, 5))
        
        self.lbl_subtitulo = tk.Label(
            self.root, 
            text="Selecione o algoritmo recursivo de sua preferência.", 
            font=(FONTE_TEXTO, 14), 
            bg=COR_FUNDO, 
            fg=COR_TEXTO_MUTED
        )
        self.lbl_subtitulo.pack(pady=(0, 40))

        # --- CONTAINER DOS CARDS ---
        frame_cards = tk.Frame(self.root, bg=COR_FUNDO)
        frame_cards.pack(pady=20)

        # Configurações comuns dos cards
        largura_card, altura_card = 200, 220

        # CARD 1: Fatorial
        self.card1 = tk.Frame(frame_cards, bg=COR_CARD_BG, width=largura_card, height=altura_card, highlightthickness=2, highlightbackground="#dddddd")
        self.card1.pack_propagate(False)
        self.card1.pack(side=tk.LEFT, padx=15)
        self.lbl_ico1 = tk.Label(self.card1, text="n!", font=(FONTE_TEXTO, 38), bg=COR_CARD_BG, fg=COR_TEXTO_ESCURO)
        self.lbl_ico1.pack(expand=True, pady=(20, 0))
        self.lbl_txt1 = tk.Label(self.card1, text="Fatorial", font=(FONTE_TEXTO, 14, "bold"), bg=COR_CARD_BG, fg=COR_TEXTO_ESCURO)
        self.lbl_txt1.pack(expand=True, pady=(0, 20))

        # CARD 2: Merge Sort
        self.card2 = tk.Frame(frame_cards, bg=COR_CARD_BG, width=largura_card, height=altura_card, highlightthickness=2, highlightbackground="#dddddd")
        self.card2.pack_propagate(False)
        self.card2.pack(side=tk.LEFT, padx=15)
        self.lbl_ico2 = tk.Label(self.card2, text="⇄", font=(FONTE_TEXTO, 38), bg=COR_CARD_BG, fg=COR_TEXTO_ESCURO)
        self.lbl_ico2.pack(expand=True, pady=(20, 0))
        self.lbl_txt2 = tk.Label(self.card2, text="Merge Sort", font=(FONTE_TEXTO, 14, "bold"), bg=COR_CARD_BG, fg=COR_TEXTO_ESCURO)
        self.lbl_txt2.pack(expand=True, pady=(0, 20))

        # CARD 3: Busca Binária
        self.card3 = tk.Frame(frame_cards, bg=COR_CARD_BG, width=largura_card, height=altura_card, highlightthickness=2, highlightbackground="#dddddd")
        self.card3.pack_propagate(False)
        self.card3.pack(side=tk.LEFT, padx=15)
        self.lbl_ico3 = tk.Label(self.card3, text="🔍", font=(FONTE_TEXTO, 38), bg=COR_CARD_BG, fg=COR_TEXTO_ESCURO)
        self.lbl_ico3.pack(expand=True, pady=(20, 0))
        self.lbl_txt3 = tk.Label(self.card3, text="Busca Binária", font=(FONTE_TEXTO, 14, "bold"), bg=COR_CARD_BG, fg=COR_TEXTO_ESCURO)
        self.lbl_txt3.pack(expand=True, pady=(0, 20))

        self.vincular_clique(self.card1, self.lbl_ico1, self.lbl_txt1, 1)
        self.vincular_clique(self.card2, self.lbl_ico2, self.lbl_txt2, 2)
        self.vincular_clique(self.card3, self.lbl_ico3, self.lbl_txt3, 3)

        self.btn_proximo = tk.Button(
            self.root, 
            text="Próximo", 
            font=(FONTE_TEXTO, 14, "bold"), 
            bg=COR_VERDE, 
            fg="#ffffff",          
            activebackground=COR_VERDE,
            activeforeground="#ffffff",
            bd=0, 
            padx=40, 
            pady=10,
            cursor="hand2",
            command=self.abrir_algoritmo
        )
        self.btn_proximo.pack(pady=(40, 0))
        
        self.marcar_selecao(1)

    def vincular_clique(self, frame, label_ico, label_txt, id_opcao):
        # Garante que clicar em qualquer parte do quadrado ative a seleção
        frame.bind("<Button-1>", lambda event: self.marcar_selecao(id_opcao))
        label_ico.bind("<Button-1>", lambda event: self.marcar_selecao(id_opcao))
        label_txt.bind("<Button-1>", lambda event: self.marcar_selecao(id_opcao))

    def marcar_selecao(self, id_opcao):
        self.selecionado = id_opcao
        
        # Resetar todos os cards para o padrão cinza/preto
        self.card1.config(highlightbackground="#dddddd")
        self.lbl_ico1.config(fg=COR_TEXTO_ESCURO)
        self.lbl_txt1.config(fg=COR_TEXTO_ESCURO)
        
        self.card2.config(highlightbackground="#dddddd")
        self.lbl_ico2.config(fg=COR_TEXTO_ESCURO)
        self.lbl_txt2.config(fg=COR_TEXTO_ESCURO)
        
        self.card3.config(highlightbackground="#dddddd")
        self.lbl_ico3.config(fg=COR_TEXTO_ESCURO)
        self.lbl_txt3.config(fg=COR_TEXTO_ESCURO)

        #destaque verde 
        if id_opcao == 1:
            self.card1.config(highlightbackground=COR_VERDE)
            self.lbl_ico1.config(fg=COR_VERDE)
            self.lbl_txt1.config(fg=COR_VERDE)
        elif id_opcao == 2:
            self.card2.config(highlightbackground=COR_VERDE)
            self.lbl_ico2.config(fg=COR_VERDE)
            self.lbl_txt2.config(fg=COR_VERDE)
        elif id_opcao == 3:
            self.card3.config(highlightbackground=COR_VERDE)
            self.lbl_ico3.config(fg=COR_VERDE)
            self.lbl_txt3.config(fg=COR_VERDE)

    def abrir_algoritmo(self):
        if self.selecionado in self.arquivos:
            nome_arquivo = self.arquivos[self.selecionado]
            
            if os.path.exists(nome_arquivo):
                subprocess.Popen([sys.executable, nome_arquivo])
            else:
                print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado nesta pasta.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppHub(root)
    root.mainloop()