Berikut adalah **tahapan lengkap setup project Python** menggunakan **virtual environment (venv)** dan menginstall package dari `requirements.txt`:

---

# **Tahapan Setup Project Python**

## **1. Clone atau siapkan project**

```bash
git clone https://github.com/rezaawp/rest-openai-api.git
cd rest-openai-api
```

Atau jika project sudah ada di folder lokal, pindah ke folder project.

---

## **2. Buat Virtual Environment (venv)**

Virtual environment digunakan agar **dependency project tidak tercampur dengan package global Python**.

```bash
python3 -m venv venv
```

* `venv` → nama folder virtual environment (bisa diganti)
* Folder `venv` akan berisi Python interpreter lokal untuk project

---

## **3. Aktifkan Virtual Environment**

### **Linux / macOS / WSL**

```bash
source venv/bin/activate
```

### **Windows (CMD)**

```cmd
venv\Scripts\activate
```

### **Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

> Setelah aktif, prompt terminal biasanya berubah, menunjukkan bahwa venv aktif.

---

## **4. Upgrade pip (opsional tapi direkomendasikan)**

```bash
pip install --upgrade pip
```

Agar package terbaru dapat terinstall tanpa error.

---

## **5. Install dependency dari requirements.txt**

```bash
pip install -r requirements.txt
```

* `requirements.txt` berisi semua package dan versinya
* Contoh isi `requirements.txt`:

  ```
  Flask==3.2.0
  flask-restx==1.3.0
  SQLAlchemy==2.0.28
  ```

---

## **6. Jalankan aplikasi**

Pastikan venv masih aktif:

```bash
python app.py
```

Aplikasi biasanya akan berjalan di:

```
http://localhost:5000
```

Docs API:
```
http://localhost:5000/api/docs
```

Pastikan ngrok sudah terinstall dan jalankan:
```
ngrok http 500
```
Lalu setting webook di: https://platform.openai.com/settings/project/webhooks

Add webhook di OpenAI untuk event `video.completed` dan set url: `{ngrok_base_url}/callback/ai/video/success-callback`

---

## **7. Update requirements.txt (jika menambahkan package baru)**

```bash
pip freeze > requirements.txt
```

* `pip freeze` → mencetak semua package beserta versinya
* File `requirements.txt` bisa digunakan untuk environment lain

---

## **8. Nonaktifkan Virtual Environment**

Jika sudah selesai bekerja:

```bash
deactivate
```

> Prompt terminal kembali normal, dan package global Python dapat digunakan lagi.

---

## **9. Tips tambahan**

* Selalu aktifkan venv sebelum menjalankan project atau install package.
* Jangan commit folder `venv` ke Git, tambahkan ke `.gitignore`:

  ```
  venv/
  ```
* Gunakan `python -m venv` daripada `virtualenv` jika Python 3 sudah tersedia.

---
