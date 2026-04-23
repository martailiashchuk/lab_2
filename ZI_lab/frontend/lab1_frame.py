import customtkinter as ctk

class Lab1Frame(ctk.CTkFrame):
    def __init__(self, master, service, on_back):
        super().__init__(master, fg_color="#1E1B2E")
        self.service = service

        ctk.CTkButton(self, text="← Back to Menu", command=on_back, width=110, height=30,
                      fg_color="#7B2CBF", hover_color="#9D4EDD", corner_radius=10).pack(anchor="nw", padx=45, pady=15)

        self.title = ctk.CTkLabel(
            self, text="Lemer Algorithm\n",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#E0AAFF"
        )
        self.title.pack(pady=(0, 5))

        self.entry = ctk.CTkEntry(
            self, width=260, height=40, corner_radius=15,
            placeholder_text="Enter your number", fg_color="#2A2438",
            text_color="#F1E1FF", border_width=0
        )
        self.entry.pack(pady=5)

        self.btn = ctk.CTkButton(
            self, text="Run", command=self.run,
            width=260, height=40, corner_radius=15,
            fg_color="#7B2CBF", hover_color="#9D4EDD",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn.pack(pady=10)

        self.period_out = self._create_output_field("Period:", 35)
        self.prob_out = self._create_output_field("Probability (P):", 35)
        self.pi_out = self._create_output_field("PI (Lemer):", 35)
        self.pi_rand_out = self._create_output_field("PI (System Random):", 35)
        self.seq_out = self._create_output_field("Sequence:", 100)

    def _create_output_field(self, label_text, height):
        label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0AAFF")
        label.pack(padx=45, anchor="nw", pady=(2, 0))
        field = ctk.CTkTextbox(self, width=560, height=height, corner_radius=12, fg_color="#2A2438", text_color="#F1E1FF", border_width=0)
        field.pack(pady=(2, 5))
        return field

    def run(self):
        self._clear_fields()

        val = self.entry.get().strip()

        if not val or not val.isdigit() or int(val) <= 1:
            self._display_error()
            return

        try:
            n = int(val)
            self.entry.configure(placeholder_text="Enter your number")

            seq = self.service.generate(n)
            p = self.service.cesaro_test(seq)
            pi_l = self.service.estimate_pi(p)
            pi_s = self.service.get_system_random_pi(n)
            period = self.service.calculate_period()

            self.period_out.insert("0.0", f"Period: {period}")
            self.prob_out.insert("0.0", f"P = {p:.4f}")
            self.pi_out.insert("0.0", f"PI = {pi_l:.6f}")
            self.pi_rand_out.insert("0.0", f"PI = {pi_s:.6f}")
            self.seq_out.insert("0.0", " ".join(map(str, seq)))

        except Exception:
            self._display_error()

    def _display_error(self):
        self.entry.delete(0, "end")
        self.entry.configure(placeholder_text="Error: Enter your number")
        self.focus()

    def _clear_fields(self):
        self.period_out.delete("0.0", "end")
        self.prob_out.delete("0.0", "end")
        self.pi_out.delete("0.0", "end")
        self.pi_rand_out.delete("0.0", "end")
        self.seq_out.delete("0.0", "end")