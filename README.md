# 🌴 VisionPalm
**Sistem Deteksi Kematangan Tandan Buah Segar (TBS) Kelapa Sawit**

Aplikasi Computer Vision berbasis Streamlit untuk mengklasifikasikan kematangan TBS kelapa sawit ke dalam 5 kelas (F0–F4) menggunakan pipeline multi-algoritma.

---

## ⚡ Cara Menjalankan

```bash
pip install -r requirements.txt
pip install opencv-python numpy streamlit pillow matplotlib scikit-image
streamlit run app.py
```

---

## 🔬 Pipeline Algoritma (6 Tahap)

| Tahap | Algoritma | Fungsi |
|-------|-----------|--------|
| 01 | Spatial Sampling + K-Means Color Quantization | Normalisasi resolusi 512×512, reduksi warna K=8 |
| 02 | Gaussian Blur + HSV & Lab* Conversion | Noise reduction, transformasi ruang warna |
| 03 | HSV Segmentation + Morphological Filtering | Isolasi area buah per kelas warna, bersihkan mask |
| 04 | Canny Edge + Contour Bounding Box | Deteksi tepi, kunci ROI objek sawit |
| 05 | GLCM Texture Feature Extraction | 6 fitur Haralick dari matriks ko-okkurensi |
| 06 | Rule Fusion Classifier | Gabungan skor warna + Lab* + tekstur → kelas + confidence |

---

## 🌿 Kelas Kematangan

| Kode | Label | Ciri Visual | Rekomendasi |
|------|-------|-------------|-------------|
| F0 | Mentah | Dominan hijau | Tunda panen 2–3 minggu |
| F1 | Kurang Matang | Kuning + pucuk gelap | Tunda panen 1–2 minggu |
| F2 | Cukup Matang | Oranye bercampur merah | Panen dalam 3–5 hari |
| F3 | Matang Ideal | Merah cerah dominan | Panen segera |
| F4 | Terlalu Matang | Maroon gelap, buah rontok | Panen darurat |

---

## 📁 Struktur Direktori

```
visionpalm/
├── app.py
├── requirements.txt
├── README.md
└── dataset/          ← opsional: gambar referensi per kelas
    ├── dataset_f0.jpeg
    ├── dataset_f1.jpeg
    ├── dataset_f2.jpeg
    ├── dataset_f3.jpeg
    └── dataset_f4.jpeg
```

Dataset referensi bersifat opsional. Jika folder `dataset/` ada dan berisi gambar,
aplikasi akan menampilkan panel referensi kelas di bagian atas.

---

## 📖 Mata Kuliah
Tugas Visi Komputer — Deteksi Kematangan TBS Kelapa Sawit
