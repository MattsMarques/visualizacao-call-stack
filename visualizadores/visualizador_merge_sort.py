"""
Visualizador de Call Stack — Merge Sort
Design: fiel ao wireframe, Cabinet Grotesk + Inter, #4ADE80 / #276B61
Vetor: [14, 7, 3, 12]
"""

import tkinter as tk
from tkinter import font as tkfont
import array

# ══════════════════════════════════════════════════════
#  PALETA
# ══════════════════════════════════════════════════════
FUNDO        = "#F9F9F9"
BRANCO       = "#FFFFFF"
BORDA        = "#E2E2E2"
BORDA_FORTE  = "#C8C8C8"

VERDE        = "#4ADE80"   # destaque principal
VERDE_ESCURO = "#276B61"   # texto/ícone sobre verde
VERDE_BG     = "#EDFAF3"   # fundo frame ativo

CINZA_TEXTO  = "#1A1A1A"
CINZA_MED    = "#6B7280"
CINZA_LEVE   = "#9CA3AF"
CINZA_FRAME  = "#F3F3F3"   # frame inativo (abaixo)

# células do vetor
COR_ESQ_BG   = "#FEF9C3"   # amarelo claro  (lado esquerdo)
COR_ESQ_BD   = "#EAB308"   # amarelo borda
COR_ESQ_TX   = "#92400E"
COR_DIR_BG   = "#DBEAFE"   # azul claro     (lado direito)
COR_DIR_BD   = "#3B82F6"
COR_DIR_TX   = "#1E3A8A"
COR_NEU_BG   = "#F3F4F6"   # neutro (antes do split)
COR_NEU_BD   = "#D1D5DB"
COR_NEU_TX   = "#374151"
COR_OK_BG    = "#DCFCE7"   # verde (resultado ordenado)
COR_OK_BD    = "#22C55E"
COR_OK_TX    = "#166534"

FONTE_HEAD   = "Cabinet Grotesk"
FONTE_TXT    = "Inter"

# ══════════════════════════════════════════════════════
#  TRACER — gera lista compacta de passos
# ══════════════════════════════════════════════════════
class Tracer:
    """
    Produz passos compactos focados exclusivamente na call stack:
    - PUSH: nova chamada empurrada na pilha
    - SPLIT: mostra v_esq / v_dir dentro do frame
    - POP: chamada retorna (com resultado)
    Chamadas de 'copiar' são mostradas como anotação textual,
    sem passo separado — reduz o total de passos.
    """
    def __init__(self, dados):
        self.passos = []
        self._id = 0
        v = array.array("i", dados)
        self._ms(v, len(v), pai=None, prof=0, lado="RAIZ")

    def _novo_id(self):
        self._id += 1
        return self._id

    def _push(self, **kw):
        self.passos.append({"tipo": "PUSH", **kw})

    def _split(self, **kw):
        self.passos.append({"tipo": "SPLIT", **kw})

    def _pop(self, **kw):
        self.passos.append({"tipo": "POP", **kw})

    def _ms(self, vetor, fim, pai, prof, lado):
        cid = self._novo_id()

        # PUSH — nova chamada na pilha
        self._push(cid=cid, pai=pai, prof=prof, lado=lado,
                   vetor=list(vetor), fim=fim)

        if fim <= 1:
            # caso base: pop imediato
            self._pop(cid=cid, pai=pai, prof=prof,
                      resultado=list(vetor), base=True)
            return vetor

        meio = fim // 2
        v_esq = array.array("i", vetor[0:meio])
        v_dir = array.array("i", vetor[meio:fim])

        # SPLIT — mostra as duas metades no frame
        self._split(cid=cid, prof=prof,
                    v_esq=list(v_esq), v_dir=list(v_dir),
                    meio=meio, fim=fim, vetor=list(vetor))

        ord_esq = self._ms(v_esq, meio,        pai=cid, prof=prof+1, lado="ESQ")
        ord_dir = self._ms(v_dir, meio+(fim%2), pai=cid, prof=prof+1, lado="DIR")

        # merge
        tam_esq = meio
        tam_dir = meio + (fim % 2)
        merged  = array.array("i", [0]*(tam_esq+tam_dir))
        i = j = 0
        while i < tam_esq and j < tam_dir:
            if ord_esq[i] < ord_dir[j]:
                merged[i+j] = ord_esq[i]; i += 1
            else:
                merged[i+j] = ord_dir[j]; j += 1
        while i < tam_esq:
            merged[i+j] = ord_esq[i]; i += 1
        while j < tam_dir:
            merged[i+j] = ord_dir[j]; j += 1

        resultado = list(merged)
        self._pop(cid=cid, pai=pai, prof=prof,
                  resultado=resultado, base=False)
        return merged


def _fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


# ══════════════════════════════════════════════════════
#  WIDGET DE CÉLULAS
# ══════════════════════════════════════════════════════
def celulas(pai, valores, esquema="neutro", tamanho=36):
    cores = {
        "neutro":     (COR_NEU_BG,  COR_NEU_BD,  COR_NEU_TX),
        "esq":        (COR_ESQ_BG,  COR_ESQ_BD,  COR_ESQ_TX),
        "dir":        (COR_DIR_BG,  COR_DIR_BD,  COR_DIR_TX),
        "ordenado":   (COR_OK_BG,   COR_OK_BD,   COR_OK_TX),
    }
    bg, bd, tx = cores.get(esquema, cores["neutro"])
    widgets = []
    for val in valores:
        f = tk.Frame(pai, bg=bg,
                     highlightbackground=bd, highlightthickness=1,
                     width=tamanho, height=tamanho)
        f.pack_propagate(False)
        f.pack(side="left", padx=2)
        tk.Label(f, text=str(val), bg=bg, fg=tx,
                 font=(FONTE_TXT, 10, "bold")).place(relx=.5, rely=.5, anchor="center")
        widgets.append(f)
    return widgets


# ══════════════════════════════════════════════════════
#  CARD DE FRAME NA PILHA
# ══════════════════════════════════════════════════════
class FrameCard(tk.Frame):
    """Um frame da call stack — ativo (verde) ou inativo (cinza)."""

    def __init__(self, master, cid, prof, lado, vetor, fim, numero, ativo=True):
        super().__init__(master, bg=VERDE_BG if ativo else CINZA_FRAME,
                         highlightbackground=VERDE if ativo else BORDA_FORTE,
                         highlightthickness=2 if ativo else 1)
        self.cid   = cid
        self.prof  = prof
        self.ativo = ativo
        self._vetor = vetor
        self._fim   = fim
        self._numero = numero

        cor_header_bg = VERDE_BG if ativo else CINZA_FRAME
        cor_label     = VERDE_ESCURO if ativo else CINZA_TEXTO
        cor_badge_bg  = VERDE        if ativo else BORDA_FORTE
        cor_badge_fg  = VERDE_ESCURO if ativo else CINZA_TEXTO

        # ── cabeçalho ──────────────────────────────────
        cab = tk.Frame(self, bg=cor_header_bg)
        cab.pack(fill="x", padx=14, pady=(10, 4))

        label_lado = tk.Label(cab,
            text=f"{lado}  merge_sort({_fmt(vetor)}, fim = {fim})",
            bg=cor_header_bg, fg=cor_label,
            font=(FONTE_HEAD, 11, "bold"), anchor="w")
        label_lado.pack(side="left")

        badge = tk.Label(cab,
            text=f"  Chamada {numero}  ",
            bg=cor_badge_bg, fg=cor_badge_fg,
            font=(FONTE_TXT, 9, "bold"),
            relief="flat", padx=6, pady=3)
        badge.pack(side="right")

        # separador
        tk.Frame(self, bg=VERDE if ativo else BORDA, height=1).pack(fill="x")

        # ── corpo ──────────────────────────────────────
        self._corpo = tk.Frame(self, bg=BRANCO if ativo else CINZA_FRAME,
                                padx=14, pady=10)
        self._corpo.pack(fill="x")

        # linha de células (começa neutro)
        self._linha_cel = tk.Frame(self._corpo,
                                    bg=BRANCO if ativo else CINZA_FRAME)
        self._linha_cel.pack(anchor="w", pady=(0, 6))

        esquema_inicial = "neutro" if ativo else "neutro"
        self._celulas = celulas(self._linha_cel, vetor, esquema_inicial)

        # linha de texto copiar
        cor_ann = CINZA_MED if ativo else CINZA_LEVE
        self._ann = tk.Label(self._corpo, text="",
                              bg=BRANCO if ativo else CINZA_FRAME,
                              fg=cor_ann,
                              font=(FONTE_TXT, 9), anchor="w", justify="left")
        self._ann.pack(fill="x")

    # ── API ────────────────────────────────────────────
    def mostrar_split(self, v_esq, v_dir, meio, fim, vetor):
        # recolore células
        for w in self._linha_cel.winfo_children():
            w.destroy()
        celulas(self._linha_cel, v_esq, "esq")
        celulas(self._linha_cel, v_dir, "dir")

        ann = (f"copiar({_fmt(vetor)}, 0, meio = {meio})    "
               f"copiar({_fmt(vetor)}, meio = {meio}, fim = {fim})")
        self._ann.configure(text=ann)

    def mostrar_resultado(self, resultado):
        for w in self._linha_cel.winfo_children():
            w.destroy()
        celulas(self._linha_cel, resultado, "ordenado")
        self._ann.configure(text=f"↩  retorna  {_fmt(resultado)}")

    def desativar(self):
        self.configure(bg=CINZA_FRAME, highlightbackground=BORDA, highlightthickness=1)


# ══════════════════════════════════════════════════════
#  APLICATIVO
# ══════════════════════════════════════════════════════
class App(tk.Tk):
    DADOS    = [14, 7, 3, 12]
    PADDING  = 16           # px lateral dentro da área de pilha

    def __init__(self):
        super().__init__()
        self.title("Call Stack — Merge Sort")
        self.configure(bg=FUNDO)
        self.geometry("860x620")
        self.minsize(700, 480)
        self.resizable(True, True)

        tracer = Tracer(self.DADOS)
        self._passos  = tracer.passos
        self._total   = len(self._passos)
        self._atual   = 0

        # estado da pilha: lista de dicts com info do frame
        self._pilha: list[dict] = []   # cada item: {cid, card_widget, numero}
        self._cards: dict[int, FrameCard] = {}
        self._chamada_num = 0          # contador de chamadas (1-based)

        self._build()
        self._atualizar_nav()

    # ── BUILD ────────────────────────────────────────
    def _build(self):
        # ── topo ──────────────────────────────────────
        topo = tk.Frame(self, bg=BRANCO,
                        highlightbackground=BORDA, highlightthickness=1)
        topo.pack(fill="x")

        tk.Label(topo, text="Call Stack Merge Sort",
                 bg=BRANCO, fg=CINZA_TEXTO,
                 font=(FONTE_HEAD, 14, "bold"),
                 padx=20, pady=14).pack(side="left")

        tk.Label(topo, text=f"Vetor: {_fmt(self.DADOS)}",
                 bg=BRANCO, fg=CINZA_TEXTO,
                 font=(FONTE_HEAD, 14, "bold"),
                 padx=20).pack(side="right")

        # ── label "Pilha de Execução" ──────────────────
        tk.Label(self, text="Pilha de Execução (Call Stack)",
                 bg=FUNDO, fg=CINZA_MED,
                 font=(FONTE_TXT, 9),
                 anchor="w", padx=20, pady=8).pack(fill="x")

        # ── área da pilha (scrollável) ─────────────────
        area = tk.Frame(self, bg=FUNDO, padx=20)
        area.pack(fill="both", expand=True)

        pilha_borda = tk.Frame(area, bg=BRANCO,
                                highlightbackground=BORDA,
                                highlightthickness=1)
        pilha_borda.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(pilha_borda, bg=BRANCO,
                                  highlightthickness=0)
        vsb = tk.Scrollbar(pilha_borda, orient="vertical",
                           command=self._canvas.yview, bg=FUNDO)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(fill="both", expand=True)

        self._inner = tk.Frame(self._canvas, bg=BRANCO)
        # anchor="sw" — frames são inseridos pelo topo (pack side=bottom),
        # fazendo a pilha crescer para cima visualmente
        self._win   = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")

        def _on_inner_configure(e):
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))
            # reposiciona a janela interna na base do canvas para
            # que o conteúdo cresça de baixo para cima
            ch = self._canvas.winfo_height()
            ih = self._inner.winfo_reqheight()
            y  = max(0, ch - ih)
            self._canvas.coords(self._win, 0, y)

        self._inner.bind("<Configure>", _on_inner_configure)
        self._canvas.bind("<Configure>",
            lambda e: (self._canvas.itemconfig(self._win, width=e.width),
                       _on_inner_configure(e)))

        # ── rodapé de navegação ────────────────────────
        rodape = tk.Frame(self, bg=BRANCO,
                          highlightbackground=BORDA, highlightthickness=1)
        rodape.pack(fill="x", side="bottom")

        btn_cfg = dict(relief="flat", cursor="hand2",
                       font=(FONTE_TXT, 10), pady=12, padx=20)

        self._btn_ant = tk.Button(rodape, text="← Passo Anterior",
                                   bg=BRANCO, fg=CINZA_TEXTO,
                                   highlightbackground=BORDA,
                                   highlightthickness=1,
                                   command=self._anterior, **btn_cfg)
        self._btn_ant.pack(side="left", padx=20, pady=10)

        self._lbl_passo = tk.Label(rodape, text="",
                                    bg=BRANCO, fg=CINZA_MED,
                                    font=(FONTE_TXT, 10))
        self._lbl_passo.pack(side="left", expand=True)

        self._btn_prox = tk.Button(rodape, text="Próximo Passo →",
                                    bg=VERDE, fg=VERDE_ESCURO,
                                    highlightbackground=VERDE,
                                    highlightthickness=0,
                                    activebackground="#22c55e",
                                    command=self._proximo, **btn_cfg)
        self._btn_prox.pack(side="right", padx=20, pady=10)

        # atalhos
        self.bind("<Right>", lambda e: self._proximo())
        self.bind("<Left>",  lambda e: self._anterior())
        self.bind("<space>", lambda e: self._proximo())

    # ── NAVEGAÇÃO ────────────────────────────────────
    def _proximo(self):
        if self._atual >= self._total:
            return
        self._aplicar(self._passos[self._atual])
        self._atual += 1
        self._atualizar_nav()

    def _anterior(self):
        if self._atual <= 0:
            return
        alvo = self._atual - 1
        # reconstruir do zero
        self._reconstruir(alvo)

    def _reconstruir(self, alvo):
        for w in self._inner.winfo_children():
            w.destroy()
        self._cards.clear()
        self._pilha.clear()
        self._chamada_num = 0
        self._atual = 0
        for i in range(alvo):
            self._aplicar(self._passos[i])
            self._atual += 1
        self._atualizar_nav()

    def _atualizar_nav(self):
        self._lbl_passo.configure(
            text=f"Passo {self._atual} de {self._total}")
        self._btn_ant.configure(
            state="normal" if self._atual > 0 else "disabled",
            fg=CINZA_TEXTO if self._atual > 0 else CINZA_LEVE)
        self._btn_prox.configure(
            state="normal" if self._atual < self._total else "disabled")
        self._canvas.yview_moveto(1.0)

    # ── APLICAR PASSO ────────────────────────────────
    def _aplicar(self, passo):
        t = passo["tipo"]

        if t == "PUSH":
            self._chamada_num += 1
            num = self._chamada_num

            # cards existentes viram inativos visualmente
            # (ficam na tela, apenas o mais recente é "ativo")
            # — desativar o topo anterior
            if self._pilha:
                topo_cid = self._pilha[-1]["cid"]
                card = self._cards.get(topo_cid)
                if card:
                    card.desativar()

            ativo = True
            card = FrameCard(
                self._inner,
                cid    = passo["cid"],
                prof   = passo["prof"],
                lado   = passo["lado"],
                vetor  = passo["vetor"],
                fim    = passo["fim"],
                numero = num,
                ativo  = ativo,
            )
            card.pack(fill="x", padx=self.PADDING, pady=(0, 8))

            self._cards[passo["cid"]] = card
            self._pilha.append({"cid": passo["cid"], "num": num})

        elif t == "SPLIT":
            card = self._cards.get(passo["cid"])
            if card:
                card.mostrar_split(passo["v_esq"], passo["v_dir"],
                                   passo["meio"], passo["fim"],
                                   passo["vetor"])

        elif t == "POP":
            cid  = passo["cid"]
            card = self._cards.get(cid)
            if card:
                card.mostrar_resultado(passo["resultado"])
                card.desativar()

            # remove da pilha lógica
            self._pilha = [p for p in self._pilha if p["cid"] != cid]

            # reativar novo topo
            if self._pilha:
                novo_topo = self._pilha[-1]["cid"]
                novo_card = self._cards.get(novo_topo)
                if novo_card:
                    novo_card.configure(
                        bg=VERDE_BG,
                        highlightbackground=VERDE,
                        highlightthickness=2)


# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()