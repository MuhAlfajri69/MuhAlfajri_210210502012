import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Data buku
buku_list = [
    {"kode": "BK001", "judul": "Pemrograman Python", "penulis": "Andi", "tahun": 2021},
    {"kode": "BK002", "judul": "Dasar-Dasar Jaringan", "penulis": "Budi", "tahun": 2020},
    {"kode": "BK003", "judul": "Algoritma dan Struktur Data", "penulis": "Cici", "tahun": 2019},
    {"kode": "BK004", "judul": "Machine Learning Dasar", "penulis": "Dedi", "tahun": 2022},
    {"kode": "BK005", "judul": "Sistem Operasi Modern", "penulis": "Eka", "tahun": 2018},
    {"kode": "BK006", "judul": "Pemrograman Java Lanjutan", "penulis": "Andi", "tahun": 2021},
    {"kode": "BK007", "judul": "Deep Learning dengan Python", "penulis": "Fajar", "tahun": 2023},
    {"kode": "BK008", "judul": "Kecerdasan Buatan", "penulis": "Gina", "tahun": 2020},
    {"kode": "BK009", "judul": "Jaringan Komputer Lanjut", "penulis": "Budi", "tahun": 2022},
    {"kode": "BK010", "judul": "Dasar-Dasar Data Mining", "penulis": "Hana", "tahun": 2021},
    {"kode": "BK011", "judul": "Big Data untuk Pemula", "penulis": "Irfan", "tahun": 2023},
    {"kode": "BK012", "judul": "Cloud Computing", "penulis": "Joko", "tahun": 2020},
    {"kode": "BK013", "judul": "Etika Profesi TI", "penulis": "Kiki", "tahun": 2019},
    {"kode": "BK014", "judul": "Keamanan Siber Dasar", "penulis": "Lina", "tahun": 2022},
    {"kode": "BK015", "judul": "Pemrograman Web dengan Flask", "penulis": "Andi", "tahun": 2023},
]

class SistemRekomendasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Rekomendasi Buku")
        self.root.geometry("650x500")

        # Simulasi riwayat pinjam pengguna
        self.riwayat_peminjaman = []

        # Judul
        tk.Label(root, text="Pilih Buku yang Sudah Pernah Dipinjam:").pack(pady=5)
        self.buku_var = tk.StringVar()
        self.buku_menu = ttk.Combobox(root, textvariable=self.buku_var, width=50)
        self.buku_menu['values'] = [b["judul"] for b in buku_list]
        self.buku_menu.pack(pady=5)

        ttk.Button(root, text="Tambahkan ke Riwayat", command=self.tambah_riwayat).pack(pady=5)

        self.riwayat_label = tk.Label(root, text="Riwayat Peminjaman: (Kosong)")
        self.riwayat_label.pack(pady=10)

        ttk.Button(root, text="Tampilkan Rekomendasi", command=self.rekomendasi).pack(pady=10)

        # Tabel hasil
        self.tree = ttk.Treeview(root, columns=("kode", "judul", "penulis", "tahun", "similarity"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
        self.tree.pack(expand=True, fill='both')

    def tambah_riwayat(self):
        judul = self.buku_var.get()
        if not judul:
            messagebox.showwarning("Peringatan", "Pilih buku terlebih dahulu.")
            return
        if judul not in self.riwayat_peminjaman:
            self.riwayat_peminjaman.append(judul)
            self.riwayat_label.config(text=f"Riwayat Peminjaman: {', '.join(self.riwayat_peminjaman)}")
        else:
            messagebox.showinfo("Info", "Buku sudah ada di riwayat.")

    def rekomendasi(self):
        if not self.riwayat_peminjaman:
            messagebox.showwarning("Peringatan", "Riwayat peminjaman kosong.")
            return

        # Gabungkan semua judul buku yang dipinjam sebagai 1 dokumen
        input_user = " ".join(self.riwayat_peminjaman)

        semua_judul = [b["judul"] for b in buku_list]
        judul_tanpa_pinjam = [j for j in semua_judul if j not in self.riwayat_peminjaman]

        if not judul_tanpa_pinjam:
            messagebox.showinfo("Info", "Tidak ada buku lain yang bisa direkomendasikan.")
            return

        # Hitung similarity
        all_docs = judul_tanpa_pinjam + [input_user]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_docs)
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

        # Gabungkan data dan similarity
        kandidat_buku = [b for b in buku_list if b["judul"] not in self.riwayat_peminjaman]
        hasil = sorted(zip(kandidat_buku, similarity_scores), key=lambda x: x[1], reverse=True)

        # Tampilkan hasil
        for item in self.tree.get_children():
            self.tree.delete(item)

        for buku, skor in hasil:    
            if skor > 0:
                self.tree.insert("", tk.END, values=(
                    buku["kode"], buku["judul"], buku["penulis"], buku["tahun"], f"{skor:.2f}"
                ))

# Jalankan program
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemRekomendasi(root)
    root.mainloop()
