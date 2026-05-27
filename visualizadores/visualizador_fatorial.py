import tkinter as tk

BG          = "#FFFFFF"
BLACK       = "#111111"
MUTED_FG    = "#888888"
BORDER      = "#E0E0E0"

# Tabela — header
HDR_BG      = "#F5F5F5"
HDR_FG      = "#333333"

# Linha normal (ainda não revelada / não ativa)
ROW_BG      = "#F9F9F9"
ROW_FG      = "#AAAAAA"   # texto esmaecido

# Linha resolvida (desempilhada) — verde escuro
DONE_BG     = "#1B5E3B"
DONE_FG     = "#6EE7A0"

# Linha ativa — verde claro (mint)
ACTIVE_BG   = "#E8F8EF"
ACTIVE_FG   = "#1B5E3B"
ACTIVE_BD   = "#3BB06A"

#escondido
HIDDEN = "#FFFFFF"

# Badge ETAPA
BADGE_FG    = "#3BB06A"

# Botões
BTN_GHOST_BG  = "#FFFFFF"
BTN_GHOST_FG  = "#333333"
BTN_GHOST_BD  = "#CCCCCC"
BTN_GREEN_BG  = "#3BB06A"
BTN_GREEN_FG  = "#FFFFFF"
BTN_GREEN_HOV = "#2E9A5A"

FONTE_HEAD = "Cabinet Grotesk"
FONTE = "Inter"

W, H = 820, 540

def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)

E1_PASSOS = [
    # passo 0 — estado inicial (nada revelado)
    [
        ("4", "fatorial(1)", "Retorna 1",     "hidden"),
        ("3", "fatorial(2)", "2 × ?",     "hidden"),
        ("2", "fatorial(3)", "3 × ?",     "hidden"),
        ("1", "fatorial(4)", "4 × ?",     "hidden"),
    ],
    # passo 1 — revela fatorial(4) (idx 4)
    [
        ("4", "fatorial(1)", "Retorna 1",     "hidden"),
        ("3", "fatorial(2)", "2 × ?",     "hidden"),
        ("2", "fatorial(3)", "3 × ?",     "hidden"),
        ("1", "fatorial(4)", "4 × ?",     "active"),
    ],
    # passo 2
    [
        ("4", "fatorial(1)", "Retorna 1",     "hidden"),
        ("3", "fatorial(2)", "2 × ?",     "hidden"),
        ("2", "fatorial(3)", "3 × ?",     "active"),
        ("1", "fatorial(4)", "4 × ?",     "waiting"),
    ],
    # passo 3
    [
        ("4", "fatorial(1)", "Retorna 1",     "hidden"),
        ("3", "fatorial(2)", "2 × ?",     "active"),
        ("2", "fatorial(3)", "3 × ?",     "waiting"),
        ("1", "fatorial(4)", "4 × ?",     "waiting"),
    ],
    # passo 4
    [
        ("4", "fatorial(1)", "Retorna 1",     "active"),
        ("3", "fatorial(2)", "2 × ?",     "waiting"),
        ("2", "fatorial(3)", "3 × ?",     "waiting"),
        ("1", "fatorial(4)", "4 × ?",     "waiting"),
    ],
]

# Etapa 2 — desempilhamento
E2_PASSOS = [

    # passo 1 — fatorial(1) resolve
    [
        ("4", "fatorial(1)", "Retorna 1", "done"),
        ("3", "fatorial(2)", "2 × ?",       "waiting"),
        ("2", "fatorial(3)", "3 × ?",       "waiting"),
        ("1", "fatorial(4)", "4 × ?",       "waiting"),
    ],
    # passo 2 — fatorial(1) done, fatorial(2) resolve
    [
        ("4", "fatorial(1)", "Retorna 1", "done"),
        ("3", "fatorial(2)", "2×1 = 2",     "active"),
        ("2", "fatorial(3)", "3 × ?",       "waiting"),
        ("1", "fatorial(4)", "4 × ?",       "waiting"),
    ],
    # passo 3
    [
        ("4", "fatorial(1)", "Retorna 1", "done"),
        ("3", "fatorial(2)", "Retorna 2",   "done"),
        ("2", "fatorial(3)", "3×2 = 6",     "active"),
        ("1", "fatorial(4)", "4 × ?",       "waiting"),
    ],
    # passo 4 — final
    [
        ("4", "fatorial(1)", "Retorna 1", "done"),
        ("3", "fatorial(2)", "Retorna 2",   "done"),
        ("2", "fatorial(3)", "Retorna 6",   "done"),
        ("1", "fatorial(4)", "4×6 = 24 ✓", "active"),
    ],
]

COL_W   = [100, 280, 260]
HEADERS = ["Ordem", "Chamada atual", "Retorno"]


class App:
    def __init__(self, root):
        self.root = root
        root.title("Call Stack — Fatorial Recursivo")
        root.configure(bg=BG)
        root.resizable(False, False)
        cx = (root.winfo_screenwidth()  - W) // 2
        cy = (root.winfo_screenheight() - H) // 2
        root.geometry(f"{W}x{H}+{cx}+{cy}")
        self._show(1, E1_PASSOS, 0)

    def _show(self, etapa, passos, passo_idx):
        self._clear()
        self.etapa     = etapa
        self.passos    = passos
        self.passo_idx = passo_idx
        total          = len(passos) - 1   

        # ── CARD PRINCIPAL ──────────────────────────────
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=48, pady=36)

        # Header card
        card_hdr = tk.Frame(outer, bg=BG, highlightbackground=BORDER,
                            highlightthickness=1)
        card_hdr.pack(fill="x")

        tk.Label(card_hdr,
                 text="Pilha de chamadas  fatorial de 4",
                 font=(FONTE_HEAD, 16, "bold"), bg=BG, fg=BLACK,
                 anchor="w", padx=20, pady=16).pack(side="left")

        tk.Label(card_hdr,
                 text=f"ETAPA {etapa}",
                 font=(FONTE, 11, "bold"), bg=BG, fg=BADGE_FG,
                 anchor="e", padx=20).pack(side="right")

        tk.Frame(outer, bg=BG, height=20).pack()  # spacer

        # ── TABELA ──────────────────────────────────────
        tbl = tk.Frame(outer, bg=BG, highlightbackground=BORDER,
                       highlightthickness=1)
        tbl.pack(fill="x")

        # Header row
        for col, (h, cw) in enumerate(zip(HEADERS, COL_W)):
            cell = tk.Frame(tbl, bg=HDR_BG, width=cw, height=40,
                            highlightbackground=BORDER, highlightthickness=1)
            cell.grid(row=0, column=col, sticky="nsew")
            cell.pack_propagate(False)
            tk.Label(cell, text=h, font=(FONTE, 11, "bold"),
                     bg=HDR_BG, fg=HDR_FG,
                     anchor="w" if col == 0 else "center",
                     padx=16).pack(fill="both", expand=True)

        # Data rows
        estado_atual = passos[passo_idx]
        for row_i, (ordem, chamada, guardado, estado) in enumerate(estado_atual):
            if estado == "done":
                rbg, rfg, bd = DONE_BG, DONE_FG, DONE_BG
            elif estado == "active":
                rbg, rfg, bd = ACTIVE_BG, ACTIVE_FG, ACTIVE_BD
            elif estado == "hidden":   
                rbg, rfg, bd = HIDDEN, HIDDEN, HIDDEN
            else:
                rbg, rfg, bd = ROW_BG, ROW_FG, BORDER

            for col in range(3):
                cell = tk.Frame(tbl, bg=rbg, width=COL_W[col], height=50,
                                highlightbackground=bd, highlightthickness=1)
                cell.grid(row=row_i + 1, column=col, sticky="nsew")
                cell.pack_propagate(False)

                if col == 0:
                    tk.Label(cell, text=ordem,
                             font=(FONTE, 14, "bold"),
                             bg=rbg, fg=rfg,
                             anchor="center").pack(fill="both", expand=True)
                elif col == 1:
                    tk.Label(cell, text=chamada,
                             font=(FONTE, 13, "bold"),
                             bg=rbg, fg=rfg,
                             anchor="center").pack(fill="both", expand=True)
                else:
                    # col 2 — destaca o resultado calculado em verde
                    if estado == "active" and "=" in guardado:
                        # split em " = "
                        parts = guardado.split(" = ")
                        inner = tk.Frame(cell, bg=rbg)
                        inner.place(relx=0.5, rely=0.5, anchor="center")
                        tk.Label(inner, text=parts[0] + " = ",
                                 font=(FONTE, 13), bg=rbg, fg=rfg
                                 ).pack(side="left")
                        tk.Label(inner, text=parts[1],
                                 font=(FONTE, 13, "bold"), bg=rbg,
                                 fg=ACTIVE_BD).pack(side="left")
                    else:
                        tk.Label(cell, text=guardado,
                                 font=(FONTE, 13,
                                       "bold" if estado in ("done","active") else "normal"),
                                 bg=rbg, fg=rfg,
                                 anchor="center").pack(fill="both", expand=True)

        tk.Frame(outer, bg=BG, height=28).pack()  # spacer

        # ── BARRA DE NAVEGAÇÃO ───────────────────────────
        nav = tk.Frame(outer, bg=BG)
        nav.pack(fill="x")

        # Botão ← Passo Anterior
        btn_prev = tk.Button(
            nav, text="←  Passo Anterior",
            font=(FONTE, 12),
            bg=BTN_GHOST_BG, fg=BTN_GHOST_FG,
            activebackground="#F0F0F0", activeforeground=BLACK,
            relief="solid", bd=1, padx=20, pady=10,
            cursor="hand2" if passo_idx > 0 else "arrow",
            state="normal" if passo_idx > 0 else "disabled",
            command=lambda: self._nav(-1),
        )
        btn_prev.pack(side="left")

        # Passo X de Y — centro
        lbl_mid = tk.Label(
            nav,
            text=f"Passo {passo_idx} de {total}",
            font=(FONTE, 12), bg=BG, fg=MUTED_FG,
        )
        lbl_mid.pack(side="left", expand=True)

        # Botão Próximo Passo →  /  Próxima Etapa  /  Recomeçar
        is_last_e1 = (etapa == 1 and passo_idx == total)
        is_last_e2 = (etapa == 2 and passo_idx == total)

        if is_last_e2:
            btn_lbl = "↺  Recomeçar"
            btn_cmd = lambda: self._show(1, E1_PASSOS, 0)
        elif is_last_e1:
            btn_lbl = "Próxima Etapa  →"
            btn_cmd = lambda: self._show(2, E2_PASSOS, 0)
        else:
            btn_lbl = "Próximo Passo  →"
            btn_cmd = lambda: self._nav(+1)

        tk.Button(
            nav, text=btn_lbl,
            font=(FONTE, 12, "bold"),
            bg=BTN_GREEN_BG, fg=BTN_GREEN_FG,
            activebackground=BTN_GREEN_HOV, activeforeground=BTN_GREEN_FG,
            relief="flat", padx=24, pady=10,
            cursor="hand2",
            command=btn_cmd,
        ).pack(side="right")

    def _nav(self, delta):
        new_idx = self.passo_idx + delta
        new_idx = max(0, min(new_idx, len(self.passos) - 1))
        self._show(self.etapa, self.passos, new_idx)

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()