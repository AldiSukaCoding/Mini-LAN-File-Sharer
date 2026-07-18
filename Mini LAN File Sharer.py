import os
import socket
import threading
import http.server
import socketserver
import platform
import subprocess
import customtkinter as ctk
from tkinter import filedialog
import pyqrcode
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
class LanFileSharerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📡 Mini LAN File Sharer Pro")
        self.geometry("600x620")
        self.resizable(False, False)
        self.file_path = ""
        self.ip_lokal = self.dapatkan_ip_lokal()
        self.port = 8080
        self.server_thread = None
        self.httpd = None
        self.title_label = ctk.CTkLabel(self, text="LAN File Sharer", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(padx=20, pady=(20, 5))
        self.sub_label = ctk.CTkLabel(self, text="Bagikan berkas ke perangkat lain dalam satu jaringan Wi-Fi lokal", font=ctk.CTkFont(size=12, slant="italic"))
        self.sub_label.pack(padx=20, pady=(0, 15))
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(padx=20, pady=10, fill="x")      
        self.lbl_ip = ctk.CTkLabel(self.info_frame, text=f"📍 IP Lokal Anda: {self.ip_lokal}", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_ip.pack(padx=20, pady=(10, 5), anchor="w")    
        self.lbl_status_server = ctk.CTkLabel(self.info_frame, text="🟢 Status Server: Berhenti", text_color="orange", font=ctk.CTkFont(size=12))
        self.lbl_status_server.pack(padx=20, pady=(0, 10), anchor="w")
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(padx=20, pady=10, fill="x")      
        self.btn_select = ctk.CTkButton(self.file_frame, text="📁 Pilih Berkas", width=120, command=self.pilih_berkas)
        self.btn_select.grid(row=0, column=0, padx=(10, 10))      
        self.lbl_file_name = ctk.CTkLabel(self.file_frame, text="Belum ada berkas yang dipilih...", text_color="gray", font=ctk.CTkFont(size=12))
        self.lbl_file_name.grid(row=0, column=1, sticky="w")
        self.qr_frame = ctk.CTkFrame(self, width=220, height=220, fg_color="#2b2b2b")
        self.qr_frame.pack(padx=20, pady=15)
        self.qr_frame.pack_propagate(False)     
        self.lbl_qr_placeholder = ctk.CTkLabel(self.qr_frame, text="QR Code\nKemunculan di sini\nsetelah server aktif", text_color="gray")
        self.lbl_qr_placeholder.pack(expand=True)
        self.log_text = ctk.CTkTextbox(self, width=560, height=120, font=ctk.CTkFont(family="Courier", size=11))
        self.log_text.pack(padx=20, pady=10)
        self.log_text.configure(state="disabled")
        self.cetak_log("[SISTEM]: Aplikasi siap. Pastikan Anda terhubung ke Wi-Fi.")
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(padx=20, pady=10)    
        self.btn_start = ctk.CTkButton(self.action_frame, text="▶️ Aktifkan Server", width=180, height=40, font=ctk.CTkFont(weight="bold"), fg_color="#2b719e", hover_color="#1f5375", command=self.mulai_server_thread)
        self.btn_start.grid(row=0, column=0, padx=10)    
        self.btn_stop = ctk.CTkButton(self.action_frame, text="⏹️ Matikan Server", width=180, height=40, font=ctk.CTkFont(weight="bold"), fg_color="#a83232", hover_color="#822525", command=self.hentikan_server)
        self.btn_stop.grid(row=0, column=1, padx=10)
        self.btn_stop.configure(state="disabled")
    def cetak_log(self, teks):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", teks + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    def dapatkan_ip_lokal(self):
        """Mendeteksi IP Address komputer di jaringan Wi-Fi lokal."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    def pilih_berkas(self):
        path = filedialog.askopenfilename(title="Pilih Berkas untuk Dibagikan")
        if path:
            self.file_path = path
            nama_file = os.path.basename(path)
            self.lbl_file_name.configure(text=nama_file if len(nama_file) <= 40 else f"{nama_file[:37]}...", text_color="white")
            self.cetak_log(f"📂 [BERKAS]: Berkas terpilih -> {nama_file}")
    def mulai_server_thread(self):
        if not self.file_path:
            self.cetak_log("⚠️ [PERINGATAN]: Silakan pilih berkas terlebih dahulu!")
            return       
        self.btn_start.configure(state="disabled")
        self.btn_select.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.server_thread = threading.Thread(target=self.jalankan_server, daemon=True)
        self.server_thread.start()
    def jalankan_server(self):
        folder_berkas = os.path.dirname(self.file_path)
        nama_berkas = os.path.basename(self.file_path)
        os.chdir(folder_berkas)
        Handler = http.server.SimpleHTTPRequestHandler
        while True:
            try:
                self.httpd = socketserver.TCPServer((self.ip_lokal, self.port), Handler)
                break
            except OSError:
                self.port += 1  
        tautan_unduhan = f"http://{self.ip_lokal}:{self.port}/{nama_berkas}"
        self.after(0, self.perbarui_ui_server_aktif, tautan_unduhan)   
        self.cetak_log(f"\n🚀 [SERVER]: Server aktif pada port {self.port}")
        self.cetak_log(f"🔗 [LINK]: {tautan_unduhan}")
        self.cetak_log("📱 [TIPS]: Scan QR Code di atas menggunakan HP untuk mengunduh langsung.")
        try:
            self.httpd.serve_forever()
        except Exception:
            pass
    def perbarui_ui_server_aktif(self, tautan):
        self.lbl_status_server.configure(text=f"🔵 Status Server: Berjalan di Port {self.port}", text_color="green")
        qr = pyqrcode.create(tautan)
        qr_path = os.path.join(os.path.expanduser("~"), "temp_sharer_qr.png")
        qr.png(qr_path, scale=5)
        from PIL import Image
        img_qr = ctk.CTkImage(light_image=Image.open(qr_path), dark_image=Image.open(qr_path), size=(200, 200))
        self.lbl_qr_placeholder.configure(image=img_qr, text="")
        try:
            os.remove(qr_path)
        except Exception:
            pass
    def hentikan_server(self):
        if self.httpd:
            threading.Thread(target=self.httpd.shutdown, daemon=True).start()
            self.httpd.server_close()
        self.lbl_status_server.configure(text="條 Status Server: Berhenti", text_color="orange")
        self.lbl_qr_placeholder.configure(image=None, text="QR Code\nKemunculan di sini\nsetelah server aktif")      
        self.btn_start.configure(state="normal")
        self.btn_select.configure(state="normal")
        self.btn_stop.configure(state="disabled")     
        self.cetak_log("\n⏹️ [SERVER]: Server berhasil dimatikan secara aman.")
if __name__ == "__main__":
    app = LanFileSharerApp()
    app.mainloop()