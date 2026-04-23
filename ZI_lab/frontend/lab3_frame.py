import customtkinter as ctk
from tkinter import filedialog, messagebox


class Lab3Frame(ctk.CTkFrame):
    def __init__(self, master, services, on_back):
        super().__init__(master, fg_color="#1E1B2E")
        self.lcg, self.md5, self.rc5 = services['lcg'], services['md5'], services['rc5']

        ctk.CTkButton(self, text="← Menu", command=on_back, width=90, fg_color="#7B2CBF").pack(anchor="nw", padx=20,
                                                                                               pady=10)
        ctk.CTkLabel(self, text="RC5-CBC-Pad (w=64, r=8, b=32)", font=("Arial", 20, "bold"), text_color="#E0AAFF").pack(
            pady=10)

        self.pass_entry = ctk.CTkEntry(self, width=400, height=45, placeholder_text="Password Phrase", show="*",
                                       fg_color="#2A2438", border_width=0)
        self.pass_entry.pack(pady=20)

        btn_f = ctk.CTkFrame(self, fg_color="transparent")
        btn_f.pack(pady=10)
        ctk.CTkButton(btn_f, text="Encrypt File", command=self.encrypt, width=160, height=45, fg_color="#7B2CBF").grid(
            row=0, column=0, padx=10)
        ctk.CTkButton(btn_f, text="Decrypt File", command=self.decrypt, width=160, height=45, fg_color="#9D4EDD").grid(
            row=0, column=1, padx=10)

    def encrypt(self):
        pw = self.pass_entry.get()
        if not pw:
            return
        path = filedialog.askopenfilename()
        if path:
            try:
                self.rc5.encrypt_file(path, path + ".enc", pw, self.md5, self.lcg)
                messagebox.showinfo("Success", "File encrypted!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encrypt: {e}")

    def decrypt(self):
        pw = self.pass_entry.get()
        path = filedialog.askopenfilename(filetypes=[("Encrypted", "*.enc")])
        if path:
            try:
                self.rc5.decrypt_file(path, path.replace(".enc", ".dec"), pw, self.md5)
                messagebox.showinfo("Success", "File decrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Decryption failed. Check your password! \n({e})")
