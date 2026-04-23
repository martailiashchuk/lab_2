import customtkinter as ctk
from tkinter import filedialog, messagebox


class Lab5Frame(ctk.CTkFrame):
    def __init__(self, master, sig_service, on_back):
        super().__init__(master, fg_color="#1E1B2E")
        self.sig_service = sig_service

        # Заголовок та кнопка назад
        ctk.CTkButton(self, text="← Menu", command=on_back, fg_color="#7B2CBF", hover_color="#9D4EDD", width=80).pack(
            anchor="nw", padx=20, pady=10)
        ctk.CTkLabel(self, text="Lab 5: Digital Signature Standard (DSS)", font=("Arial", 22, "bold"),
                     text_color="#E0AAFF").pack(pady=5)

        # 1. Керування ключами
        key_frame = ctk.CTkFrame(self, fg_color="#2A2438")
        key_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(key_frame, text="Generate DSA Keys", command=self.gen_keys, fg_color="#5A189A").pack(pady=10)

        # 2. Ввід тексту (Рядка)
        input_frame = ctk.CTkFrame(self, fg_color="#2A2438")
        input_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(input_frame, text="Input String for Signature:", text_color="#E0AAFF").pack(anchor="w", padx=15)
        self.text_input = ctk.CTkEntry(input_frame, fg_color="#1E1B2E", border_color="#7B2CBF", text_color="white")
        self.text_input.pack(fill="x", padx=15, pady=10)

        # 3. Вивід підпису (HEX)
        ctk.CTkLabel(self, text="Signature Value (HEX):", text_color="#E0AAFF").pack()
        self.sig_output = ctk.CTkTextbox(self, height=100, fg_color="#1E1B2E", border_color="#9D4EDD", border_width=1)
        self.sig_output.pack(fill="x", padx=20, pady=5)

        # 4. Панель кнопок
        btn_grid = ctk.CTkFrame(self, fg_color="transparent")
        btn_grid.pack(pady=10, padx=20, fill="x")

        # Кнопки підпису
        ctk.CTkButton(btn_grid, text="Sign String", command=self.sign_text, fg_color="#7B2CBF").grid(row=0, column=0,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky="ew")
        ctk.CTkButton(btn_grid, text="Sign File", command=self.sign_file, fg_color="#7B2CBF").grid(row=0, column=1,
                                                                                                   padx=5, pady=5,
                                                                                                   sticky="ew")

        # Кнопки збереження та перевірки
        ctk.CTkButton(btn_grid, text="Save HEX to File", command=self.save_sig, fg_color="#5A189A").grid(row=1,
                                                                                                         column=0,
                                                                                                         padx=5, pady=5,
                                                                                                         sticky="ew")
        ctk.CTkButton(btn_grid, text="Verify File Signature", command=self.verify_file, fg_color="#5A189A").grid(row=1,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5,
                                                                                                                 sticky="ew")

        btn_grid.grid_columnconfigure((0, 1), weight=1)




    def gen_keys(self):
        folder = filedialog.askdirectory(title="Select folder for DSA keys")
        if folder:
            _, _ = self.sig_service.generate_dsa_keys(folder)
            messagebox.showinfo("Success", f"Keys saved to:\n{folder}")

    def sign_text(self):
        text_data = self.text_input.get().encode('utf-8')
        if not text_data:
            messagebox.showwarning("Warning", "Please enter some text")
            return
        key_path = filedialog.askopenfilename(title="Select Private Key")
        if key_path:
            hex_sig = self.sig_service.sign_data(text_data, key_path)
            self.sig_output.delete("1.0", "end")
            self.sig_output.insert("1.0", hex_sig)

    def sign_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Sign")
        if not file_path: return
        key_path = filedialog.askopenfilename(title="Select Private Key")
        if not key_path: return

        with open(file_path, "rb") as f:
            data = f.read()
        hex_sig = self.sig_service.sign_data(data, key_path)
        self.sig_output.delete("1.0", "end")
        self.sig_output.insert("1.0", hex_sig)

    def save_sig(self):
        hex_data = self.sig_output.get("1.0", "end-1c").strip()
        if not hex_data: return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(hex_data)
            messagebox.showinfo("Saved", "Signature HEX saved successfully")

    def verify_file(self):
        file_path = filedialog.askopenfilename(title="Select Original File")
        sig_file = filedialog.askopenfilename(title="Select Signature HEX File (.txt)")
        key_file = filedialog.askopenfilename(title="Select Public Key")

        if not (file_path and sig_file and key_file): return

        with open(file_path, "rb") as f:
            data = f.read()
        with open(sig_file, "r") as f:
            hex_sig = f.read().strip()

        is_valid = self.sig_service.verify_data(data, hex_sig, key_file)
        if is_valid:

            messagebox.showinfo("Result", "✅ ПІДПИС ВІРНИЙ")
        else:

            messagebox.showerror("Result", "❌ ПІДПИС НЕВІРНИЙ")