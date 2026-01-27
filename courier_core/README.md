# Courier Core - Sistem Log Insiden

Modul Odoo 18 untuk mencatat dan mengelola insiden pengiriman pada layanan kurir BeraniExpress.

## Daftar Isi

- [Fitur](#fitur)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi](#instalasi)
- [Struktur Modul](#struktur-modul)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Spesifikasi Teknis](#spesifikasi-teknis)
- [Pengujian Manual](#pengujian-manual)
- [Lisensi](#lisensi)

---

## Fitur

- **Pencatatan Insiden**: Catat insiden dengan tingkat urgensi (low, medium, high)
- **Alur Kerja Status**: Draft → Follow-up → Done
- **Validasi Otomatis**: Catatan tindak lanjut wajib diisi sebelum menyelesaikan insiden
- **Constraint Unik**: Mencegah duplikasi insiden (kombinasi pelanggan, tipe, dan waktu yang sama)
- **Dekorasi Visual**: Warna baris berbeda berdasarkan status (kuning untuk follow-up, hijau untuk done)

---

## Persyaratan Sistem

| Komponen | Versi |
|----------|-------|
| Odoo | 18.0 |
| Python | 3.10 atau 3.11 |
| PostgreSQL | 14+ |

---

## Instalasi

1. **Salin modul** ke direktori addons Odoo Anda:
   ```bash
   cp -r courier_core /path/to/odoo/addons/
   ```

2. **Perbarui daftar aplikasi** di Odoo:
   - Buka menu **Apps**
   - Klik **Update Apps List**

3. **Cari dan instal modul**:
   - Ketik "Courier Core" di pencarian
   - Klik **Install**

---

## Struktur Modul

```
courier_core/
├── __init__.py              # Inisialisasi modul
├── __manifest__.py          # Metadata modul
├── README.md                # Dokumentasi
├── data/
│   └── demo_data.xml        # Data contoh (pelanggan & pengiriman)
├── models/
│   ├── __init__.py          # Inisialisasi model
│   ├── courier_customer.py  # Model pelanggan
│   ├── courier_shipment.py  # Model pengiriman
│   └── courier_incident.py  # Model insiden (utama)
├── views/
│   └── courier_incident_views.xml  # Tampilan dan menu
└── security/
    └── ir.model.access.csv  # Hak akses pengguna
```

---

## Panduan Penggunaan

### Mengakses Menu
1. Login ke Odoo
2. Klik menu **BeraniExpress Courier**
3. Pilih **Log Insiden**

### Membuat Insiden Baru
1. Klik tombol **Create**
2. Isi field yang diperlukan:
   - **Name**: Judul insiden
   - **Jamaah**: Pilih pelanggan
   - **Quotation**: Pilih nomor resi (opsional)
   - **Incident Type**: Pilih tipe insiden
   - **Severity**: Pilih tingkat urgensi
   - **Incident Datetime**: Waktu kejadian
   - **Description**: Detail kronologi kejadian
3. Klik **Save**

### Alur Kerja (Workflow)

```
┌─────────┐    Mark Follow-up    ┌───────────┐    Resolve    ┌────────┐
│  Draft  │ ──────────────────→  │ Follow-up │ ────────────→ │  Done  │
└─────────┘                      └───────────┘               └────────┘
                                       │
                                       ▼
                              Wajib isi "Follow up note"
                              sebelum klik "Resolve"
```

1. **Draft**: Status awal saat insiden dibuat
2. **Follow-up**: Klik tombol "Mark Follow-up" untuk menandai sedang ditindaklanjuti
3. **Done**: Isi catatan tindakan, lalu klik "Resolve" untuk menyelesaikan

---

## Spesifikasi Teknis

### Model: `courier.incident`

| Field | Label | Tipe | Keterangan |
|-------|-------|------|------------|
| `name` | Judul Insiden | Char | Wajib diisi |
| `customer_id` | Jamaah/Pelanggan | Many2one | Relasi ke courier.customer (wajib) |
| `shipment_id` | Quotation/No. Resi | Many2one | Relasi ke courier.shipment |
| `incident_type` | Tipe Insiden | Selection | health, lost_item, delay, other |
| `incident_datetime` | Waktu Kejadian | Datetime | Wajib, default: waktu sekarang |
| `severity` | Urgensi | Selection | low, medium, high |
| `description` | Kronologi | Text | Detail kejadian |
| `followup_note` | Catatan Tindakan | Text | Tindakan yang diambil |
| `state` | Status | Selection | draft, followup, done |
| `resolved_at` | Selesai Pada | Datetime | Otomatis terisi saat status Done |

### Metode Bisnis

| Metode | Fungsi |
|--------|--------|
| `action_mark_followup()` | Mengubah status dari Draft ke Follow-up |
| `action_resolve()` | Mengubah status ke Done dan mengisi `resolved_at` |

### Constraints

| Tipe | Deskripsi |
|------|-----------|
| SQL Constraint | Kombinasi unik: customer_id + incident_type + incident_datetime |
| Python Constraint | Field `followup_note` wajib diisi sebelum status Done |

### Dekorasi Tree View

| Status | Warna |
|--------|-------|
| Draft | Default |
| Follow-up | Kuning (warning) |
| Done | Hijau (success) |

---

## Pengujian Manual

### Langkah Pengujian

#### 1. Buat Insiden Baru
```
Menu: BeraniExpress Courier → Log Insiden → Create
```
- Isi Name: "Test Insiden"
- Pilih Jamaah: "Ahmad F"
- Pilih Quotation: "QTN-00123"
- Pilih Incident Type: "delay"
- Pilih Severity: "medium"
- Klik Save

#### 2. Mark Follow-up
- Buka insiden yang baru dibuat
- Klik tombol **"Mark Follow-up"**
- Verifikasi: Status berubah menjadi "Follow-up"
- Verifikasi: Baris di list view berwarna kuning

#### 3. Resolve Insiden
- Isi field **"Follow up note"**: "Sudah ditangani"
- Klik tombol **"Resolve"**
- Verifikasi: Status berubah menjadi "Done"
- Verifikasi: Field "Resolve at" terisi otomatis
- Verifikasi: Baris di list view berwarna hijau

#### 4. Test Validasi
- Buat insiden baru, Mark Follow-up
- **Jangan isi** Follow up note
- Klik Resolve
- Verifikasi: Muncul error "Catatan (followup_note) wajib diisi sebelum menyelesaikan insiden!"

#### 5. Test Constraint Unik
- Buat insiden dengan data yang sama (customer, type, datetime)
- Verifikasi: Muncul error database constraint

---

## Data Demo

Modul ini menyertakan data contoh untuk pengujian:

### Pelanggan
| Nama |
|------|
| Ahmad F |
| Siti N |
| Yusuf R |

### Pengiriman (Quotation)
| No. Resi | Pelanggan |
|----------|-----------|
| QTN-00123 | Ahmad F |
| QTN-00456 | Siti N |
| QTN-00303 | Yusuf R |

---

## Teknologi

- **Platform**: Odoo 18.0
- **Bahasa**: Python 3.11, XML
- **Database**: PostgreSQL
- **Framework**: Odoo ORM

---

## Referensi Dokumentasi

- [Odoo 18 Developer Documentation](https://www.odoo.com/documentation/18.0/developer.html)
- [Odoo ORM API](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## Lisensi

LGPL-3 (GNU Lesser General Public License v3.0)

---

## Penulis

Dikembangkan untuk Technical Test PT Berani Digital Indonesia.

---

*Dokumentasi ini dibuat mengikuti standar Odoo 18 dan best practices pengembangan modul.*
