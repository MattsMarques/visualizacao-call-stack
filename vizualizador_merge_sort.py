import tkinter as tk
from tkinter import ttk, font
import array
import time
import threading
from collections import deque

# ─────────────────────────────────────────────
#  CORES & ESTILOS
# ─────────────────────────────────────────────
BG        = "#ffffff"
BG2       = "#f1f1f1"
BG3       = "#f1f1f1"
BORDER    = "#C1C1C1"
GREEN     = "#3fb950"
GREEN_DIM = "#1a4a25"
BLUE      = "#58a6ff"
BLUE_DIM  = "#1a3a6a"
ORANGE    = "#f0883e"
ORANGE_DIM= "#4a2c0a"
PURPLE    = "#bc8cff"
PURPLE_DIM= "#3a1f6a"
RED       = "#f85149"
RED_DIM   = "#4a1010"
YELLOW    = "#e3b341"
CYAN      = "#39d0d8"
TEXT      = "#e6edf3"
TEXT_DIM  = "#8b949e"
TEXT_MUTED= "#484f58"

# ─────────────────────────────────────────────
#  INSTRUMENTAÇÃO DO MERGE SORT
# ─────────────────────────────────────────────
class MergeSortTracer:
    """Executa o merge_sort e grava cada evento em order."""
    def __init__(self, vetor_inicial):
        self.events = []
        self.call_id_counter = 0
        v = array.array("i", vetor_inicial)
        self._merge_sort(v, len(v), parent_id=None, depth=0, side="root")

    def _new_id(self):
        self.call_id_counter += 1
        return self.call_id_counter

    def _emit(self, kind, **kwargs):
        self.events.append({"kind": kind, **kwargs})

    def _merge_sort(self, vetor, fim, parent_id, depth, side):
        call_id = self._new_id()
        v_list  = list(vetor)

        self._emit("CALL",
                   call_id=call_id, parent_id=parent_id,
                   depth=depth, side=side,
                   vetor=v_list, fim=fim)

        if fim <= 1:
            self._emit("BASE_CASE",
                       call_id=call_id, depth=depth,
                       vetor=v_list)
            self._emit("RETURN",
                       call_id=call_id, parent_id=parent_id,
                       depth=depth, result=v_list)
            return vetor

        meio  = fim // 2
        v_esq = array.array("i", vetor[0:meio])
        v_dir = array.array("i", vetor[meio:fim])

        self._emit("SPLIT",
                   call_id=call_id, depth=depth,
                   esq=list(v_esq), dir=list(v_dir), meio=meio)

        ord_esq = self._merge_sort(v_esq, meio,         parent_id=call_id, depth=depth+1, side="esq")
        ord_dir = self._merge_sort(v_dir, meio+(fim%2), parent_id=call_id, depth=depth+1, side="dir")

        # ---- merge step ----
        tam_esq = meio
        tam_dir = meio + (fim % 2)
        merged  = array.array("i", [0]*(tam_esq + tam_dir))
        i, j = 0, 0
        steps = []
        while i < tam_esq and j < tam_dir:
            if ord_esq[i] < ord_dir[j]:
                merged[i+j] = ord_esq[i]
                steps.append({"picked": "esq", "idx_esq": i, "idx_dir": j,
                               "value": ord_esq[i], "merged_so_far": list(merged[:i+j+1])})
                i += 1
            else:
                merged[i+j] = ord_dir[j]
                steps.append({"picked": "dir", "idx_esq": i, "idx_dir": j,
                               "value": ord_dir[j], "merged_so_far": list(merged[:i+j+1])})
                j += 1
        while i < tam_esq:
            merged[i+j] = ord_esq[i]
            steps.append({"picked": "esq_rem", "idx_esq": i, "idx_dir": j,
                           "value": ord_esq[i], "merged_so_far": list(merged[:i+j+1])})
            i += 1
        while j < tam_dir:
            merged[i+j] = ord_dir[j]
            steps.append({"picked": "dir_rem", "idx_esq": i, "idx_dir": j,
                           "value": ord_dir[j], "merged_so_far": list(merged[:i+j+1])})
            j += 1

        result = list(merged)
        self._emit("MERGE",
                   call_id=call_id, depth=depth,
                   esq=list(ord_esq), dir=list(ord_dir),
                   result=result, steps=steps)
        self._emit("RETURN",
                   call_id=call_id, parent_id=parent_id,
                   depth=depth, result=result)
        return merged


# ─────────────────────────────────────────────
#  JANELA PRINCIPAL
# ─────────────────────────────────────────────
class MergeSortVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Merge Sort — Visualizador de Call Stack")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.geometry("1300x800")

        self._initial_data = [6, 5, 12, 10, 9, 1]
        self.speed_ms  = 700          # ms entre eventos
        self.events    = []
        self.event_idx = 0
        self.playing   = False
        self._after_id = None

        # call_id → frame widget
        self.frame_widgets: dict[int, tk.Frame] = {}
        # stack of active call_ids (for indentation)
        self.active_stack: list[int] = []
        # call_id → metadata
        self.call_meta: dict[int, dict] = {}

        self._build_ui()
        self._load_data(self._initial_data)

    # ─── UI LAYOUT ───────────────────────────
    def _build_ui(self):
        # ── top bar ──
        topbar = tk.Frame(self, bg=BG, pady=6, padx=12)
        topbar.pack(fill="x", side="top")

        tk.Label(topbar, text="⟨ merge_sort ⟩  call stack visualizer",
                 bg=BG, fg=GREEN, font=("Courier New", 13, "bold")).pack(side="left")

        # input + reload
        right = tk.Frame(topbar, bg=BG)
        right.pack(side="right")
        tk.Label(right, text="vetor:", bg=BG, fg=TEXT_DIM,
                 font=("Courier New", 10)).pack(side="left", padx=(0,4))
        self.input_var = tk.StringVar(value="6,5,12,10,9,1")
        entry = tk.Entry(right, textvariable=self.input_var, bg=BG3, fg=TEXT,
                         insertbackground=TEXT, relief="flat", bd=0,
                         font=("Courier New", 10), width=22,
                         highlightthickness=1, highlightbackground=BORDER)
        entry.pack(side="left", padx=4)
        tk.Button(right, text="↺ Recarregar", bg=BG3, fg=CYAN, relief="flat",
                  font=("Courier New", 9, "bold"), cursor="hand2",
                  command=self._reload, padx=8).pack(side="left", padx=4)

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x")

        # ── main pane ──
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

        # left: call stack
        left_wrap = tk.Frame(main, bg=BG, width=520)
        left_wrap.pack(side="left", fill="both", expand=True, padx=(0,0))
        left_wrap.pack_propagate(False)

        tk.Label(left_wrap, text="CALL  STACK", bg=BG, fg=TEXT_MUTED,
                 font=("Courier New", 9, "bold"), anchor="w",
                 padx=12, pady=6).pack(fill="x")

        self.stack_canvas = tk.Canvas(left_wrap, bg=BG, highlightthickness=0)
        self.stack_vsb    = tk.Scrollbar(left_wrap, orient="vertical",
                                         command=self.stack_canvas.yview,
                                         bg=BG3, troughcolor=BG)
        self.stack_canvas.configure(yscrollcommand=self.stack_vsb.set)
        self.stack_vsb.pack(side="right", fill="y")
        self.stack_canvas.pack(fill="both", expand=True)

        self.stack_inner = tk.Frame(self.stack_canvas, bg=BG)
        self._stack_window = self.stack_canvas.create_window(
            (0, 0), window=self.stack_inner, anchor="nw")
        self.stack_inner.bind("<Configure>", self._on_stack_configure)
        self.stack_canvas.bind("<Configure>", self._on_canvas_resize)

        # right pane: log + controls
        right_pane = tk.Frame(main, bg=BG2, width=380)
        right_pane.pack(side="right", fill="both", padx=0)
        right_pane.pack_propagate(False)

        # event log
        tk.Label(right_pane, text="LOG  DE  EVENTOS", bg=BG2, fg=TEXT_MUTED,
                 font=("Courier New", 9, "bold"), anchor="w",
                 padx=12, pady=6).pack(fill="x")

        log_frame = tk.Frame(right_pane, bg=BG2)
        log_frame.pack(fill="both", expand=True, padx=8, pady=(0,4))

        self.log_text = tk.Text(log_frame, bg=BG, fg=TEXT_DIM, relief="flat",
                                font=("Courier New", 9), wrap="word",
                                state="disabled", bd=0,
                                highlightthickness=1, highlightbackground=BORDER)
        log_vsb = tk.Scrollbar(log_frame, command=self.log_text.yview,
                               bg=BG3, troughcolor=BG)
        self.log_text.configure(yscrollcommand=log_vsb.set)
        log_vsb.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True)

        # colour tags for log
        self.log_text.tag_configure("call",    foreground=BLUE)
        self.log_text.tag_configure("base",    foreground=YELLOW)
        self.log_text.tag_configure("split",   foreground=ORANGE)
        self.log_text.tag_configure("merge",   foreground=GREEN)
        self.log_text.tag_configure("ret",     foreground=PURPLE)
        self.log_text.tag_configure("dim",     foreground=TEXT_MUTED)
        self.log_text.tag_configure("current", foreground=TEXT,
                                    background="#1c2a1c")

        sep2 = tk.Frame(right_pane, bg=BORDER, height=1)
        sep2.pack(fill="x", padx=8)

        # progress bar area
        prog_area = tk.Frame(right_pane, bg=BG2, padx=12, pady=6)
        prog_area.pack(fill="x")

        self.progress_var = tk.DoubleVar()
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("custom.Horizontal.TProgressbar",
                         troughcolor=BG3, background=GREEN,
                         bordercolor=BG2, lightcolor=GREEN, darkcolor=GREEN,
                         thickness=6)
        self.progress_bar = ttk.Progressbar(prog_area, variable=self.progress_var,
                                             style="custom.Horizontal.TProgressbar",
                                             maximum=100)
        self.progress_bar.pack(fill="x")

        self.step_label = tk.Label(prog_area, text="evento 0 / 0",
                                   bg=BG2, fg=TEXT_MUTED,
                                   font=("Courier New", 8))
        self.step_label.pack(anchor="e")

        sep3 = tk.Frame(right_pane, bg=BORDER, height=1)
        sep3.pack(fill="x", padx=8)

        # speed slider
        speed_area = tk.Frame(right_pane, bg=BG2, padx=12, pady=6)
        speed_area.pack(fill="x")
        tk.Label(speed_area, text="velocidade", bg=BG2, fg=TEXT_MUTED,
                 font=("Courier New", 8)).pack(anchor="w")
        self.speed_var = tk.IntVar(value=700)
        speed_sl = tk.Scale(speed_area, from_=100, to=2000, orient="horizontal",
                            variable=self.speed_var, bg=BG2, fg=TEXT_DIM,
                            troughcolor=BG3, highlightthickness=0,
                            sliderrelief="flat", showvalue=False,
                            command=lambda v: setattr(self, "speed_ms", int(v)))
        speed_sl.pack(fill="x")
        speed_labels = tk.Frame(speed_area, bg=BG2)
        speed_labels.pack(fill="x")
        tk.Label(speed_labels, text="rápido", bg=BG2, fg=TEXT_MUTED,
                 font=("Courier New", 7)).pack(side="left")
        tk.Label(speed_labels, text="lento", bg=BG2, fg=TEXT_MUTED,
                 font=("Courier New", 7)).pack(side="right")

        sep4 = tk.Frame(right_pane, bg=BORDER, height=1)
        sep4.pack(fill="x", padx=8)

        # playback controls
        ctrl = tk.Frame(right_pane, bg=BG2, pady=10)
        ctrl.pack(fill="x")

        btn_cfg = dict(bg=BG3, fg=TEXT, relief="flat",
                       font=("Courier New", 12), cursor="hand2",
                       width=3, pady=4, padx=6)

        self.btn_prev = tk.Button(ctrl, text="⏮", **btn_cfg,
                                  command=self._step_back_many)
        self.btn_prev.pack(side="left", padx=(12,2))

        self.btn_step_back = tk.Button(ctrl, text="◀", **btn_cfg,
                                       command=self._step_back)
        self.btn_step_back.pack(side="left", padx=2)

        self.btn_play = tk.Button(ctrl, text="▶", bg=GREEN_DIM, fg=GREEN,
                                  relief="flat", font=("Courier New", 12, "bold"),
                                  cursor="hand2", width=3, pady=4, padx=6,
                                  command=self._toggle_play)
        self.btn_play.pack(side="left", padx=2)

        self.btn_step = tk.Button(ctrl, text="▶|", **btn_cfg,
                                  command=self._step_forward)
        self.btn_step.pack(side="left", padx=2)

        self.btn_next = tk.Button(ctrl, text="⏭", **btn_cfg,
                                  command=self._step_forward_many)
        self.btn_next.pack(side="left", padx=2)

        # legend
        leg = tk.Frame(right_pane, bg=BG2, padx=12, pady=8)
        leg.pack(fill="x", side="bottom")
        tk.Label(leg, text="LEGENDA", bg=BG2, fg=TEXT_MUTED,
                 font=("Courier New", 8, "bold")).pack(anchor="w")
        legend_items = [
            (BLUE,   "CALL  — nova chamada recursiva"),
            (YELLOW, "BASE  — caso base (fim ≤ 1)"),
            (ORANGE, "SPLIT — dividir vetor"),
            (GREEN,  "MERGE — mesclar resultados"),
            (PURPLE, "RET   — retorno da função"),
        ]
        for color, label in legend_items:
            row = tk.Frame(leg, bg=BG2)
            row.pack(anchor="w", pady=1)
            tk.Label(row, text="■", bg=BG2, fg=color,
                     font=("Courier New", 9)).pack(side="left")
            tk.Label(row, text=label, bg=BG2, fg=TEXT_DIM,
                     font=("Courier New", 8)).pack(side="left", padx=4)

    # ─── SCROLL HELPERS ──────────────────────
    def _on_stack_configure(self, event):
        self.stack_canvas.configure(scrollregion=self.stack_canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.stack_canvas.itemconfig(self._stack_window, width=event.width)

    # ─── DATA LOAD ───────────────────────────
    def _load_data(self, data):
        self.playing = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

        # clear stack area
        for w in self.stack_inner.winfo_children():
            w.destroy()
        self.frame_widgets.clear()
        self.active_stack.clear()
        self.call_meta.clear()

        # clear log
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        tracer = MergeSortTracer(data)
        self.events    = tracer.events
        self.event_idx = 0
        self._update_progress()
        self._update_btn_play()

    def _reload(self):
        try:
            raw  = self.input_var.get()
            data = [int(x.strip()) for x in raw.split(",") if x.strip()]
            if not data:
                raise ValueError
        except ValueError:
            self._log_line("⚠ entrada inválida — use números separados por vírgula", "dim")
            return
        self._load_data(data)

    # ─── PLAYBACK CONTROLS ───────────────────
    def _toggle_play(self):
        self.playing = not self.playing
        self._update_btn_play()
        if self.playing:
            self._schedule_next()

    def _update_btn_play(self):
        if self.playing:
            self.btn_play.configure(text="⏸", bg=ORANGE_DIM, fg=ORANGE)
        else:
            self.btn_play.configure(text="▶", bg=GREEN_DIM, fg=GREEN)

    def _schedule_next(self):
        if not self.playing:
            return
        if self.event_idx >= len(self.events):
            self.playing = False
            self._update_btn_play()
            return
        self._apply_event(self.events[self.event_idx])
        self.event_idx += 1
        self._update_progress()
        self._after_id = self.after(self.speed_ms, self._schedule_next)

    def _step_forward(self):
        if self.event_idx < len(self.events):
            self._apply_event(self.events[self.event_idx])
            self.event_idx += 1
            self._update_progress()

    def _step_back(self):
        """Rebuild from scratch up to event_idx-1."""
        if self.event_idx <= 0:
            return
        target = self.event_idx - 1
        self._rebuild_to(target)

    def _step_back_many(self):
        target = max(0, self.event_idx - 5)
        self._rebuild_to(target)

    def _step_forward_many(self):
        end = min(len(self.events), self.event_idx + 5)
        while self.event_idx < end:
            self._apply_event(self.events[self.event_idx])
            self.event_idx += 1
        self._update_progress()

    def _rebuild_to(self, target):
        """Replay all events from 0..target (exclusive) to restore state."""
        for w in self.stack_inner.winfo_children():
            w.destroy()
        self.frame_widgets.clear()
        self.active_stack.clear()
        self.call_meta.clear()
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self.event_idx = 0
        for i in range(target):
            self._apply_event(self.events[i], silent=(i < target-1))
            self.event_idx += 1
        self._update_progress()

    def _update_progress(self):
        total = len(self.events)
        pct   = (self.event_idx / total * 100) if total else 0
        self.progress_var.set(pct)
        self.step_label.configure(text=f"evento {self.event_idx} / {total}")

    # ─── EVENT RENDERER ──────────────────────
    def _apply_event(self, ev, silent=False):
        kind = ev["kind"]

        if kind == "CALL":
            self._evt_call(ev, silent)
        elif kind == "BASE_CASE":
            self._evt_base(ev, silent)
        elif kind == "SPLIT":
            self._evt_split(ev, silent)
        elif kind == "MERGE":
            self._evt_merge(ev, silent)
        elif kind == "RETURN":
            self._evt_return(ev, silent)

    # ── helpers ──────────────────────────────
    def _log_line(self, text, tag="dim"):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _array_str(self, lst):
        return "[" + ", ".join(str(x) for x in lst) + "]"

    def _depth_indent(self, depth):
        return depth * 26   # px indent per depth level

    def _make_frame(self, call_id, depth, side, title_text, color, vetor):
        indent = self._depth_indent(depth)

        outer = tk.Frame(self.stack_inner, bg=BG, pady=2)
        outer.pack(fill="x", padx=(indent, 6), pady=2)

        inner = tk.Frame(outer, bg=BG2,
                         highlightthickness=1, highlightbackground=color)
        inner.pack(fill="x")

        # title row
        title_row = tk.Frame(inner, bg=color)
        title_row.pack(fill="x")

        side_badge = {"esq": "← L", "dir": "R →", "root": "ROOT"}
        badge_txt  = side_badge.get(side, side)

        tk.Label(title_row, text=f" {badge_txt} ", bg=color, fg=BG,
                 font=("Courier New", 7, "bold")).pack(side="left")
        tk.Label(title_row, text=title_text, bg=color, fg=BG,
                 font=("Courier New", 8, "bold")).pack(side="left", padx=4)
        tk.Label(title_row, text=f"depth={depth}", bg=color, fg=BG2,
                 font=("Courier New", 7)).pack(side="right", padx=4)

        # body
        body = tk.Frame(inner, bg=BG2, padx=6, pady=4)
        body.pack(fill="x")

        # array visualization (boxes)
        arr_frame = tk.Frame(body, bg=BG2)
        arr_frame.pack(anchor="w", pady=(0,2))

        box_size = max(22, min(36, 200 // max(len(vetor), 1)))
        cell_frames = []
        for val in vetor:
            cell = tk.Frame(arr_frame, bg=BG3,
                            width=box_size, height=box_size,
                            highlightthickness=1, highlightbackground=BORDER)
            cell.pack_propagate(False)
            cell.pack(side="left", padx=1)
            lbl = tk.Label(cell, text=str(val), bg=BG3, fg=TEXT,
                           font=("Courier New", 8, "bold"))
            lbl.place(relx=0.5, rely=0.5, anchor="center")
            cell_frames.append((cell, lbl))

        # status label
        status_lbl = tk.Label(body, text="executando…", bg=BG2, fg=TEXT_MUTED,
                               font=("Courier New", 7), anchor="w")
        status_lbl.pack(fill="x")

        self.frame_widgets[call_id] = {
            "outer":       outer,
            "inner":       inner,
            "color":       color,
            "cells":       cell_frames,
            "status_lbl":  status_lbl,
            "body":        body,
            "vetor":       vetor,
            "depth":       depth,
        }
        self._scroll_to_bottom()
        return self.frame_widgets[call_id]

    def _scroll_to_bottom(self):
        self.stack_inner.update_idletasks()
        self.stack_canvas.configure(scrollregion=self.stack_canvas.bbox("all"))
        self.stack_canvas.yview_moveto(1.0)

    def _update_frame_status(self, call_id, text, fg=TEXT_DIM):
        fw = self.frame_widgets.get(call_id)
        if fw:
            fw["status_lbl"].configure(text=text, fg=fg)

    def _highlight_frame(self, call_id, color):
        fw = self.frame_widgets.get(call_id)
        if fw:
            fw["inner"].configure(highlightbackground=color)

    def _dim_frame(self, call_id):
        fw = self.frame_widgets.get(call_id)
        if fw:
            fw["inner"].configure(highlightbackground=TEXT_MUTED)
            fw["status_lbl"].configure(fg=TEXT_MUTED)

    # ── event handlers ───────────────────────
    def _evt_call(self, ev, silent):
        cid   = ev["call_id"]
        depth = ev["depth"]
        side  = ev["side"]
        vetor = ev["vetor"]
        fim   = ev["fim"]

        self.call_meta[cid] = ev
        self.active_stack.append(cid)

        fw = self._make_frame(cid, depth, side,
                              f"merge_sort({self._array_str(vetor)}, fim={fim})",
                              BLUE, vetor)

        if not silent:
            self._highlight_frame(cid, BLUE)
            self._log_line(
                f"{'  '*depth}▶ CALL  depth={depth} {side}  {self._array_str(vetor)}",
                "call")

    def _evt_base(self, ev, silent):
        cid   = ev["call_id"]
        depth = ev["depth"]
        vetor = ev["vetor"]

        self._update_frame_status(cid, "caso base ✓  retorna imediatamente", YELLOW)
        self._highlight_frame(cid, YELLOW)

        # colour cell yellow
        fw = self.frame_widgets.get(cid)
        if fw:
            for cell, lbl in fw["cells"]:
                cell.configure(bg=GREEN_DIM, highlightbackground=GREEN)
                lbl.configure(bg=GREEN_DIM, fg=GREEN)

        if not silent:
            self._log_line(
                f"{'  '*depth}◆ BASE  {self._array_str(vetor)}  ← fim≤1",
                "base")

    def _evt_split(self, ev, silent):
        cid   = ev["call_id"]
        depth = ev["depth"]
        esq   = ev["esq"]
        dir_  = ev["dir"]
        meio  = ev["meio"]

        self._update_frame_status(cid,
            f"split  [{','.join(map(str,esq))}]  |  [{','.join(map(str,dir_))}]",
            ORANGE)
        self._highlight_frame(cid, ORANGE)

        # colour cells: left=orange, right=blue
        fw = self.frame_widgets.get(cid)
        if fw:
            cells = fw["cells"]
            for i, (cell, lbl) in enumerate(cells):
                if i < meio:
                    cell.configure(bg=ORANGE_DIM, highlightbackground=ORANGE)
                    lbl.configure(bg=ORANGE_DIM, fg=ORANGE)
                else:
                    cell.configure(bg=BLUE_DIM, highlightbackground=BLUE)
                    lbl.configure(bg=BLUE_DIM, fg=BLUE)

        if not silent:
            self._log_line(
                f"{'  '*depth}✂ SPLIT depth={depth}  esq{self._array_str(esq)}  dir{self._array_str(dir_)}",
                "split")

    def _evt_merge(self, ev, silent):
        cid    = ev["call_id"]
        depth  = ev["depth"]
        esq    = ev["esq"]
        dir_   = ev["dir"]
        result = ev["result"]

        self._update_frame_status(cid,
            f"⊕ merge  {self._array_str(esq)} + {self._array_str(dir_)} → {self._array_str(result)}",
            GREEN)
        self._highlight_frame(cid, GREEN)

        # recolour cells with merged result
        fw = self.frame_widgets.get(cid)
        if fw:
            cells = fw["cells"]
            # replace cell values with result
            for i, val in enumerate(result):
                if i < len(cells):
                    cell, lbl = cells[i]
                    lbl.configure(text=str(val), fg=GREEN, bg=GREEN_DIM)
                    cell.configure(bg=GREEN_DIM, highlightbackground=GREEN)

        if not silent:
            self._log_line(
                f"{'  '*depth}⊕ MERGE depth={depth}  {self._array_str(esq)} ⊕ {self._array_str(dir_)} → {self._array_str(result)}",
                "merge")

    def _evt_return(self, ev, silent):
        cid    = ev["call_id"]
        pid    = ev["parent_id"]
        depth  = ev["depth"]
        result = ev["result"]

        self._dim_frame(cid)
        # pop from active stack
        if cid in self.active_stack:
            self.active_stack.remove(cid)

        if not silent:
            self._log_line(
                f"{'  '*depth}↩ RET   depth={depth}  → {self._array_str(result)}",
                "ret")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = MergeSortVisualizer()
    app.mainloop()