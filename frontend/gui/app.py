import tkinter as tk
import customtkinter as ctk
from backend.simulation import Simulation
from backend.config import WIDTH, HEIGHT, BG_COLOR, TRAIL_COLOR, FRAME_DELAY_MS

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stable Particle Collision")
        self.resizable(False, False)
        self.sim = Simulation()
        self._running = True
        self._build_ui()
        self._loop()

    def _build_ui(self):
        self.canvas = tk.Canvas(
            self, width=WIDTH, height=HEIGHT,
            bg=BG_COLOR, highlightthickness=0
        )
        
        self.canvas.pack(padx=10, pady=(10,0))

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(controls, text="Reset", command=self._reset).pack(side="left", padx=5)

    def _loop(self):
        if not self._running:
            return
        self.sim.tick()
        self._render()
        self.after(FRAME_DELAY_MS, self._loop)

    def _render(self):
        self.canvas.delete("all")
        for p in self.sim.particles:
            if p.is_special and len(p.path) > 2:
                flat = [coord for point in p.path for coord in point]
                self.canvas.create_line(flat, fill=p.trail_color, width=2)
            x0, y0 = p.x - p.radius, p.y - p.radius
            x1, y1 = p.x + p.radius, p.y + p.radius
            self.canvas.create_oval(x0, y0, x1, y1, fill=p.color, outline="")

    def _reset(self):
        self.sim.reset()

    def on_close(self):
        self._running = False
        self.destroy()


