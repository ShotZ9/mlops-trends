# MLOps Trends24 Indonesia Scraper

Scraper otomatis yang mengambil data tren Twitter dari [trends24.in/indonesia](https://trends24.in/indonesia/)
dan menyimpannya ke file `data/trends.json`.  
Pipeline ini berjalan otomatis tiap jam melalui **GitHub Actions** dan juga dapat dijalankan melalui **Docker**.

---

## 🚀 Cara Menjalankan Secara Lokal

```bash
git clone https://github.com/<username>/mlops-trends.git
cd mlops-trends
docker-compose up --build
````

Output akan tersimpan di:

```
data/trends.json
```

---

## 🧰 Tools yang Digunakan

* **Python 3.10**
* **BeautifulSoup4** untuk scraping
* **Requests**
* **GitHub Actions** untuk automation
* **Docker** & **Docker Compose**

---

## ⚙️ GitHub Actions

Workflow otomatis akan:

1. Menjalankan scraper tiap 1 jam (`cron: 0 * * * *`)
2. Menyimpan hasil ke `data/trends.json`
3. Commit dan push hasil terbaru ke repo
4. (Opsional) Build image Docker ke GHCR

---

## 📈 Contoh Output

```json
{
  "meta": {
    "source": "https://trends24.in/indonesia/",
    "scraped_at": "2025-10-28T08:00:00Z",
    "count": 20
  },
  "trends": [
    {"timestamp": "1 hour ago", "rank": 1, "text": "#Halloween", "link": "https://twitter.com/hashtag/Halloween"},
    {"timestamp": "1 hour ago", "rank": 2, "text": "#Bali", "link": "https://twitter.com/hashtag/Bali"}
  ]
}
```

---

## 👨‍💻 Author

**Yoel Amadeo Pratomo**
*MLOps Final Project — Data Collection Automation*

```

---

## ✅ Next Steps
Kamu bisa langsung:
1. Buat repo GitHub, misal `yoelamadeo/mlops-trends`
2. Upload semua file di atas
3. Aktifkan **Actions → Enable workflows**
4. Tunggu 1 jam (atau klik “Run Workflow”)

---

Mau saya buatin juga **versi ZIP project siap upload ke GitHub** (termasuk folder + file lengkap)?  
Kalau iya, nanti saya generate otomatis biar kamu tinggal `git push` aja.
```
