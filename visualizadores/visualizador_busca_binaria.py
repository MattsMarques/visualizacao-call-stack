import tkinter as tk
from tkinter import ttk
import array

FONTE_HEAD = "Cabinet Grotesk"
FONTE_TXT = "Inter"


class AppBuscaBinaria:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pilha de Recursão - Busca Binária")
        self.root.geometry("1000x760")
        self.root.configure(bg="#f5f5f5")

        # ---------------- DADOS ----------------
        self.vetor = array.array("i", [1, 3, 4, 6, 9, 13, 14])
        self.numero_alvo = 14

        # ---------------- ESTADO ----------------
        self.passos = []
        self.passo_atual = 0

        # Gera todos os passos da recursão
        self.generar_passos_recursao(
            0,
            len(self.vetor) - 1,
            nivel=1
        )

        # Configura estilos e layout
        self.configurar_estilos()
        self.criar_layout()

        # Renderiza tela inicial
        self.atualizar_tela()

    def configurar_estilos(self):
        style = ttk.Style()

        style.configure(
            "Card.TFrame",
            background="#ffffff",
            borderwidth=1,
            relief="solid"
        )

        style.configure(
            "Stack.TLabelframe",
            background="#f5f5f5",
            borderwidth=0
        )

        style.configure(
            "Stack.TLabelframe.Label",
            background="#f5f5f5",
            foreground="#7a7a7a",
            font=(FONTE_TXT, 11)
        )

    def criar_layout(self):

        # ---------------- TOPO ----------------
        self.frame_topo = ttk.Frame(
            self.root,
            style="Card.TFrame",
            padding=20
        )
        self.frame_topo.pack(
            fill="x",
            padx=40,
            pady=(40, 20)
        )

        lbl_alvo = tk.Label(
            self.frame_topo,
            text=f"Buscando número: {self.numero_alvo}",
            font=(FONTE_TXT, 16, "bold"),
            bg="#ffffff",
            fg="#111111"
        )
        lbl_alvo.pack(side="left")

        lbl_vetor = tk.Label(
            self.frame_topo,
            text=f"Vetor: {list(self.vetor)}",
            font=(FONTE_TXT, 16, "bold"),
            bg="#ffffff",
            fg="#111111"
        )
        lbl_vetor.pack(side="right")

        # ---------------- CALL STACK ----------------
        self.frame_stack = ttk.LabelFrame(
            self.root,
            text=" Pilha de Execução (Call Stack) ",
            style="Stack.TLabelframe",
            padding=22
        )

        self.frame_stack.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(10, 30)
        )

        self.canvas_pilha = tk.Canvas(
            self.frame_stack,
            bg="#f5f5f5",
            highlightthickness=1,
            highlightbackground="#d9d9d9"
        )

        self.canvas_pilha.pack(
            fill="both",
            expand=True
        )

        # ---------------- RODAPÉ ----------------
        self.frame_botoes = tk.Frame(
            self.root,
            bg="#f5f5f5"
        )

        self.frame_botoes.pack(
            fill="x",
            side="bottom",
            padx=40,
            pady=(0, 24)
        )

        self.btn_anterior = tk.Button(
            self.frame_botoes,
            text="← Passo Anterior",
            command=self.passo_anterior,
            state="disabled",
            font=(FONTE_TXT, 12),
            bg="#ffffff",
            fg="#111111",
            relief="solid",
            borderwidth=1,
            padx=18,
            pady=10,
            cursor="hand2"
        )

        self.btn_anterior.pack(side="left")

        self.lbl_status = tk.Label(
            self.frame_botoes,
            text=f"Passo 0 de {len(self.passos)-1}",
            font=(FONTE_TXT, 12),
            bg="#f5f5f5",
            fg="#111111"
        )

        self.lbl_status.pack(side="bottom")

        self.btn_proximo = tk.Button(
            self.frame_botoes,
            text="Próximo Passo  →",
            command=self.proximo_passo,
            font=(FONTE_TXT, 12),
            bg="#4ade80",
            fg="#0b5d31",
            activebackground="#3fd174",
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2"
        )

        self.btn_proximo.pack(side="right")

    def generar_passos_recursao(self, inicio, fim, nivel):
        if inicio > fim:

            self.passos.append({
                'tipo': 'ida',
                'nivel': nivel,
                'inicio': inicio,
                'fim': fim,
                'meio': None
            })

            self.passos.append({
                'tipo': 'volta',
                'nivel': nivel,
                'retorno': -1
            })

            return -1

        meio = (inicio + fim) // 2
        valor_meio = self.vetor[meio]

        # Registra entrada da chamada
        self.passos.append({
            'tipo': 'ida',
            'nivel': nivel,
            'inicio': inicio,
            'fim': fim,
            'meio': meio
        })

        if valor_meio == self.numero_alvo:
            self.passos.append({
                'tipo': 'volta',
                'nivel': nivel,
                'inicio': inicio,
                'fim': fim,
                'meio': meio,
                'retorno': meio
            })

            return meio

        elif valor_meio < self.numero_alvo:
            resultado = self.generar_passos_recursao(
                meio + 1,
                fim,
                nivel + 1
            )

        else:
            resultado = self.generar_passos_recursao(
                inicio,
                meio - 1,
                nivel + 1
            )

        # -----------------------------------------------------
        # RETORNO DA CHAMADA
        # -----------------------------------------------------
        self.passos.append({
            'tipo': 'volta',
            'nivel': nivel,
            'inicio': inicio,
            'fim': fim,
            'meio': meio,
            'retorno': resultado
        })

        return resultado

    # =========================================================
    # ATUALIZA INTERFACE
    # =========================================================
    def atualizar_tela(self):

        self.canvas_pilha.delete("all")

        passo = self.passos[self.passo_atual]

        # ---------------- STATUS ----------------
        self.lbl_status.config(
            text=f"Passo {self.passo_atual} de {len(self.passos)-1}"
        )

        # ---------------- BOTÕES ----------------
        self.btn_anterior.config(
            state="normal"
            if self.passo_atual > 0
            else "disabled"
        )

        self.btn_proximo.config(
            state="normal"
            if self.passo_atual < len(self.passos)-1
            else "disabled"
        )

        # ---------------- TAMANHO CANVAS ----------------
        largura_canvas = (
            self.canvas_pilha.winfo_width()
            if self.canvas_pilha.winfo_width() > 10
            else 800
        )

        altura_bloco = 126
        espacamento = 22
        base_y = 560

        # =====================================================
        # DESCOBRE NÍVEIS ATIVOS
        # =====================================================
        niveis_ativos = {}

        for p in range(self.passo_atual + 1):

            info = self.passos[p]

            if info['tipo'] == 'ida':

                niveis_ativos[info['nivel']] = dict(info)

            elif info['tipo'] == 'volta':

                if (
                    info['nivel'] in niveis_ativos
                    and p == self.passo_atual
                ):

                    niveis_ativos[info['nivel']]['retornando'] = info['retorno']

                elif info['nivel'] in niveis_ativos:

                    del niveis_ativos[info['nivel']]

        if not niveis_ativos:
            return

        nivel_ativo = max(niveis_ativos.keys())

        # =====================================================
        # DESENHA STACK
        # =====================================================
        for nivel, dados in sorted(niveis_ativos.items()):

            y2 = base_y - (nivel * (altura_bloco + espacamento))
            y1 = y2 - altura_bloco

            x1 = 80
            x2 = largura_canvas - 80

            # -------------------------------------------------
            # ESTADOS VISUAIS
            # -------------------------------------------------
            if 'retornando' in dados:

                cor_fundo = "#4fd37c"
                cor_borda = "#4fd37c"
                cor_texto = "#000000"

                status = f"Retornando {dados['retornando']}"

            elif nivel == nivel_ativo:

                cor_fundo = "#dfe8e2"
                cor_borda = "#4fd37c"
                cor_texto = "#2d6a63"

                status = "Executando"

            else:

                cor_fundo = "#ececec"
                cor_borda = "#ececec"
                cor_texto = "#767676"

                status = "Aguardando"

            # CARD
            self.canvas_pilha.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=cor_fundo,
                outline=cor_borda,
                width=2
            )


            # TÍTULO
            titulo = (
                f"busca_binaria(inicio={dados['inicio']}, "
                f"fim={dados['fim'] + 1})"
            )

            self.canvas_pilha.create_text(
                x1 + 30,
                y1 + 32,
                anchor="w",
                text=titulo,
                font=(FONTE_TXT, 17, "bold"),
                fill="#111111"
            )

            # DETALHE
            if dados['meio'] is not None:

                detalhe = (
                    f"Meio calculado: índice {dados['meio']} "
                    f"(valor {self.vetor[dados['meio']]})"
                )

            else:

                detalhe = "Verificando limites"

            self.canvas_pilha.create_text(
                x1 + 30,
                y1 + 74,
                anchor="w",
                text=detalhe,
                font=(FONTE_TXT, 14),
                fill="#2a2a2a"
            )

            # STATUS
            self.canvas_pilha.create_text(
                x2 - 34,
                y1 + 34,
                anchor="e",
                text=status,
                font=(FONTE_TXT, 16, "italic"),
                fill=cor_texto
            )

            # TAG DA CHAMADA
            self.canvas_pilha.create_rectangle(
                x2 - 174,
                y1 + 64,
                x2 - 34,
                y1 + 106,
                outline=cor_borda,
                width=2
            )

            self.canvas_pilha.create_text(
                x2 - 104,
                y1 + 85,
                text=f"Chamada {nivel}",
                font=(FONTE_TXT, 15, "bold"),
                fill=cor_borda
            )


    def proximo_passo(self):

        if self.passo_atual < len(self.passos) - 1:

            self.passo_atual += 1
            self.atualizar_tela()

    def passo_anterior(self):

        if self.passo_atual > 0:

            self.passo_atual -= 1
            self.atualizar_tela()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppBuscaBinaria(root)
    root.update()
    app.atualizar_tela()
    root.mainloop()