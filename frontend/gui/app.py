import math
import time
import tkinter as tk
import customtkinter as ctk
from backend.simulation import Simulation
from backend.config import (WIDTH, HEIGHT, BG_COLOR, 
                            TRAIL_COLOR, FRAME_DELAY_MS, GLOW_RINGS, GLOW_SPREAD, 
                            GLOW_ENABLED, EASE, TRAIL_FADE, HUD_COLOR, HUD_FONT)
from backend.colors import blend


ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stable Particle Collision")
        self.resizable(False, False)
        self.sim = Simulation()
        self._running = True
        self._build_ui()
        self._paused = False
        self.bind("<space>", self._toggle_pause)
        self.canvas.bind("<Button-2>", self._on_repel)   # mac right-click
        self.canvas.bind("<Button-3>", self._on_repel)   # linux/win right-click
        self.canvas.bind("<Control-Button-1>", self._on_repel)  # mac trackpad fallback
        self._fps = 0.0
        self._last_t = time.perf_counter()
        self._loop()

    def _build_ui(self):
        self.canvas = tk.Canvas(
            self, width=WIDTH, height=HEIGHT,
            bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.bind("<Button-1>", self._on_click)

        self.canvas.pack(padx=10, pady=(10,0))

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=10, pady=10)

        ctk.CTkSlider(
            controls, from_=0, to=2000,
            command=self._on_count
        ).pack(side="left", padx=5, fill="x", expand=True)


        ctk.CTkButton(controls, text="Reset", command=self._reset).pack(side="left", padx=5)

    def _loop(self):
        if not self._running:
            return
        if not self._paused:
            self.sim.tick()
        self._render()
        now = time.perf_counter()
        dt = now - self._last_t
        self._last_t = now
        if dt > 0:
            self._fps += (1.0/dt - self._fps) * 0.1   # smoothed

        self.after(FRAME_DELAY_MS, self._loop)

    def _render(self):
        self.canvas.delete("all")
        for p in self.sim.particles:
            if p.is_special and GLOW_ENABLED:
                pulse = 0.5 + 0.5 * math.sin(p.pulse_phase)   # 0..1
                for k in range(GLOW_RINGS, 0, -1):
                    gr = p.radius * (1 + GLOW_SPREAD * k) * (0.8 + 0.4 * pulse)/2          # outer -> inner
                    t = k / GLOW_RINGS                       # outer = dimmer
                    gcol = blend(p.color, BG_COLOR, 0.5 + 0.5 * t)
                    self.canvas.create_oval(
                        p.x - gr, p.y - gr, p.x + gr, p.y + gr,
                        fill=gcol, outline=""
                    )
            if p.is_special and len(p.path) > 2:
                n = len(p.path)
                for i in range(1, n):
                    x0, y0 = p.path[i-1]
                    x1, y1 = p.path[i]
                    if TRAIL_FADE:
                        t = i / n
                        color = blend(BG_COLOR, p.trail_color, t)
                        w = max(1, int(t * 3))
                    else:
                        color = p.trail_color
                        w = 2
                    self.canvas.create_line(x0, y0, x1, y1, fill=color, width=w)

            x0, y0 = p.x - p.radius, p.y - p.radius
            x1, y1 = p.x + p.radius, p.y + p.radius
            self.canvas.create_oval(x0, y0, x1, y1, fill=p.color, outline="")

            blue_count = sum(1 for p in self.sim.particles if not p.is_special)
            hud = f"Blue: {blue_count}   FPS: {self._fps:.0f}"
            if self._paused:
                hud += "   [PAUSED]"
            self.canvas.create_text(
                WIDTH - 10, 10, text=hud,
                fill=HUD_COLOR, anchor="ne", font=HUD_FONT
            )

    def _reset(self):
        self.sim.reset()

    def on_close(self):
        self._running = False
        self.destroy()

    def _on_click(self, event):
        self.sim.spawn(event.x, event.y)

    def _toggle_pause(self, event=None):
        self._paused = not self._paused

    def _on_count(self, value):
        self.sim.set_blue_count(int(value))

    def _on_repel(self, event):
        self.sim.repel(event.x, event.y)

