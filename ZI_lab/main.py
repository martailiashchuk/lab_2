import customtkinter as ctk
from backend.lcg_service import LCGService
from backend.md5_service import MD5Service
from backend.rc5_service import RC5Service
from backend.rsa_service import RSAService
from backend.dss_service import DSSService
from frontend.lab1_frame import Lab1Frame
from frontend.lab2_frame import Lab2Frame
from frontend.lab3_frame import Lab3Frame
from frontend.lab4_frame import Lab4Frame
from frontend.lab5_frame import Lab5Frame


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Security Algorithms Suite")
        self.geometry("650x800")
        self.configure(fg_color="#1E1B2E")

        self.services = {
            'lcg': LCGService(),
            'md5': MD5Service(),
            'rc5': RC5Service(),
            'rsa': RSAService(),
            'dss': DSSService()
        }

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.show_menu()

    def show_menu(self):
        for w in self.container.winfo_children(): w.destroy()
        ctk.CTkLabel(self.container, text="ZI LABS", font=("Arial", 28, "bold"), text_color="#E0AAFF").pack(pady=60)

        for name, n in [("Lab 1: LCG Generator", 1), ("Lab 2: MD5 Hash", 2), ("Lab 3: RC5 File Cipher", 3), ("Lab 4: RSA", 4), ("Lab 5: DSS", 5)]:
            ctk.CTkButton(self.container, text=name, width=320, height=55, corner_radius=15,
                          fg_color="#7B2CBF", font=("Arial", 14, "bold"),
                          command=lambda x=n: self._show_lab(x)).pack(pady=12)

    def _show_lab(self, n):
        for w in self.container.winfo_children(): w.destroy()
        if n == 1:
            Lab1Frame(self.container, self.services['lcg'], self.show_menu).pack(fill="both", expand=True)
        elif n == 2:
            Lab2Frame(self.container, self.services['md5'], self.show_menu).pack(fill="both", expand=True)
        elif n == 3:
            Lab3Frame(self.container, self.services, self.show_menu).pack(fill="both", expand=True)
        elif n == 4:
            Lab4Frame(self.container, self.services['rsa'], self.show_menu).pack(fill="both", expand=True)
        elif n == 5:
            Lab5Frame(self.container, self.services['dss'], self.show_menu).pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MainApp()
    app.mainloop()