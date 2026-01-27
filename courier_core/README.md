# Courier Core - Sistem Log Insiden

Modul Odoo 18 untuk mencatat dan mengelola insiden pengiriman pada layanan kurir BeraniExpress.

## Fitur

- **Pencatatan Insiden**: Catat insiden dengan tingkat urgensi (low, medium, high)
- **Alur Kerja Status**: Draft → Follow-up → Done
- **Validasi Otomatis**: Catatan tindak lanjut wajib diisi sebelum menyelesaikan insiden
- **Constraint Unik**: Mencegah duplikasi insiden (kombinasi pelanggan, tipe, dan waktu yang sama)
- **Dekorasi Visual**: Warna baris berbeda berdasarkan status

---

## Instalasi

1. Salin folder `courier_core` ke direktori addons Odoo
2. Restart Odoo server
3. Buka menu **Apps** → **Update Apps List**
4. Cari "Courier Core" dan klik **Install**

---

## Struktur Modul

```
courier_core/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── courier_incident.py
├── views/
│   └── courier_incident_views.xml
├── security/
│   └── ir.model.access.csv
└── data/
    └── demo_data.xml
```

---

## Pengujian Manual (Quick Start)

### Langkah 1: Buat Insiden Baru
1. Buka menu **Log Insiden**
2. Klik tombol **Create**
3. Isi field yang diperlukan:
   - Name
   - Jamaah (pilih pelanggan)
   - Incident Type
   - Severity
4. Klik **Save**

### Langkah 2: Mark Follow-up
1. Buka insiden yang baru dibuat (status: Draft)
2. Klik tombol **"Mark Follow-up"**
3. Verifikasi: Status berubah menjadi "Follow-up"

### Langkah 3: Resolve
1. Isi field **"Follow up note"** dengan catatan tindakan
2. Klik tombol **"Resolve"**
3. Verifikasi:
   - Status berubah menjadi "Done"
   - Field "Resolve at" terisi otomatis dengan waktu sekarang

---

## Spesifikasi Teknis

### Model: `courier.incident`

| Field | Tipe | Keterangan |
|-------|------|------------|
| name | Char | Judul insiden (required) |
| customer_id | Many2one | Relasi ke courier.customer (required) |
| shipment_id | Many2one | Relasi ke courier.shipment |
| incident_type | Selection | health, lost_item, delay, other |
| incident_datetime | Datetime | Waktu kejadian (required) |
| severity | Selection | low, medium, high |
| description | Text | Detail kronologi |
| followup_note | Text | Catatan tindakan |
| state | Selection | draft, followup, done |
| resolved_at | Datetime | Otomatis terisi saat Done |

### Tombol Aksi

| Tombol | Fungsi |
|--------|--------|
| **Mark Follow-up** | Mengubah status dari Draft ke Follow-up |
| **Resolve** | Mengubah status ke Done dan mengisi resolved_at |

### Constraints

- **SQL**: Kombinasi unik (customer_id, incident_type, incident_datetime)
- **Python**: followup_note wajib diisi sebelum status Done

---

## Lisensi

LGPL-3
