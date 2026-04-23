import customtkinter as ctk
from tkinter import filedialog, messagebox
import time


class Lab4Frame(ctk.CTkFrame):
    def __init__(self, master, rsa_service, on_back):
        super().__init__(master, fg_color="#1E1B2E")
        self.rsa = rsa_service

        ctk.CTkButton(self, text="← Menu", command=on_back,
                      fg_color="#7B2CBF", hover_color="#9D4EDD", width=80).pack(anchor="nw", padx=20, pady=10)

        ctk.CTkLabel(self, text="Lab 4: RSA Asymmetric Encryption",
                     font=("Arial", 22, "bold"), text_color="#E0AAFF").pack(pady=5)

        key_frame = ctk.CTkFrame(self, fg_color="#2A2438")
        key_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(key_frame, text="Key Management", font=("Arial", 14, "bold"), text_color="#C77DFF").pack(pady=5)
        ctk.CTkButton(key_frame, text="Generate & Save RSA Keys",
                      command=self.handle_generate, fg_color="#5A189A", hover_color="#7B2CBF", width=300).pack(pady=10)

        ops_frame = ctk.CTkFrame(self, fg_color="#2A2438")
        ops_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(ops_frame, text="File Operations", font=("Arial", 14, "bold"), text_color="#C77DFF").pack(pady=5)

        ctk.CTkButton(ops_frame, text="Encrypt File (with Public Key)",
                      command=self.handle_encrypt, fg_color="#7B2CBF", hover_color="#9D4EDD", width=300).pack(pady=10)

        ctk.CTkButton(ops_frame, text="Decrypt File (with Private Key)",
                      command=self.handle_decrypt, fg_color="#3C096C", hover_color="#5A189A", width=300).pack(pady=10)

        status_frame = ctk.CTkFrame(self, fg_color="#161426", height=40)
        status_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        self.status = ctk.CTkLabel(status_frame, text="Status: Ready", text_color="#E0AAFF")
        self.status.pack(pady=5)

    def handle_generate(self):
        folder = filedialog.askdirectory(title="Виберіть папку для збереження ключів")
        if folder:
            try:
                priv, pub = self.rsa.save_keys_to_dir(folder)
                self.status.configure(text="Status: Keys Generated Successfully", text_color="#00FF41")
                messagebox.showinfo("Готово", f"RSA Ключі збережено:\n1. {priv}\n2. {pub}")
            except Exception:
                messagebox.showerror("Error", "Помилка генерації ключів.")

    def handle_encrypt(self):
        target_file = filedialog.askopenfilename(title="Виберіть файл для шифрування")
        if not target_file:
            return

        key_file = filedialog.askopenfilename(title="Виберіть ПУБЛІЧНИЙ ключ (public_key.pem)",
                                              filetypes=[("PEM files", "*.pem")])
        if not key_file:
            return

        try:
            start = time.time()
            res = self.rsa.encrypt_file(target_file, key_file)
            elapsed = time.time() - start
            self.status.configure(text=f"Status: Encrypted in {elapsed:.4f}s", text_color="#00FF41")
            messagebox.showinfo("Успіх", f"Файл зашифровано: {res}")
        except Exception as e:
            self.status.configure(text="Status: Encryption Error", text_color="#FF4B2B")
            messagebox.showerror("Помилка", f"Не вдалося зашифрувати: {e}")

    def handle_decrypt(self):
        target_file = filedialog.askopenfilename(title="Виберіть .rsa файл")
        if not target_file:
            return

        key_file = filedialog.askopenfilename(title="Виберіть ПРИВАТНИЙ ключ (private_key.pem)",
                                              filetypes=[("PEM files", "*.pem")])
        if not key_file:
            return

        try:
            start = time.time()
            res = self.rsa.decrypt_file(target_file, key_file)
            elapsed = time.time() - start
            self.status.configure(text=f"Status: Decrypted in {elapsed:.4f}s", text_color="#00FF41")
            messagebox.showinfo("Успіх", f"Файл розшифровано: {res}")
        except Exception:
            self.status.configure(text="Status: Decryption Error", text_color="#FF4B2B")
            messagebox.showerror("Помилка", "Не вдалося розшифрувати. Перевірте, чи це правильний RSA-ключ.")
