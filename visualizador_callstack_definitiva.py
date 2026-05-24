import tkinter as tk

# ═══════════════════════════════════════════════════════════
#  PALETA
# ═══════════════════════════════════════════════════════════
BG            = "#0F0F1A"
PANEL_BG      = "#1A1A2E"
HEADER_FG     = "#E2E8F0"
MUTED_FG      = "#64748B"
BORDER        = "#2D2D44"
ROW_NORMAL    = "#16213E"
ROW_ACTIVE    = "#1E3A5F"
BASE_ROW      = "#0D3321"
BADGE_BG      = "#2D2D60"
BADGE_FG      = "#A5B4FC"
BASE_BADGE    = "#14532D"
BASE_BADGE_FG = "#86EFAC"
QMARK_FG      = "#334155"
FILLED_FG     = "#34D399"
ACCENT        = "#6366F1"
ACCENT_HOV    = "#4F46E5"
BTN_SEC       = "#1E293B"
ACTIVE_TEXT   = "#F1F5F9"
LEGEND_BG     = "#0D1117"
LEGEND_FG     = "#CBD5E1"

# ═══════════════════════════════════════════════════════════
#  CONTEÚDO
# pilha começa de baixo: índice 0 = base (fatorial(0)), índice 4 = topo (fatorial(4))
# ═══════════════════════════════════════════════════════════

# Ordem visual de cima pra baixo na tela = topo da pilha primeiro
# Mas revelamos de BAIXO pra CIMA (índice 4 primeiro na tela = último a ser revelado)
# Linhas na tela: fatorial(4) no topo visual, fatorial(0) embaixo
# Revelação: fatorial(0) primeiro → fatorial(4) por último  ← comportamento de pilha

LINHAS = [
    # (ordem_visual, chamada,       prefixo_guardado, é_base)
    ("5", "fatorial(4)", "4 * fact(3)",  False),
    ("4", "fatorial(3)", "3 * fact(2)",  False),
    ("3", "fatorial(2)", "2 * fact(1)",  False),
    ("2", "fatorial(1)", "1 * fact(0)",  False),
    ("1", "fatorial(0)", "retorna 1",    True ),
]

# índices na lista LINHAS (0=fatorial(4), 4=fatorial(0))
# revelação de cima pra baixo na tela = do índice 0 ao 4
# porque fatorial(4) é chamada primeiro e vai descendo até o caso base
ORDEM_REVELACAO_E1 = [0, 1, 2, 3, 4]

COMENTARIOS_E1 = {
    0: "fatorial(4) é a primeira chamada — ela precisa de fatorial(3) para calcular 4 * fact(3). Fica pausada na pilha.",
    1: "fatorial(3) é chamada por fatorial(4) — precisa de fatorial(2) para calcular 3 * fact(2). Fica pausada.",
    2: "fatorial(2) é chamada por fatorial(3) — precisa de fatorial(1) para calcular 2 * fact(1). Fica pausada.",
    3: "fatorial(1) é chamada por fatorial(2) — precisa de fatorial(0) para calcular 1 * fact(0). Fica pausada.",
    4: "fatorial(0) é o CASO BASE — não faz chamada recursiva. Retorna 1 imediatamente. A recursão para aqui!",
}

# Etapa 2: desempilha do topo (índice 0 na tela = fatorial(4)) para baixo
# mas o primeiro a RESOLVER é o fatorial(0) que já tem valor → sobe de baixo pra cima
PASSOS_E2 = [
    # (índice na lista LINHAS, valor preenchido, legenda)
    (3, "1",  "fatorial(1) recebe 1 de volta  →  calcula 1 * fact(0) = 1 * 1 = 1  →  desempilha."),
    (2, "1",  "fatorial(2) recebe 1 de volta  →  calcula 2 * fact(1) = 2 * 1 = 2  →  desempilha."),
    (1, "2",  "fatorial(3) recebe 2 de volta  →  calcula 3 * fact(2) = 3 * 2 = 6  →  desempilha."),
    (0, "6",  "fatorial(4) recebe 6 de volta  →  calcula 4 * fact(3) = 4 * 6 = 24  →  pilha vazia! ✓"),
]

COL_W   = [70, 240, 260]
HEADERS = ["Ordem", "Chamada atual", "O que ficou guardado"]
W, H    = 880, 660


# ═══════════════════════════════════════════════════════════
#  APLICAÇÃO
# ═══════════════════════════════════════════════════════════
class App:
    def __init__(self, root):
        self.root = root
        root.title("Visualizador da Call Stack — Fatorial Recursivo")
        root.configure(bg=BG)
        root.resizable(False, False)
        cx = (root.winfo_screenwidth()  - W) // 2
        cy = (root.winfo_screenheight() - H) // 2
        root.geometry(f"{W}x{H}+{cx}+{cy}")
        self._show_etapa1()

    # ───────────────────────────────────────────────────────
    #  ETAPA 1
    # ───────────────────────────────────────────────────────
    def _show_etapa1(self):
        self._clear()
        self.passo = 0          # índice em ORDEM_REVELACAO_E1

        frm_top = tk.Frame(self.root, bg=BG)
        frm_top.pack(fill="x", padx=40, pady=(28, 0))
        tk.Label(frm_top, text="ETAPA  1", font=("Courier", 11, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w")
        tk.Label(frm_top, text="Empilhando chamadas",
                 font=("Georgia", 22, "bold"), bg=BG, fg=HEADER_FG).pack(anchor="w")
        tk.Label(frm_top,
                 text="A função começa em fatorial(4) e vai chamando a si mesma até chegar no caso base.",
                 font=("Helvetica", 12), bg=BG, fg=MUTED_FG).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=14)

        # Tabela
        self.frm_table = tk.Frame(self.root, bg=BG)
        self.frm_table.pack(padx=40, fill="x")

        for col, (h, w) in enumerate(zip(HEADERS, COL_W)):
            cell = tk.Frame(self.frm_table, bg=PANEL_BG, width=w, height=36)
            cell.grid(row=0, column=col, padx=(0, 2), pady=(0, 2))
            cell.pack_propagate(False)
            tk.Label(cell, text=h, font=("Helvetica", 11, "bold"),
                     bg=PANEL_BG, fg=MUTED_FG, anchor="w", padx=12).pack(fill="both", expand=True)

        self.row_frames = []   # (cells, orig_bg) para cada linha
        self.val_labels = []   # Label do valor animado (ou None se base)

        for i, (ordem, chamada, guardado, is_base) in enumerate(LINHAS):
            row_bg = BASE_ROW if is_base else ROW_NORMAL
            cells  = []
            for col in range(3):
                c = tk.Frame(self.frm_table, bg=BG, width=COL_W[col], height=48)
                c.grid(row=i + 1, column=col, padx=(0, 2), pady=(0, 2))
                c.pack_propagate(False)
                cells.append(c)

            # col 0
            tk.Label(cells[0], text=ordem, font=("Helvetica", 14),
                     bg=BG, fg=BG, anchor="w", padx=16).pack(fill="both", expand=True)

            # col 1 – badge
            b_bg = BASE_BADGE    if is_base else BADGE_BG
            b_fg = BASE_BADGE_FG if is_base else BADGE_FG
            outer = tk.Frame(cells[1], bg=BG)
            outer.pack(side="left", padx=14, pady=10)
            tk.Label(outer, text=f"  {chamada}  ", font=("Courier", 13, "bold"),
                     bg=BG, fg=BG, padx=6, pady=3).pack()

            # col 2 – guardado
            if is_base:
                tk.Label(cells[2], text=guardado, font=("Courier", 13, "bold"),
                         bg=BG, fg=BG, anchor="w", padx=14).pack(fill="both", expand=True)
                self.val_labels.append(None)
            else:
                # "4 * fact(3)" → mostra tudo, sem "?"
                # O "?" aparece ANTES de revelar; depois mostra texto completo
                inner = tk.Frame(cells[2], bg=BG)
                inner.pack(fill="both", expand=True, padx=14)
                lv = tk.Label(inner, text=guardado, font=("Courier", 13, "bold"),
                              bg=BG, fg=BG)
                lv.pack(side="left", pady=14)
                self.val_labels.append(lv)

            self.row_frames.append((cells, row_bg))

        # Legenda
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(12, 0))
        self.lbl_legend = tk.Label(
            self.root,
            text="Pressione  ▶ Avançar  para empilhar a primeira chamada.",
            font=("Helvetica", 15, "italic"), bg=LEGEND_BG, fg=LEGEND_FG,
            wraplength=800, justify="left", anchor="w", padx=20, pady=14,
        )
        self.lbl_legend.pack(fill="x", padx=40, pady=(8, 0))

        self.lbl_step = tk.Label(self.root,
            text=f"Passo  0 / {len(LINHAS)}",
            font=("Courier", 12), bg=BG, fg=MUTED_FG)
        self.lbl_step.pack(pady=(6, 0))

        frm_btn = tk.Frame(self.root, bg=BG)
        frm_btn.pack(pady=14)

        self.btn_main = tk.Button(
            frm_btn, text="▶  Avançar",
            font=("Helvetica", 13, "bold"), bg=ACCENT, fg="white",
            activebackground=ACCENT_HOV, activeforeground="white",
            relief="flat", padx=24, pady=8, cursor="hand2",
            command=self._avancar_e1,
        )
        self.btn_main.pack(side="left", padx=8)

        tk.Button(frm_btn, text="↺  Reiniciar",
            font=("Helvetica", 12), bg=BTN_SEC, fg=HEADER_FG,
            activebackground="#334155", relief="flat",
            padx=18, pady=8, cursor="hand2",
            command=self._show_etapa1,
        ).pack(side="left", padx=8)

    def _avancar_e1(self):
        if self.passo >= len(ORDEM_REVELACAO_E1):
            return

        linha_idx = ORDEM_REVELACAO_E1[self.passo]
        cells, row_bg = self.row_frames[linha_idx]

        # Remove destaque da linha anterior
        if self.passo > 0:
            prev_idx = ORDEM_REVELACAO_E1[self.passo - 1]
            prev_cells, prev_bg = self.row_frames[prev_idx]
            for c in prev_cells:
                c.configure(bg=prev_bg)
                for w in c.winfo_children():
                    self._set_bg_tree(w, prev_bg)
            lv_p = self.val_labels[prev_idx]
            if lv_p:
                lv_p.config(bg=prev_bg)

        # Revela linha com destaque ativo
        for c in cells:
            c.configure(bg=ROW_ACTIVE)
            for w in c.winfo_children():
                self._set_bg_tree(w, ROW_ACTIVE)

        self._reveal_text(linha_idx)

        self.lbl_legend.config(text=COMENTARIOS_E1[linha_idx], fg=LEGEND_FG)
        self.passo += 1
        self.lbl_step.config(text=f"Passo  {self.passo} / {len(LINHAS)}")

        if self.passo == len(LINHAS):
            self.lbl_legend.config(
                text="✓  Chegamos ao caso base! Todas as chamadas estão pausadas na pilha.\n"
                     "Pressione  Próxima etapa  para ver o desempilhamento.",
                fg=FILLED_FG,
            )
            self.btn_main.config(
                text="Próxima etapa  →",
                bg="#059669", activebackground="#047857",
                command=self._show_etapa2,
            )

    def _reveal_text(self, i):
        is_base = LINHAS[i][3]
        cells, _ = self.row_frames[i]

        # col 0
        for w in cells[0].winfo_children():
            try: w.config(fg=MUTED_FG, bg=ROW_ACTIVE)
            except: pass

        # col 1 – badge
        b_fg = BASE_BADGE_FG if is_base else BADGE_FG
        b_bg = BASE_BADGE    if is_base else BADGE_BG
        for outer in cells[1].winfo_children():
            try: outer.config(bg=ROW_ACTIVE)
            except: pass
            for lbl in outer.winfo_children():
                try: lbl.config(fg=b_fg, bg=b_bg)
                except: pass

        # col 2
        lv = self.val_labels[i]
        for inner in cells[2].winfo_children():
            try: inner.config(bg=ROW_ACTIVE)
            except: pass
            for w in inner.winfo_children():
                try:
                    if is_base:
                        w.config(fg=BASE_BADGE_FG, bg=ROW_ACTIVE)
                    else:
                        w.config(fg=ACTIVE_TEXT, bg=ROW_ACTIVE)
                except: pass

    # ───────────────────────────────────────────────────────
    #  ETAPA 2
    # ───────────────────────────────────────────────────────
    def _show_etapa2(self):
        self._clear()
        self.passo = 0

        frm_top = tk.Frame(self.root, bg=BG)
        frm_top.pack(fill="x", padx=40, pady=(28, 0))
        tk.Label(frm_top, text="ETAPA  2", font=("Courier", 11, "bold"),
                 bg=BG, fg="#34D399").pack(anchor="w")
        tk.Label(frm_top, text="Preenchendo os retornos",
                 font=("Georgia", 22, "bold"), bg=BG, fg=HEADER_FG).pack(anchor="w")
        tk.Label(frm_top,
                 text="A pilha desempilha de baixo para cima — o caso base resolve primeiro e o valor sobe.",
                 font=("Helvetica", 12), bg=BG, fg=MUTED_FG).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=14)

        self.frm_table = tk.Frame(self.root, bg=BG)
        self.frm_table.pack(padx=40, fill="x")

        for col, (h, w) in enumerate(zip(HEADERS, COL_W)):
            cell = tk.Frame(self.frm_table, bg=PANEL_BG, width=w, height=36)
            cell.grid(row=0, column=col, padx=(0, 2), pady=(0, 2))
            cell.pack_propagate(False)
            tk.Label(cell, text=h, font=("Helvetica", 11, "bold"),
                     bg=PANEL_BG, fg=MUTED_FG, anchor="w", padx=12).pack(fill="both", expand=True)

        self.row_frames2 = []
        self.val_labels2 = []

        for i, (ordem, chamada, guardado, is_base) in enumerate(LINHAS):
            row_bg = BASE_ROW if is_base else ROW_NORMAL
            cells  = []
            for col in range(3):
                c = tk.Frame(self.frm_table, bg=row_bg, width=COL_W[col], height=48)
                c.grid(row=i + 1, column=col, padx=(0, 2), pady=(0, 2))
                c.pack_propagate(False)
                cells.append(c)

            tk.Label(cells[0], text=ordem, font=("Helvetica", 14),
                     bg=row_bg, fg=MUTED_FG, anchor="w", padx=16).pack(fill="both", expand=True)

            b_bg = BASE_BADGE    if is_base else BADGE_BG
            b_fg = BASE_BADGE_FG if is_base else BADGE_FG
            outer = tk.Frame(cells[1], bg=row_bg)
            outer.pack(side="left", padx=14, pady=10)
            tk.Label(outer, text=f"  {chamada}  ", font=("Courier", 13, "bold"),
                     bg=b_bg, fg=b_fg, padx=6, pady=3).pack()

            if is_base:
                tk.Label(cells[2], text=guardado, font=("Courier", 13, "bold"),
                         bg=row_bg, fg=BASE_BADGE_FG, anchor="w", padx=14).pack(fill="both", expand=True)
                self.val_labels2.append(None)
            else:
                # Na etapa 2 mostramos "N * fact(?) " com o ? substituído pelo valor
                # Separa prefixo "N * fact(" e sufixo ")"
                # guardado ex: "4 * fact(3)"  → vamos mostrar com valor preenchido
                inner = tk.Frame(cells[2], bg=row_bg)
                inner.pack(fill="both", expand=True, padx=14)

                # Extrai partes: "4 * fact(" e "3" e ")"
                # formato: "N * fact(M)"
                left_part  = guardado[:guardado.index("(") + 1]   # "4 * fact("
                right_part = ")"

                tk.Label(inner, text=left_part, font=("Courier", 13, "bold"),
                         bg=row_bg, fg=ACTIVE_TEXT).pack(side="left", pady=14)
                lv = tk.Label(inner, text="?", font=("Courier", 13, "bold"),
                              bg=row_bg, fg=QMARK_FG)
                lv.pack(side="left", pady=14)
                tk.Label(inner, text=right_part, font=("Courier", 13, "bold"),
                         bg=row_bg, fg=ACTIVE_TEXT).pack(side="left", pady=14)

                self.val_labels2.append(lv)

            self.row_frames2.append((cells, row_bg))

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(12, 0))
        self.lbl_legend = tk.Label(
            self.root,
            text="Pressione  ▶ Avançar  para resolver o primeiro retorno.",
            font=("Helvetica", 15, "italic"), bg=LEGEND_BG, fg=LEGEND_FG,
            wraplength=800, justify="left", anchor="w", padx=20, pady=14,
        )
        self.lbl_legend.pack(fill="x", padx=40, pady=(8, 0))

        self.lbl_step = tk.Label(self.root,
            text=f"Passo  0 / {len(PASSOS_E2)}",
            font=("Courier", 12), bg=BG, fg=MUTED_FG)
        self.lbl_step.pack(pady=(6, 0))

        frm_btn = tk.Frame(self.root, bg=BG)
        frm_btn.pack(pady=14)

        self.btn_main = tk.Button(
            frm_btn, text="▶  Avançar",
            font=("Helvetica", 13, "bold"), bg=ACCENT, fg="white",
            activebackground=ACCENT_HOV, activeforeground="white",
            relief="flat", padx=24, pady=8, cursor="hand2",
            command=self._avancar_e2,
        )
        self.btn_main.pack(side="left", padx=8)

        tk.Button(frm_btn, text="↺  Recomeçar do início",
            font=("Helvetica", 12), bg=BTN_SEC, fg=HEADER_FG,
            activebackground="#334155", relief="flat",
            padx=18, pady=8, cursor="hand2",
            command=self._show_etapa1,
        ).pack(side="left", padx=8)

    def _avancar_e2(self):
        p = self.passo

        if p > 0:
            prev_idx = PASSOS_E2[p - 1][0]
            prev_cells, prev_bg = self.row_frames2[prev_idx]
            for c in prev_cells:
                c.configure(bg=prev_bg)
                for w in c.winfo_children():
                    self._set_bg_tree(w, prev_bg)
            lv = self.val_labels2[prev_idx]
            if lv:
                lv.config(bg=prev_bg)

        if p >= len(PASSOS_E2):
            return

        idx, valor, msg = PASSOS_E2[p]
        cells, _ = self.row_frames2[idx]

        for c in cells:
            c.configure(bg=ROW_ACTIVE)
            for w in c.winfo_children():
                self._set_bg_tree(w, ROW_ACTIVE)

        lv = self.val_labels2[idx]
        if lv:
            lv.config(text=valor, fg=FILLED_FG, bg=ROW_ACTIVE)

        self.lbl_legend.config(text=msg, fg=LEGEND_FG)
        self.passo += 1
        self.lbl_step.config(text=f"Passo  {self.passo} / {len(PASSOS_E2)}")

        if self.passo == len(PASSOS_E2):
            self.lbl_legend.config(
                text="✓  Pilha vazia!  Resultado final:  4! = 4 × 3 × 2 × 1 = 24",
                fg=FILLED_FG,
            )
            self.btn_main.config(
                text="↺  Recomeçar do início",
                bg=BTN_SEC, fg=HEADER_FG,
                activebackground="#334155",
                command=self._show_etapa1,
            )

    # ───────────────────────────────────────────────────────
    #  UTILIDADES
    # ───────────────────────────────────────────────────────
    def _set_bg_tree(self, widget, color):
        try:
            widget.configure(bg=color)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._set_bg_tree(child, color)

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
