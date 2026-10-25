# Situs pribadi Wahyu Pebrianto

Situs Jekyll dwibahasa (EN di `/`, ID di `/id/`) tanpa tema pihak ketiga, tanpa
JavaScript framework, tanpa permintaan ke layanan luar (font dan ikon dilayani
sendiri). Repo **private** ini berisi sumber lengkap; GitHub Actions membangun
situs lalu hanya menerbitkan hasil HTML-nya ke repo **public**
`wahyupebrianto/wahyupebrianto.github.io`.

## 1. Menjalankan di komputer sendiri

Butuh Ruby 3.3 (di Windows: RubyInstaller dengan DevKit) dan Bundler.

```bash
bundle install                          # sekali saja, lalu commit Gemfile.lock
bundle exec jekyll serve --livereload   # buka http://localhost:4000
bundle exec jekyll serve --drafts       # ikut menampilkan tulisan di _drafts/
bash scripts/check.sh                   # build produksi + cek link (seperti CI)
```

Pertama kali `bundle install` selesai, jalankan juga
`bundle lock --add-platform x86_64-linux` agar `Gemfile.lock` cocok dengan
server GitHub Actions, lalu commit file itu.

## 2. Struktur

| Lokasi | Isi |
|---|---|
| `_data/profile.yml` | Nama, peran, bio EN/ID, kata kunci, tautan sosial, CV |
| `_data/navigation.yml` | Menu dan saklar `enabled` per halaman |
| `_data/publications.yml` | Daftar publikasi |
| `_data/courses.yml` | Mata kuliah (deskripsi, silabus, materi) EN/ID |
| `_data/research.yml` | Tema riset dan saklar `ready` |
| `_data/members.yml`, `links.yml` | Anggota dan tautan (kosong = "coming soon") |
| `_data/i18n.yml` | Semua teks antarmuka EN/ID |
| `_posts/` | Tulisan blog |
| `index.md`, `id/index.md`, dst. | Halaman; file di `id/` adalah versi Indonesia |
| `_layouts/`, `_includes/` | Template |
| `assets/css/main.css`, `assets/js/` | Gaya dan skrip |
| `figures-src/` | Sumber gambar TikZ (`.tex`, label bahasa Inggris) |
| `_includes/figures/` | SVG hasil kompilasi, dipasang inline di tulisan |
| `_archive/` | Gambar lama yang tidak dipakai (tidak diterbitkan) |

## 3. Pekerjaan sehari-hari

**Tulisan baru.** Buat `_posts/2026-11-02-judul-singkat.md`:

```yaml
---
title: "Judul tulisan"
date: 2026-11-02 09:00:00 +0700
lang: id                      # id atau en
ref: judul-singkat            # sama untuk terjemahannya
permalink: /id/blog/judul-singkat/   # EN: /blog/judul-singkat/
categories: [Deep Learning]   # dipakai tombol filter di halaman blog
tags: [fastai, deployment]
description: "Ringkasan satu-dua kalimat untuk daftar blog dan hasil pencarian."
---
Isi tulisan. Gambar: ![alt]({{ '/assets/images/blog/nama.png' | relative_url }})
```

Tulisan yang belum selesai taruh di `_drafts/` (tanpa tanggal di nama file).
Jika sebuah tulisan punya terjemahan, beri `ref` yang sama; tombol bahasa dan
tag `hreflang` otomatis menghubungkannya. Tulisan tanpa terjemahan tampil di
kedua daftar blog dengan label bahasa.

**Gambar dan kotak sitasi di tulisan.** Gambar teknis dibuat dari TikZ di
`figures-src/` dengan label bahasa Inggris (istilah global), sehingga satu gambar
dipakai di tulisan EN maupun ID. Ubah `.tex`, lalu jalankan
`python3 scripts/build_figures.py` (butuh `pdflatex` dan `pdftocairo`). Hasilnya
SVG inline yang mengikuti mode terang/gelap. Pasang di tulisan dengan:

```html
<figure class="figure" markdown="0">
{% include figures/fig2-agent-loop.svg label="fig2-cap" %}
<figcaption id="fig2-cap"><strong>Gambar 2.</strong> Keterangan gambar.</figcaption>
</figure>
```

Tambahkan `cite: true` di front matter agar muncul kotak "Cara mengutip tulisan
ini" (IEEE dan BibTeX, dibuat otomatis dari judul, tanggal, dan URL tulisan,
lengkap dengan tombol salin). Referensi di akhir tulisan memakai format IEEE:
sitasi dalam teks `[[1]](#ref-1)`, daftar `<a id="ref-1"></a>` lalu `**[1]** ...`.

**Publikasi baru.** Tambahkan satu blok di `_data/publications.yml`. Urutan dan
pengelompokan otomatis; nama Anda otomatis ditebalkan.

**Mata kuliah baru.** Tambahkan blok di `_data/courses.yml`, lalu salin
`teaching/devops.md` dan `id/teaching/devops.md`; ganti `course:` dan
`permalink:`.

**Mengaktifkan halaman tersembunyi** (Members, Links, tema riset):
isi datanya, lalu ubah `enabled: true` di `navigation.yml` (Members, Links)
atau `ready: true` di `research.yml` (tema riset). Satu saklar itu juga
mengatur menu, `noindex`, dan sitemap.

**Tautan sosial / CV.** Isi `social.scholar`, `social.youtube`, dst. di
`profile.yml`; ikon muncul otomatis saat tidak kosong. Untuk CV, taruh PDF di
`assets/files/` lalu isi `cv:`.

**Gambar.** Kecilkan sebelum commit: `python3 scripts/optimize_images.py file.png`.
Pakai nama file tanpa spasi dan selalu isi teks alt.

## 4. Deploy: repo private -> repo public

Pola dua repo ini umum dipakai (sumber/draf privat, hasil build publik) dan
tetap dipertahankan; yang berubah hanyalah penyalinan manual diganti workflow
otomatis (`.github/workflows/deploy.yml`).

Setup satu kali:

1. Buat pasangan kunci: `ssh-keygen -t ed25519 -f deploy_key -N "" -C "mysite-deploy"`
2. Repo **public** -> Settings -> Deploy keys -> Add: tempel isi `deploy_key.pub`,
   centang *Allow write access*.
3. Repo **private** (ini) -> Settings -> Secrets and variables -> Actions ->
   *New repository secret* bernama `PUBLIC_REPO_DEPLOY_KEY`, isi dengan isi file
   `deploy_key` (kunci privat). Hapus kedua file kunci dari komputer.
4. Jika branch repo public bukan `main`, buat *Variable* `PUBLIC_REPO_BRANCH`
   (misalnya `master`).
5. Repo public -> Settings -> Pages -> Source: *Deploy from a branch*, pilih branch
   di atas, folder `/ (root)`.
6. Push ke branch `main`/`master` repo private. Tab Actions menampilkan build,
   cek link, lalu publikasi. Pull request hanya menjalankan build + cek.

Catatan penting:

- Workflow membuat **satu commit baru** di repo public setiap deploy
  (`force_orphan`), jadi isi lama repo public akan tergantikan seluruhnya. Pastikan
  tidak ada file lain di sana yang ingin dipertahankan.
- Privasi di sini berarti sumber, draf, dan riwayat tidak terlihat. Semua yang
  terbit ke situs tetap publik, termasuk halaman `noindex` (itu hanya meminta mesin
  pencari tidak mengindeks, bukan menyembunyikan).
- Jangan pernah commit kunci API atau kata sandi, walau repo private. Jika pernah
  terlanjur, putar (rotate) kuncinya.

## 5. Perawatan jangka panjang

- Dependabot membuka pull request mingguan untuk gem dan versi GitHub Actions;
  merge setelah CI hijau.
- Jangan ubah `permalink` tulisan yang sudah terbit; jika harus, tambahkan lama di
  `redirect_from:`.
- URL lama (`/ai/2022/11/15/Popular-Dataset.html`, `/dl/2024/05/15/...`,
  `/courses/`, `/wahyulab/`) sudah dialihkan lewat `redirect_from`. Tautan
  Hugging Face Space lama tetap bekerja.
- Sekali setahun: naikkan `.ruby-version`, jalankan `bundle update`, dan
  `bash scripts/check.sh`.
- Mau menambah bahasa ketiga: tambah blok di `_data/i18n.yml`, folder bahasa baru,
  dan sesuaikan `i18n.html` serta `alternates.html`.

## 6. Pemecahan masalah

- `jekyll serve` gagal di Ruby 3: pastikan gem `webrick` terpasang (sudah di Gemfile).
- Gambar tidak muncul di tulisan: gunakan `{{ '/assets/...' | relative_url }}`.
- Build CI gagal di `htmlproofer`: baca pesan; biasanya tautan internal/gambar salah ketik.
- Halaman baru tidak ada di menu: tambahkan ke `_data/navigation.yml` dan beri
  `nav_id:` yang sama di front matter halamannya.
