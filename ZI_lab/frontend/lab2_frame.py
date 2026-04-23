import customtkinter as ctk
from tkinter import filedialog, messagebox


class Lab2Frame(ctk.CTkFrame):
    def __init__(self, master, service, on_back):
        super().__init__(master, fg_color="#1E1B2E")
        self.service = service

        ctk.CTkButton(self, text="← Back to Menu", command=on_back, width=110, height=30,
                      fg_color="#7B2CBF", hover_color="#9D4EDD", corner_radius=10).pack(anchor="nw", padx=45, pady=15)

        ctk.CTkLabel(self, text="MD5 Integrity Tool", font=("Arial", 22, "bold"), text_color="#E0AAFF").pack(pady=5)

        self.entry = ctk.CTkEntry(self, width=400, height=40, corner_radius=15,
                                  placeholder_text="Enter text to hash", fg_color="#2A2438", border_width=0)
        self.entry.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Hash Text", command=self.run_text, width=120, fg_color="#7B2CBF").grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=5)
        ctk.CTkButton(btn_frame, text="Select File", command=self.run_file, width=120, fg_color="#9D4EDD").grid(row=0,
                                                                                                                column=1,
                                                                                                                padx=5)
        ctk.CTkButton(btn_frame, text="Save to File", command=self.save_result, width=120, fg_color="#5A189A").grid(
            row=0, column=2, padx=5)


        ctk.CTkLabel(self, text="Result (MD5 Hash):", text_color="#E0AAFF", font=("Arial", 13, "bold")).pack(
            anchor="nw", padx=45, pady=(15, 0))
        self.res_box = ctk.CTkTextbox(self, width=560, height=80, corner_radius=12, fg_color="#2A2438",
                                      text_color="#F1E1FF")
        self.res_box.pack(pady=5)

        ctk.CTkLabel(self, text="Verify with existing Hash:", text_color="#E0AAFF", font=("Arial", 13, "bold")).pack(
            anchor="nw", padx=45, pady=(15, 0))
        self.verify_entry = ctk.CTkEntry(self, width=560, height=40, corner_radius=12,
                                         placeholder_text="Paste hash to compare", fg_color="#2A2438", border_width=0)
        self.verify_entry.pack(pady=5)

        ctk.CTkButton(self, text="Verify Integrity", command=self.verify_integrity, width=200, height=40,
                      corner_radius=15, fg_color="#7B2CBF").pack(pady=15)

    def run_text(self):
        text = self.entry.get()
        if not text: return
        result = self.service.hash_text(text)
        self._display_result(result)

    def run_file(self):
        path = filedialog.askopenfilename()
        if path:
            result = self.service.hash_file(path)
            self._display_result(result)
            messagebox.showinfo("Success", f"File processed!\n{path}")

    def verify_integrity(self):
        current = self.res_box.get("1.0", "end-1c").strip().upper()
        expected = self.verify_entry.get().strip().upper()

        if not current or not expected:
            messagebox.showwarning("Warning", "Generate a hash first!")
            return

        if current == expected:
            messagebox.showinfo("Integrity", "✅ Hashes match! File is authentic.")
        else:
            messagebox.showerror("Integrity", "❌ Hashes do NOT match! File corrupted.")

    def save_result(self):
        content = self.res_box.get("1.0", "end-1c").strip()
        if not content: return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w") as f: f.write(f"MD5: {content}")
            messagebox.showinfo("Saved", "Result saved to disk.")

    def _display_result(self, val):
        self.res_box.delete("1.0", "end")
        self.res_box.insert("1.0", val)