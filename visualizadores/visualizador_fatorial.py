import tkinter as tk

BG           = "#FFFFFF"
BLACK = "#000000"
PANEL_BG     = "#F1F1F1"
HEADER_FG    = "#E2E8F0"
MUTED_FG     = "#64748B"
BORDER       = "#2D2D44"
ROW_NORMAL   = "#F1F1F1"
ROW_ACTIVE   = "#1E3A5F"
BASE_ROW     = "#0D3321"
BADGE_BG     = "#2D2D60"
BADGE_FG     = "#A5B4FC"
BASE_BADGE   = "#14532D"
BASE_BADGE_FG= "#86EFAC"
QMARK_FG     = "#334155"
FILLED_FG    = "#34D399"
ACCENT       = "#4ADE80"
ACCENT_HOV   = "#44A869"
BTN_SEC      = "#FFFFFF"
ACTIVE_TEXT  = "#F1F5F9"
LEGEND_BG    = "#0D1117"
LEGEND_FG    = "#CBD5E1"

FONTE_HEAD = "Cabinet Grotesk"
FONTE_TXT = "Inter"

# ═══════════════════════════════════════════════════════════
#  CONTEÚDO
# ═══════════════════════════════════════════════════════════
ETAPA1_LINHAS = [
    ("5", "fatorial(0)", "retorna 1", "#86EFAC"),  # linha 0 — topo da tela, fundo da pilha
    ("4", "fatorial(1)", "1 × ?",     "#A5B4FC"),  # linha 1
    ("3", "fatorial(2)", "2 × ?",     "#A5B4FC"),  # linha 2
    ("2", "fatorial(3)", "3 × ?",     "#A5B4FC"),  # linha 3
    ("1", "fatorial(4)", "4 × ?",     "#A5B4FC"),  # linha 4 — fundo da tela, topo da pilha
]

# Revelação de baixo pra cima: fatorial(4) primeiro (índice 4), fatorial(0) por último (índice 0)
ORDEM_REVELACAO = [4, 3, 2, 1, 0]

ETAPA1_COMENTARIOS = [
    "fatorial(0) é o CASO BASE — não faz chamada recursiva. Retorna 1 imediatamente. A recursão para aqui!",  # idx 0
    "fatorial(1) é empilhada acima — pausa e aguarda fatorial(0).",                                            # idx 1
    "fatorial(2) entra na pilha — pausa e espera o resultado de fatorial(1).",                                 # idx 2
    "fatorial(3) é empilhada — também não pode terminar sozinha, precisa de fatorial(2). Fica pausada.",       # idx 3
    "fatorial(4) é a primeira chamada — precisa de fatorial(3) para continuar, fica pausada na pilha.",        # idx 4
]

ETAPA2_PASSOS = [
    # resolve do topo da tela (fatorial(0), idx 0) descendo até fatorial(4) (idx 4)
    (1, "1", "fatorial(1) recebe 1 de volta  →  calcula 1 × 1 = 1  →  desempilha."),
    (2, "1", "fatorial(2) recebe 1 de volta  →  calcula 2 × 1 = 2  →  desempilha."),
    (3, "2", "fatorial(3) recebe 2 de volta  →  calcula 3 × 2 = 6  →  desempilha."),
    (4, "6", "fatorial(4) recebe 6 de volta  →  calcula 4 × 6 = 24  →  pilha vazia! ✓"),
]

COL_W   = [70, 260, 230]
HEADERS = ["Ordem", "Chamada atual", "O que ficou guardado"]
W, H    = 860, 640


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
        self.passo = 0

        frm_top = tk.Frame(self.root, bg=BG)
        frm_top.pack(fill="x", padx=40, pady=(30, 0))
        tk.Label(frm_top, text="ETAPA  1", font=(FONTE_TXT, 11, "bold"),
                 bg=BG, fg=ACCENT).pack(anchor="w")
        tk.Label(frm_top, text="Empilhando chamadas",
                 font=(FONTE_HEAD, 22, "bold"), bg=BG, fg=BLACK).pack(anchor="w")
        tk.Label(frm_top,
                 text="Quando a função chama outra, ela fica pausada e vai para a pilha.",
                 font=(FONTE_TXT, 12), bg=BG, fg=MUTED_FG).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=16)

        # Tabela
        self.frm_table = tk.Frame(self.root, bg=BG)
        self.frm_table.pack(padx=40, fill="x")

        for col, (h, w) in enumerate(zip(HEADERS, COL_W)):
            cell = tk.Frame(self.frm_table, bg=PANEL_BG, width=w, height=36)
            cell.grid(row=0, column=col, padx=(0, 2), pady=(0, 2))
            cell.pack_propagate(False)
            tk.Label(cell, text=h, font=(FONTE_TXT, 11, "bold"),
                     bg=PANEL_BG, fg=BLACK, anchor="w", padx=12).pack(fill="both", expand=True)

        self.row_frames = []
        self.val_labels = []

        for i, (ordem, chamada, guardado, _) in enumerate(ETAPA1_LINHAS):
            is_base = i == 0  # fatorial(0) agora é a primeira linha
            row_bg  = BASE_ROW if is_base else ROW_NORMAL
            cells   = []
            for col in range(3):
                c = tk.Frame(self.frm_table, bg=BG, width=COL_W[col], height=48)
                c.grid(row=i + 1, column=col, padx=(0, 2), pady=(0, 2))
                c.pack_propagate(False)
                cells.append(c)

            tk.Label(cells[0], text=ordem, font=(FONTE_TXT, 14),
                     bg=BG, fg=BG, anchor="w", padx=16).pack(fill="both", expand=True)

            b_bg = BASE_BADGE    if is_base else BADGE_BG
            b_fg = BASE_BADGE_FG if is_base else BADGE_FG
            outer = tk.Frame(cells[1], bg=BG)
            outer.pack(side="left", padx=14, pady=10)
            tk.Label(outer, text=f"  {chamada}  ", font=(FONTE_TXT, 13, "bold"),
                     bg=BG, fg=BG, padx=6, pady=3).pack()

            if is_base:
                tk.Label(cells[2], text=guardado, font=(FONTE_TXT, 13, "bold"),
                         bg=BG, fg=BG, anchor="w", padx=14).pack(fill="both", expand=True)
                self.val_labels.append(None)
            else:
                prefix = guardado[:-1]
                inner = tk.Frame(cells[2], bg=BG)
                inner.pack(fill="both", expand=True, padx=14)
                tk.Label(inner, text=prefix, font=(FONTE_TXT, 13),
                         bg=BG, fg=BG).pack(side="left", pady=14)
                lv = tk.Label(inner, text="?", font=(FONTE_TXT, 13, "bold"),
                              bg=BG, fg=BG)
                lv.pack(side="left", pady=14)
                self.val_labels.append(lv)

            self.row_frames.append((cells, row_bg))

        # Legenda
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(14, 0))
        self.lbl_legend = tk.Label(
            self.root,
            text="Pressione  ▶ Avançar  para revelar a primeira chamada.",
            font=(FONTE_TXT, 12, "italic"), bg=LEGEND_BG, fg=LEGEND_FG,
            wraplength=760, justify="left", anchor="w", padx=20, pady=12,
        )
        self.lbl_legend.pack(fill="x", padx=40, pady=(8, 0))

        # Contador de passos
        self.lbl_step = tk.Label(
            self.root,
            text=f"Passo  0 / {len(ETAPA1_LINHAS)}",
            font=(FONTE_TXT, 11), bg=BG, fg=MUTED_FG,
        )
        self.lbl_step.pack(pady=(6, 0))

        # Botões
        frm_btn = tk.Frame(self.root, bg=BG)
        frm_btn.pack(pady=14)

        self.btn_main = tk.Button(
            frm_btn, text="▶  Avançar",
            font=(FONTE_TXT, 13, "bold"),
            bg=ACCENT, fg="white",
            activebackground=ACCENT_HOV, activeforeground="white",
            relief="flat", padx=24, pady=8, cursor="hand2",
            command=self._avancar_e1,
        )
        self.btn_main.pack(side="left", padx=8)

        tk.Button(
            frm_btn, text="↺  Reiniciar",
            font=(FONTE_TXT, 12), bg=BTN_SEC, fg=HEADER_FG,
            activebackground="#334155", relief="flat",
            padx=18, pady=8, cursor="hand2",
            command=self._show_etapa1,
        ).pack(side="left", padx=8)

    def _avancar_e1(self):
        p = self.passo

        if p >= len(ORDEM_REVELACAO):
            return

        i = ORDEM_REVELACAO[p]          # índice real da linha a revelar
        cells, row_bg = self.row_frames[i]

        # Remove destaque da linha anterior
        if p > 0:
            prev_i = ORDEM_REVELACAO[p - 1]
            prev_cells, prev_bg = self.row_frames[prev_i]
            for c in prev_cells:
                c.configure(bg=prev_bg)
                for w in c.winfo_children():
                    self._set_bg_tree(w, prev_bg)
            lv_prev = self.val_labels[prev_i]
            if lv_prev:
                lv_prev.config(bg=prev_bg, fg=QMARK_FG)

        # Revela e destaca linha atual
        for c in cells:
            c.configure(bg=ROW_ACTIVE)
            for w in c.winfo_children():
                self._set_bg_tree(w, ROW_ACTIVE)

        # Ajusta cores dos textos
        lv = self.val_labels[i]
        if lv:
            lv.config(fg=QMARK_FG, bg=ROW_ACTIVE)

        # Corrige textos que estavam invisíveis (fg=BG)
        self._reveal_row_text(i)

        self.lbl_legend.config(text=ETAPA1_COMENTARIOS[i], fg=LEGEND_FG)
        self.passo += 1
        self.lbl_step.config(text=f"Passo  {self.passo} / {len(ETAPA1_LINHAS)}")

        # Último passo: troca botão
        if self.passo == len(ETAPA1_LINHAS):
            self.lbl_legend.config(
                text="✓  Todas as chamadas foram empilhadas. A recursão chegou ao caso base!\n"
                     "Pressione  Próxima etapa  para ver o desempilhamento.",
                fg=FILLED_FG,
            )
            self.btn_main.config(
                text="Próxima etapa  →",
                bg="#059669", activebackground="#047857",
                command=self._show_etapa2,
            )

    def _reveal_row_text(self, i):
        """Torna os widgets de texto visíveis na linha i."""
        cells, _ = self.row_frames[i]
        is_base  = i == 0

        # col 0 – número da ordem
        for w in cells[0].winfo_children():
            try: w.config(fg=MUTED_FG)
            except: pass

        # col 1 – badge
        for outer in cells[1].winfo_children():
            b_fg = BASE_BADGE_FG if is_base else BADGE_FG
            b_bg = BASE_BADGE    if is_base else BADGE_BG
            for lbl in outer.winfo_children():
                try: lbl.config(fg=b_fg, bg=b_bg)
                except: pass
            try: outer.config(bg=ROW_ACTIVE)
            except: pass

        # col 2 – valor guardado
        lv = self.val_labels[i]
        for inner in cells[2].winfo_children():
            try: inner.config(bg=ROW_ACTIVE)
            except: pass
            for w in inner.winfo_children():
                try:
                    if w is lv:
                        w.config(fg=QMARK_FG, bg=ROW_ACTIVE)
                    elif is_base:
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
        frm_top.pack(fill="x", padx=40, pady=(30, 0))
        tk.Label(frm_top, text="ETAPA  2", font=(FONTE_TXT, 11, "bold"),
                 bg=BG, fg="#34D399").pack(anchor="w")
        tk.Label(frm_top, text="Preenchendo os retornos",
                 font=(FONTE_HEAD, 22, "bold"), bg=BG, fg=HEADER_FG).pack(anchor="w")
        tk.Label(frm_top,
                 text="fatorial(0) retorna 1 — o valor sobe resolvendo cada chamada pausada.",
                 font=(FONTE_TXT, 12), bg=BG, fg=MUTED_FG).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=16)

        self.frm_table = tk.Frame(self.root, bg=BG)
        self.frm_table.pack(padx=40, fill="x")

        for col, (h, w) in enumerate(zip(HEADERS, COL_W)):
            cell = tk.Frame(self.frm_table, bg=PANEL_BG, width=w, height=36)
            cell.grid(row=0, column=col, padx=(0, 2), pady=(0, 2))
            cell.pack_propagate(False)
            tk.Label(cell, text=h, font=(FONTE_TXT, 11, "bold"),
                     bg=PANEL_BG, fg=MUTED_FG, anchor="w", padx=12).pack(fill="both", expand=True)

        self.row_frames2 = []
        self.val_labels2 = []

        for i, (ordem, chamada, guardado, _) in enumerate(ETAPA1_LINHAS):
            is_base = i == 0  # fatorial(0) é a primeira linha
            row_bg  = BASE_ROW if is_base else ROW_NORMAL
            cells   = []
            for col in range(3):
                c = tk.Frame(self.frm_table, bg=row_bg, width=COL_W[col], height=48)
                c.grid(row=i + 1, column=col, padx=(0, 2), pady=(0, 2))
                c.pack_propagate(False)
                cells.append(c)

            tk.Label(cells[0], text=ordem, font=(FONTE_TXT, 14),
                     bg=row_bg, fg=MUTED_FG, anchor="w", padx=16).pack(fill="both", expand=True)

            b_bg = BASE_BADGE    if is_base else BADGE_BG
            b_fg = BASE_BADGE_FG if is_base else BADGE_FG
            outer = tk.Frame(cells[1], bg=row_bg)
            outer.pack(side="left", padx=14, pady=10)
            tk.Label(outer, text=f"  {chamada}  ", font=(FONTE_TXT, 13, "bold"),
                     bg=b_bg, fg=b_fg, padx=6, pady=3).pack()

            if is_base:
                tk.Label(cells[2], text=guardado, font=(FONTE_TXT, 13, "bold"),
                         bg=row_bg, fg=BASE_BADGE_FG, anchor="w", padx=14).pack(fill="both", expand=True)
                self.val_labels2.append(None)
            else:
                prefix = guardado[:-1]
                inner = tk.Frame(cells[2], bg=row_bg)
                inner.pack(fill="both", expand=True, padx=14)
                tk.Label(inner, text=prefix, font=(FONTE_TXT, 13),
                         bg=row_bg, fg=ACTIVE_TEXT).pack(side="left", pady=14)
                lv = tk.Label(inner, text="?", font=(FONTE_TXT, 13, "bold"),
                              bg=row_bg, fg=QMARK_FG)
                lv.pack(side="left", pady=14)
                self.val_labels2.append(lv)

            self.row_frames2.append((cells, row_bg))

        # Legenda
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(14, 0))
        self.lbl_legend = tk.Label(
            self.root,
            text="Pressione  ▶ Avançar  para desempilhar o primeiro retorno.",
            font=(FONTE_TXT, 12, "italic"), bg=LEGEND_BG, fg=LEGEND_FG,
            wraplength=760, justify="left", anchor="w", padx=20, pady=12,
        )
        self.lbl_legend.pack(fill="x", padx=40, pady=(8, 0))

        self.lbl_step = tk.Label(
            self.root,
            text=f"Passo  0 / {len(ETAPA2_PASSOS)}",
            font=(FONTE_TXT, 11), bg=BG, fg=MUTED_FG,
        )
        self.lbl_step.pack(pady=(6, 0))

        frm_btn = tk.Frame(self.root, bg=BG)
        frm_btn.pack(pady=14)

        self.btn_main = tk.Button(
            frm_btn, text="▶  Avançar",
            font=(FONTE_TXT, 13, "bold"),
            bg=ACCENT, fg="white",
            activebackground=ACCENT_HOV, activeforeground="white",
            relief="flat", padx=24, pady=8, cursor="hand2",
            command=self._avancar_e2,
        )
        self.btn_main.pack(side="left", padx=8)

        tk.Button(
            frm_btn, text="↺  Recomeçar do início",
            font=(FONTE_TXT, 12), bg=BTN_SEC, fg=HEADER_FG,
            activebackground="#334155", relief="flat",
            padx=18, pady=8, cursor="hand2",
            command=self._show_etapa1,
        ).pack(side="left", padx=8)

    def _avancar_e2(self):
        p = self.passo

        # Remove destaque anterior
        if p > 0:
            prev_idx = ETAPA2_PASSOS[p - 1][0]
            prev_cells, prev_bg = self.row_frames2[prev_idx]
            for c in prev_cells:
                c.configure(bg=prev_bg)
                for w in c.winfo_children():
                    self._set_bg_tree(w, prev_bg)
            lv = self.val_labels2[prev_idx]
            if lv:
                lv.config(bg=prev_bg)

        if p >= len(ETAPA2_PASSOS):
            return

        idx, valor, msg = ETAPA2_PASSOS[p]
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
        self.lbl_step.config(text=f"Passo  {self.passo} / {len(ETAPA2_PASSOS)}")

        if self.passo == len(ETAPA2_PASSOS):
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
