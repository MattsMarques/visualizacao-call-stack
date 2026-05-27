import tkinter as tk
from tkinter import ttk
import array

FUNDO        = "#F1F1F1"     
PAPEL        = "#FFFFFF"
BORDA        = "#E0E0E0"
BORDA_FORTE  = "#B6B6B6"

CINZA_TEXTO  = "#303030"
CINZA_MEDIO  = "#696969"
CINZA_LEVE   = "#A8A8A8"
CINZA_BG     = "#F1F1F1"


COR_CALL   = "#4ADE80"  
COR_COPIAR = "#7E3AF2" 
COR_BASE   = "#0E9F6E"   
COR_MERGE  = "#E3A008"  
COR_RET    = "#C81E1E"   

COR_CALL_BG   = "#EBF5FF"
COR_COPIAR_BG = "#F5F3FF"
COR_BASE_BG   = "#F3FAF7"
COR_MERGE_BG  = "#FFFBEB"
COR_RET_BG    = "#FDF2F2"

FONTE_MONO = "Cabinet Grotesk"
FONTE_SANS = "Switzer"


# ══════════════════════════════════════════════════════════════
#  TRACER — instrumenta o merge_sort original passo a passo
# ══════════════════════════════════════════════════════════════
class Tracer:
    """
    Registra cada passo da execução do merge_sort como uma lista de eventos.
    Cada evento representa exatamente uma linha lógica do código original.
    """
    def __init__(self, vetor_inicial: list[int]):
        self.eventos: list[dict] = []
        self._id = 0
        v = array.array("i", vetor_inicial)
        self._merge_sort(v, len(v), pai=None, profundidade=0, lado="raiz")

    def _novo_id(self) -> int:
        self._id += 1
        return self._id

    def _emit(self, tipo: str, **kwargs):
        self.eventos.append({"tipo": tipo, **kwargs})

    # ── copiar ──────────────────────────────────────────────
    def _copiar(self, vetor: array.array, inicio: int, fim: int) -> array.array:
        tamanho = fim - inicio
        v = array.array("i", [0] * tamanho)
        i = 0
        while i < tamanho:
            v[i] = vetor[inicio + i]
            i += 1
        return v

    # ── merge ───────────────────────────────────────────────
    def _merge(self, ord_esq, tam_esq, ord_dir, tam_dir,
               call_id: int, profundidade: int):
        resultado = array.array("i", [0] * (tam_esq + tam_dir))
        i, j = 0, 0
        passos: list[dict] = []

        while i < tam_esq and j < tam_dir:
            if ord_esq[i] < ord_dir[j]:
                resultado[i + j] = ord_esq[i]
                passos.append({"origem": "esq", "valor": ord_esq[i], "pos": i + j,
                                "i": i, "j": j})
                i += 1
            else:
                resultado[i + j] = ord_dir[j]
                passos.append({"origem": "dir", "valor": ord_dir[j], "pos": i + j,
                                "i": i, "j": j})
                j += 1

        while i < tam_esq:
            resultado[i + j] = ord_esq[i]
            passos.append({"origem": "esq_resto", "valor": ord_esq[i],
                           "pos": i + j, "i": i, "j": j})
            i += 1
        while j < tam_dir:
            resultado[i + j] = ord_dir[j]
            passos.append({"origem": "dir_resto", "valor": ord_dir[j],
                           "pos": i + j, "i": i, "j": j})
            j += 1

        return resultado, passos

    # ── merge_sort ───────────────────────────────────────────
    def _merge_sort(self, vetor: array.array, fim: int,
                    pai, profundidade: int, lado: str):
        call_id = self._novo_id()

        # ── CHAMADA ──────────────────────────────────────────
        self._emit("CHAMADA",
                   call_id=call_id, pai=pai,
                   profundidade=profundidade, lado=lado,
                   vetor=list(vetor), fim=fim)

        # ── CASO BASE ────────────────────────────────────────
        if fim <= 1:
            self._emit("CASO_BASE",
                       call_id=call_id, profundidade=profundidade,
                       vetor=list(vetor))
            self._emit("RETORNO",
                       call_id=call_id, pai=pai,
                       profundidade=profundidade,
                       resultado=list(vetor),
                       motivo="caso_base")
            return vetor

        meio = fim // 2

        # ── COPIAR ESQ ───────────────────────────────────────
        v_esq = self._copiar(vetor, 0, meio)
        self._emit("COPIAR",
                   call_id=call_id, profundidade=profundidade,
                   origem=list(vetor), inicio=0, fim_copia=meio,
                   resultado=list(v_esq), variavel="v_esq",
                   meio=meio)

        # ── COPIAR DIR ───────────────────────────────────────
        v_dir = self._copiar(vetor, meio, fim)
        self._emit("COPIAR",
                   call_id=call_id, profundidade=profundidade,
                   origem=list(vetor), inicio=meio, fim_copia=fim,
                   resultado=list(v_dir), variavel="v_dir",
                   meio=meio)

        # ── RECURSÃO ESQ ─────────────────────────────────────
        ord_esq = self._merge_sort(v_esq, meio,
                                   pai=call_id, profundidade=profundidade + 1,
                                   lado="esq")

        # ── RECURSÃO DIR ─────────────────────────────────────
        ord_dir = self._merge_sort(v_dir, meio + (fim % 2),
                                   pai=call_id, profundidade=profundidade + 1,
                                   lado="dir")

        # ── MERGE ────────────────────────────────────────────
        tam_esq = meio
        tam_dir = meio + (fim % 2)
        merged, passos = self._merge(ord_esq, tam_esq, ord_dir, tam_dir,
                                     call_id, profundidade)

        self._emit("MERGE",
                   call_id=call_id, profundidade=profundidade,
                   esq=list(ord_esq), dir=list(ord_dir),
                   resultado=list(merged), passos=passos)

        # ── RETORNO ──────────────────────────────────────────
        self._emit("RETORNO",
                   call_id=call_id, pai=pai,
                   profundidade=profundidade,
                   resultado=list(merged),
                   motivo="merge")
        return merged


# ══════════════════════════════════════════════════════════════
#  WIDGET DE CÉLULA (um número do vetor)
# ══════════════════════════════════════════════════════════════
def criar_celulas(pai_frame, valores: list[int],
                  cor_fundo="#FFFFFF", cor_borda="#C0BCBA",
                  cor_texto="#2C2A25", tamanho=28) -> list:
    """Retorna lista de (frame, label) para cada valor."""
    celulas = []
    for v in valores:
        f = tk.Frame(pai_frame, bg=cor_fundo,
                     highlightbackground=cor_borda,
                     highlightthickness=1,
                     width=tamanho, height=tamanho)
        f.pack_propagate(False)
        f.pack(side="left", padx=1)
        lbl = tk.Label(f, text=str(v), bg=cor_fundo, fg=cor_texto,
                       font=(FONTE_MONO, 9, "bold"))
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        celulas.append((f, lbl))
    return celulas


# ══════════════════════════════════════════════════════════════
#  FRAME DE CHAMADA NA PILHA
# ══════════════════════════════════════════════════════════════
class FrameChamada(tk.Frame):
    """
    Representa um frame na call stack — um retângulo com:
    - cabeçalho: nome da função + assinatura
    - corpo: estado interno (variáveis locais visuais)
    - status: linha que descreve o que está acontecendo agora
    """
    LARGURA_INDENT = 20   # px de recuo por nível de profundidade

    def __init__(self, pai, call_id: int, profundidade: int,
                 lado: str, vetor: list[int], fim: int, **kwargs):
        super().__init__(pai, bg=PAPEL,
                         highlightbackground=BORDA,
                         highlightthickness=1, **kwargs)
        self.call_id     = call_id
        self.profundidade = profundidade
        self.lado        = lado
        self._vetor      = vetor
        self._fim        = fim

        # ── cabeçalho ──────────────────────────────────────
        cab = tk.Frame(self, bg=COR_CALL_BG,
                       highlightbackground=BORDA, highlightthickness=0)
        cab.pack(fill="x")

        lado_badge = {"raiz": "●", "esq": "◀", "dir": "▶"}.get(lado, lado)
        lado_cor   = {"raiz": CINZA_MEDIO, "esq": COR_CALL, "dir": COR_COPIAR
                      }.get(lado, CINZA_MEDIO)

        tk.Label(cab, text=f" {lado_badge} ", bg=COR_CALL_BG,
                 fg=lado_cor, font=(FONTE_MONO, 9, "bold")).pack(side="left")

        sig = f"merge_sort(vetor={_fmt_vetor(vetor)}, fim={fim})"
        tk.Label(cab, text=sig, bg=COR_CALL_BG, fg=COR_CALL,
                 font=(FONTE_MONO, 8, "bold"), anchor="w").pack(side="left", padx=2)

        tk.Label(cab, text=f"prof. {profundidade}", bg=COR_CALL_BG,
                 fg=CINZA_LEVE, font=(FONTE_MONO, 7)).pack(side="right", padx=6)

        # ── corpo: variáveis locais ─────────────────────────
        self._corpo = tk.Frame(self, bg=PAPEL, padx=8, pady=5)
        self._corpo.pack(fill="x")

        # linha das células do vetor de entrada
        linha_v = tk.Frame(self._corpo, bg=PAPEL)
        linha_v.pack(anchor="w", pady=(0, 3))
        tk.Label(linha_v, text="vetor → ", bg=PAPEL, fg=CINZA_MEDIO,
                 font=(FONTE_MONO, 8)).pack(side="left")
        self._celulas_vetor = criar_celulas(linha_v, vetor)

        # linha de variáveis (meio, v_esq, v_dir)
        self._linha_vars = tk.Frame(self._corpo, bg=PAPEL)
        self._linha_vars.pack(anchor="w", fill="x")

        # status
        self._status = tk.Label(self._corpo, text="aguardando…",
                                 bg=PAPEL, fg=CINZA_LEVE,
                                 font=(FONTE_MONO, 8), anchor="w")
        self._status.pack(fill="x", pady=(3, 0))

        # guarda widgets dinâmicos para atualização
        self._vars_widgets: dict[str, tk.Widget] = {}

    # ── API pública ────────────────────────────────────────
    def set_status(self, texto: str, cor: str = CINZA_MEDIO):
        self._status.configure(text=texto, fg=cor)

    def set_borda(self, cor: str):
        self.configure(highlightbackground=cor)

    def mostrar_meio(self, meio: int):
        self._set_var_label("meio", f"meio = {meio}", CINZA_MEDIO)

    def mostrar_v_esq(self, valores: list[int], destaque=False):
        self._set_var_celulas("v_esq", valores,
                              cor=COR_CALL if destaque else CINZA_LEVE,
                              bg=COR_CALL_BG if destaque else CINZA_BG)

    def mostrar_v_dir(self, valores: list[int], destaque=False):
        self._set_var_celulas("v_dir", valores,
                              cor=COR_COPIAR if destaque else CINZA_LEVE,
                              bg=COR_COPIAR_BG if destaque else CINZA_BG)

    def mostrar_resultado(self, valores: list[int]):
        """Substitui as células do vetor pelo resultado ordenado."""
        for w, _ in self._celulas_vetor:
            w.destroy()
        linha = None
        for w in self._corpo.winfo_children():
            if isinstance(w, tk.Frame):
                linha = w
                break
        if not linha:
            return
        # recriar na linha do vetor
        for widget in linha.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        self._celulas_vetor = criar_celulas(
            linha, valores,
            cor_fundo="#F0FDF4", cor_borda="#22C55E", cor_texto="#15803D")

    def dimmer(self):
        """Esmaece o frame após retorno."""
        self.configure(highlightbackground=BORDA)
        self._status.configure(fg=CINZA_LEVE)

    # ── helpers internos ───────────────────────────────────
    def _set_var_label(self, chave: str, texto: str, cor: str):
        if chave in self._vars_widgets:
            self._vars_widgets[chave].configure(text=texto, fg=cor)
        else:
            lbl = tk.Label(self._linha_vars, text=texto, bg=PAPEL, fg=cor,
                           font=(FONTE_MONO, 8))
            lbl.pack(side="left", padx=(0, 10))
            self._vars_widgets[chave] = lbl

    def _set_var_celulas(self, chave: str, valores: list[int],
                         cor: str, bg: str):
        if chave in self._vars_widgets:
            self._vars_widgets[chave].destroy()

        container = tk.Frame(self._linha_vars, bg=PAPEL)
        container.pack(side="left", padx=(0, 10))
        tk.Label(container, text=f"{chave} → ", bg=PAPEL, fg=cor,
                 font=(FONTE_MONO, 8)).pack(side="left")
        criar_celulas(container, valores, cor_fundo=bg,
                      cor_borda=cor, cor_texto=cor)
        self._vars_widgets[chave] = container


# ══════════════════════════════════════════════════════════════
#  UTILITÁRIOS
# ══════════════════════════════════════════════════════════════
def _fmt_vetor(v: list) -> str:
    return "[" + ", ".join(str(x) for x in v) + "]"

def _descricao_evento(ev: dict) -> tuple[str, str, str]:
    """Retorna (tipo_label, descricao_curta, cor)."""
    t = ev["tipo"]
    p = ev.get("profundidade", 0)
    ind = "  " * p

    if t == "CHAMADA":
        lado = {"raiz": "raiz", "esq": "lado esquerdo", "dir": "lado direito"
                }.get(ev["lado"], ev["lado"])
        return ("CHAMADA", f"{ind}merge_sort({_fmt_vetor(ev['vetor'])}, fim={ev['fim']})  ← {lado}", COR_CALL)

    if t == "CASO_BASE":
        return ("BASE", f"{ind}caso base: fim ≤ 1, retorna {_fmt_vetor(ev['vetor'])} sem dividir", COR_BASE)

    if t == "COPIAR":
        return ("COPIAR",
                f"{ind}copiar(vetor, {ev['inicio']}, {ev['fim_copia']})  →  {ev['variavel']} = {_fmt_vetor(ev['resultado'])}",
                COR_COPIAR)

    if t == "MERGE":
        return ("MERGE",
                f"{ind}merge({_fmt_vetor(ev['esq'])}, {_fmt_vetor(ev['dir'])})  →  {_fmt_vetor(ev['resultado'])}",
                COR_MERGE)

    if t == "RETORNO":
        mot = "caso base" if ev.get("motivo") == "caso_base" else "após merge"
        return ("RETORNO",
                f"{ind}retorna {_fmt_vetor(ev['resultado'])}  ({mot})",
                COR_RET)

    return (t, str(ev), CINZA_MEDIO)


# ══════════════════════════════════════════════════════════════
#  APLICATIVO PRINCIPAL
# ══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Call Stack — Merge Sort")
        self.configure(bg=FUNDO)
        self.resizable(True, True)
        self.geometry("1180x740")
        self.minsize(900, 600)

        self._dados_default = [6, 5, 12, 10, 9, 1]
        self._eventos: list[dict] = []
        self._passo_atual = 0
        self._frames_pilha: dict[int, FrameChamada] = {}   # call_id → widget
        self._pilha_ativa: list[int] = []                  # ids em execução

        self._construir_ui()
        self._carregar(self._dados_default)

    # ══ CONSTRUÇÃO DA UI ═══════════════════════════════════
    def _construir_ui(self):
        # ── barra superior ─────────────────────────────────
        topo = tk.Frame(self, bg=PAPEL,
                        highlightbackground=BORDA, highlightthickness=1)
        topo.pack(fill="x", side="top")

        tk.Label(topo, text="Merge Sort", bg=PAPEL, fg=CINZA_TEXTO,
                 font=(FONTE_SANS, 13, "bold"), padx=16, pady=10
                 ).pack(side="left")
        tk.Label(topo, text="visualizador de call stack",
                 bg=PAPEL, fg=CINZA_LEVE,
                 font=(FONTE_SANS, 10, "italic")).pack(side="left")

        direita_topo = tk.Frame(topo, bg=PAPEL)
        direita_topo.pack(side="right", padx=12)

        tk.Label(direita_topo, text="vetor:", bg=PAPEL, fg=CINZA_MEDIO,
                 font=(FONTE_MONO, 9)).pack(side="left", padx=(0, 4))

        self._var_entrada = tk.StringVar(value="6,5,12,10,9,1")
        entrada = tk.Entry(direita_topo, textvariable=self._var_entrada,
                           font=(FONTE_MONO, 9), bg=CINZA_BG,
                           fg=CINZA_TEXTO, relief="flat", bd=0,
                           highlightthickness=1, highlightbackground=BORDA,
                           width=20, insertbackground=CINZA_TEXTO)
        entrada.pack(side="left", padx=4, ipady=3)

        tk.Button(direita_topo, text="Recarregar",
                  font=(FONTE_MONO, 8), bg=FUNDO, fg=CINZA_TEXTO,
                  relief="flat", cursor="hand2", padx=8, pady=3,
                  highlightbackground=BORDA, highlightthickness=1,
                  command=self._recarregar).pack(side="left", padx=4)

        # ── área principal ─────────────────────────────────
        principal = tk.Frame(self, bg=FUNDO)
        principal.pack(fill="both", expand=True)

        # coluna esquerda: pilha
        coluna_esq = tk.Frame(principal, bg=FUNDO)
        coluna_esq.pack(side="left", fill="both", expand=True, padx=(12, 6), pady=12)

        cab_pilha = tk.Frame(coluna_esq, bg=FUNDO)
        cab_pilha.pack(fill="x", pady=(0, 6))
        tk.Label(cab_pilha, text="PILHA DE CHAMADAS", bg=FUNDO,
                 fg=CINZA_LEVE, font=(FONTE_MONO, 8, "bold")).pack(side="left")
        self._lbl_profundidade = tk.Label(cab_pilha, text="", bg=FUNDO,
                                           fg=CINZA_LEVE, font=(FONTE_MONO, 8))
        self._lbl_profundidade.pack(side="right")

        # canvas scrollável para a pilha
        self._canvas_pilha = tk.Canvas(coluna_esq, bg=FUNDO,
                                       highlightthickness=0)
        vsb = tk.Scrollbar(coluna_esq, orient="vertical",
                           command=self._canvas_pilha.yview,
                           bg=CINZA_BG)
        self._canvas_pilha.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas_pilha.pack(fill="both", expand=True)

        self._frame_pilha_interno = tk.Frame(self._canvas_pilha, bg=FUNDO)
        self._win_pilha = self._canvas_pilha.create_window(
            (0, 0), window=self._frame_pilha_interno, anchor="nw")

        self._frame_pilha_interno.bind("<Configure>", self._ao_redimensionar_pilha)
        self._canvas_pilha.bind("<Configure>", self._ao_redimensionar_canvas)

        # coluna direita: log + controles
        coluna_dir = tk.Frame(principal, bg=FUNDO, width=340)
        coluna_dir.pack(side="right", fill="y", padx=(6, 12), pady=12)
        coluna_dir.pack_propagate(False)

        # ── log de eventos ─────────────────────────────────
        tk.Label(coluna_dir, text="LOG DE EVENTOS", bg=FUNDO,
                 fg=CINZA_LEVE, font=(FONTE_MONO, 8, "bold"),
                 anchor="w").pack(fill="x", pady=(0, 4))

        frame_log = tk.Frame(coluna_dir, bg=PAPEL,
                             highlightbackground=BORDA, highlightthickness=1)
        frame_log.pack(fill="both", expand=True)

        self._log = tk.Text(frame_log, bg=PAPEL, fg=CINZA_MEDIO,
                            font=(FONTE_MONO, 8), relief="flat", bd=0,
                            state="disabled", wrap="word", cursor="arrow",
                            padx=8, pady=6)
        vsb_log = tk.Scrollbar(frame_log, command=self._log.yview,
                               bg=CINZA_BG)
        self._log.configure(yscrollcommand=vsb_log.set)
        vsb_log.pack(side="right", fill="y")
        self._log.pack(fill="both", expand=True)

        # tags de cor no log
        for tipo, cor in [("CHAMADA", COR_CALL), ("BASE", COR_BASE),
                           ("COPIAR", COR_COPIAR), ("MERGE", COR_MERGE),
                           ("RETORNO", COR_RET), ("dim", CINZA_LEVE)]:
            self._log.tag_configure(tipo, foreground=cor)
        self._log.tag_configure("destaque", background="#FFF9C4",
                                foreground=CINZA_TEXTO)
        self._log.tag_configure("atual_linha", background="#EBF5FF")

        # ── separador ──────────────────────────────────────
        tk.Frame(coluna_dir, bg=BORDA, height=1).pack(fill="x", pady=8)

        # ── legenda ────────────────────────────────────────
        tk.Label(coluna_dir, text="LEGENDA", bg=FUNDO, fg=CINZA_LEVE,
                 font=(FONTE_MONO, 8, "bold"), anchor="w").pack(fill="x",
                                                                 pady=(0, 4))
        legenda = [
            (COR_CALL,   "CHAMADA",  "nova chamada a merge_sort"),
            (COR_COPIAR, "COPIAR",   "função copiar(vetor, ini, fim)"),
            (COR_BASE,   "BASE",     "caso base: fim ≤ 1"),
            (COR_MERGE,  "MERGE",    "função merge(esq, dir)"),
            (COR_RET,    "RETORNO",  "retorno com vetor ordenado"),
        ]
        for cor, tipo, desc in legenda:
            row = tk.Frame(coluna_dir, bg=FUNDO)
            row.pack(fill="x", pady=1)
            tk.Label(row, text="■", bg=FUNDO, fg=cor,
                     font=(FONTE_MONO, 9)).pack(side="left")
            tk.Label(row, text=f" {tipo:<8}", bg=FUNDO, fg=cor,
                     font=(FONTE_MONO, 8, "bold")).pack(side="left")
            tk.Label(row, text=desc, bg=FUNDO, fg=CINZA_LEVE,
                     font=(FONTE_MONO, 7)).pack(side="left")

        # ── separador ──────────────────────────────────────
        tk.Frame(coluna_dir, bg=BORDA, height=1).pack(fill="x", pady=8)

        # ── barra de progresso ─────────────────────────────
        self._var_prog = tk.DoubleVar()

        self._lbl_passo = tk.Label(coluna_dir, text="passo 0 / 0",
                                    bg=FUNDO, fg=CINZA_LEVE,
                                    font=(FONTE_MONO, 8), anchor="e")
        self._lbl_passo.pack(fill="x")

        # ── botões de navegação ────────────────────────────
        tk.Frame(coluna_dir, bg=BORDA, height=1).pack(fill="x", pady=8)

        frame_btns = tk.Frame(coluna_dir, bg=FUNDO)
        frame_btns.pack(fill="x")

        estilo_btn = dict(relief="flat", font=(FONTE_MONO, 10),
                          cursor="hand2", pady=6, padx=14,
                          highlightthickness=1)

        self._btn_ant = tk.Button(frame_btns, text="◀  Anterior",
                                   bg=PAPEL, fg=CINZA_MEDIO,
                                   highlightbackground=BORDA,
                                   command=self._passo_anterior, **estilo_btn)
        self._btn_ant.pack(side="left", padx=(0, 6), fill="x", expand=True)

        self._btn_prox = tk.Button(frame_btns, text="Próximo  ▶",
                                    bg=COR_CALL, fg=PAPEL,
                                    highlightbackground=COR_CALL,
                                    activebackground="#1346B8",
                                    activeforeground=PAPEL,
                                    command=self._passo_proximo, **estilo_btn)
        self._btn_prox.pack(side="left", fill="x", expand=True)

        # teclas de atalho
        self.bind("<Right>",  lambda e: self._passo_proximo())
        self.bind("<Left>",   lambda e: self._passo_anterior())
        self.bind("<space>",  lambda e: self._passo_proximo())

    # ══ SCROLL ════════════════════════════════════════════
    def _ao_redimensionar_pilha(self, event):
        self._canvas_pilha.configure(
            scrollregion=self._canvas_pilha.bbox("all"))

    def _ao_redimensionar_canvas(self, event):
        self._canvas_pilha.itemconfig(self._win_pilha, width=event.width)

    def _rolar_para_baixo(self):
        self._frame_pilha_interno.update_idletasks()
        self._canvas_pilha.configure(
            scrollregion=self._canvas_pilha.bbox("all"))
        self._canvas_pilha.yview_moveto(1.0)

    # ══ CARGA DE DADOS ════════════════════════════════════
    def _carregar(self, dados: list[int]):
        for w in self._frame_pilha_interno.winfo_children():
            w.destroy()
        self._frames_pilha.clear()
        self._pilha_ativa.clear()
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")

        tracer = Tracer(dados)
        self._eventos = tracer.eventos
        self._passo_atual = 0
        self._atualizar_progresso()
        self._atualizar_botoes()

    def _recarregar(self):
        try:
            raw   = self._var_entrada.get()
            dados = [int(x.strip()) for x in raw.split(",") if x.strip()]
            if not dados:
                raise ValueError
        except ValueError:
            self._log_append("⚠ entrada inválida. Use números separados por vírgula.", "dim")
            return
        self._carregar(dados)

    # ══ NAVEGAÇÃO ═════════════════════════════════════════
    def _passo_proximo(self):
        if self._passo_atual >= len(self._eventos):
            return
        self._aplicar_evento(self._eventos[self._passo_atual])
        self._passo_atual += 1
        self._atualizar_progresso()
        self._atualizar_botoes()

    def _passo_anterior(self):
        if self._passo_atual <= 0:
            return
        alvo = self._passo_atual - 1
        self._reconstruir_ate(alvo)

    def _reconstruir_ate(self, alvo: int):
        """Reconstrói a pilha do zero até o passo `alvo`."""
        for w in self._frame_pilha_interno.winfo_children():
            w.destroy()
        self._frames_pilha.clear()
        self._pilha_ativa.clear()
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")
        self._passo_atual = 0
        for i in range(alvo):
            self._aplicar_evento(self._eventos[i])
            self._passo_atual += 1
        self._atualizar_progresso()
        self._atualizar_botoes()

    def _atualizar_progresso(self):
        total = len(self._eventos)
        pct   = (self._passo_atual / total * 100) if total else 0
        self._var_prog.set(pct)
        self._lbl_passo.configure(
            text=f"passo {self._passo_atual} / {total}")

    def _atualizar_botoes(self):
        self._btn_ant.configure(
            state="normal" if self._passo_atual > 0 else "disabled",
            fg=CINZA_MEDIO if self._passo_atual > 0 else CINZA_LEVE)
        self._btn_prox.configure(
            state="normal" if self._passo_atual < len(self._eventos) else "disabled")

        # profundidade atual
        if self._pilha_ativa:
            fw = self._frames_pilha.get(self._pilha_ativa[-1])
            p  = fw.profundidade if fw else 0
            self._lbl_profundidade.configure(
                text=f"profundidade atual: {p}")
        else:
            self._lbl_profundidade.configure(text="")

    # ══ APLICAÇÃO DE EVENTOS ══════════════════════════════
    def _aplicar_evento(self, ev: dict):
        tipo = ev["tipo"]

        if tipo == "CHAMADA":
            self._evt_chamada(ev)
        elif tipo == "CASO_BASE":
            self._evt_caso_base(ev)
        elif tipo == "COPIAR":
            self._evt_copiar(ev)
        elif tipo == "MERGE":
            self._evt_merge(ev)
        elif tipo == "RETORNO":
            self._evt_retorno(ev)

        # sempre registrar no log
        tipo_label, desc, cor = _descricao_evento(ev)
        self._log_append(f"{tipo_label:<8}  {desc}", tipo_label)

    # ── CHAMADA ───────────────────────────────────────────
    def _evt_chamada(self, ev: dict):
        cid  = ev["call_id"]
        prof = ev["profundidade"]
        lado = ev["lado"]

        # indent por profundidade
        indent = prof * FrameChamada.LARGURA_INDENT

        wrapper = tk.Frame(self._frame_pilha_interno, bg=FUNDO)
        wrapper.pack(fill="x", padx=(indent, 6), pady=(0, 4))

        fc = FrameChamada(wrapper, call_id=cid, profundidade=prof,
                          lado=lado, vetor=ev["vetor"], fim=ev["fim"])
        fc.pack(fill="x")
        fc.set_status("chamada iniciada", COR_CALL)
        fc.set_borda(COR_CALL)

        self._frames_pilha[cid] = fc
        self._pilha_ativa.append(cid)
        self._rolar_para_baixo()

    # ── CASO BASE ─────────────────────────────────────────
    def _evt_caso_base(self, ev: dict):
        fc = self._frames_pilha.get(ev["call_id"])
        if not fc:
            return
        fc.set_status("caso base: fim ≤ 1 → retorna imediatamente", COR_BASE)
        fc.set_borda(COR_BASE)

    # ── COPIAR ────────────────────────────────────────────
    def _evt_copiar(self, ev: dict):
        fc = self._frames_pilha.get(ev["call_id"])
        if not fc:
            return
        fc.mostrar_meio(ev["meio"])
        if ev["variavel"] == "v_esq":
            fc.mostrar_v_esq(ev["resultado"], destaque=True)
            fc.set_status(
                f"copiar(vetor, 0, {ev['fim_copia']}) → v_esq = {_fmt_vetor(ev['resultado'])}",
                COR_COPIAR)
        else:
            fc.mostrar_v_dir(ev["resultado"], destaque=True)
            fc.set_status(
                f"copiar(vetor, {ev['inicio']}, {ev['fim_copia']}) → v_dir = {_fmt_vetor(ev['resultado'])}",
                COR_COPIAR)
        fc.set_borda(COR_COPIAR)

    # ── MERGE ─────────────────────────────────────────────
    def _evt_merge(self, ev: dict):
        fc = self._frames_pilha.get(ev["call_id"])
        if not fc:
            return
        fc.set_status(
            f"merge({_fmt_vetor(ev['esq'])}, {_fmt_vetor(ev['dir'])}) → {_fmt_vetor(ev['resultado'])}",
            COR_MERGE)
        fc.set_borda(COR_MERGE)
        fc.mostrar_resultado(ev["resultado"])

    # ── RETORNO ───────────────────────────────────────────
    def _evt_retorno(self, ev: dict):
        cid = ev["call_id"]
        fc  = self._frames_pilha.get(cid)
        if fc:
            fc.set_status(
                f"↩ retorna {_fmt_vetor(ev['resultado'])}",
                COR_RET)
            fc.set_borda(COR_RET)
            # após breve delay visual, esmaece
            self.after(80, lambda: fc.dimmer())

        if cid in self._pilha_ativa:
            self._pilha_ativa.remove(cid)

    # ══ LOG ═══════════════════════════════════════════════
    def _log_append(self, texto: str, tag: str = "dim"):
        self._log.configure(state="normal")
        self._log.insert("end", texto + "\n", tag)
        self._log.see("end")
        self._log.configure(state="disabled")


# ══════════════════════════════════════════════════════════════
#  ENTRADA
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()