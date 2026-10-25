---
title: "LLM, Reasoning Model, AI Agent, dan Agent Harness: Empat Konsep Sistem AI Modern"
date: 2026-10-24 20:49:00 +0700
lang: id
ref: llm-agent-harness
permalink: /id/blog/llm-reasoning-agent-harness/
categories: [Generative AI]
tags: [llm, reasoning-model, ai-agent, agent-harness]
description: "Peta ringkas empat konsep sistem AI modern (LLM, reasoning model, AI agent, dan agent harness): peran, cara kerja, dan rujukannya."
cite: true
---

Model bahasa besar (*large language model*, LLM) mampu mengikuti instruksi dan menghasilkan teks yang koheren. Namun, tugas nyata seperti memperbaiki *bug* atau mengerjakan proyek perangkat lunak lintas sesi membutuhkan lebih dari itu. Tulisan ini merangkum empat konsep yang sering muncul pada sistem AI modern: **LLM**, **reasoning model**, **AI agent**, dan **agent harness**.

> Keempatnya bukan empat lapisan yang setara atau tahapan wajib. *Reasoning model* merupakan jenis LLM; *agent* menggunakan model dan *tools*; sedangkan *harness* mengelola komponen pendukungnya. Batas antaristilah dapat tumpang tindih, dan penggunaan istilah *agent harness* saat artikel ini ditulis masih berkembang.

## 1. LLM dan Reasoning Model

LLM generatif menghasilkan respons dengan memprediksi token berikutnya berdasarkan konteks. *Reasoning model* dioptimalkan untuk tugas yang menuntut penalaran bertahap. Kemampuannya dapat didukung oleh *reinforcement learning* (RL) saat pelatihan dan komputasi tambahan saat inferensi (*test-time compute*). Mengingat penalaran bertahap, proses penalaran internalnya tidak selalu ditampilkan kepada pengguna. Berikut adalah beberapa point temuan yang telah dilaporkan:

- OpenAI melaporkan bahwa kinerja o1 meningkat seiring lebih banyak RL saat pelatihan dan lebih banyak waktu berpikir saat inferensi [[1]](#ref-1).
- Snell dkk. menunjukkan bahwa komputasi inferensi dapat dialokasikan secara adaptif. Pada kondisi komputasi setara (*FLOPs-matched*) dan masalah yang tingkat keberhasilan model kecilnya tidak terlalu rendah, model kecil dengan tambahan komputasi inferensi dapat mengungguli model 14 kali lebih besar [[2]](#ref-2).
- DeepSeek-R1-Zero dilatih dengan RL berskala besar tanpa *supervised fine-tuning* (SFT) awal, sedangkan DeepSeek-R1 menambahkan pelatihan multitahap dan data *cold-start*. Penulisnya melaporkan kinerja R1 sebanding dengan OpenAI-o1-1217 pada tugas penalaran yang mereka evaluasi, bukan keunggulan universal [[3]](#ref-3).

<figure class="figure" markdown="0">
{% include figures/fig1-llm-vs-reasoning.svg label="fig1-cap" %}
<figcaption id="fig1-cap"><strong>Gambar 1.</strong> Perbandingan konseptual: (a) LLM umum menjawab langsung; (b) reasoning model dapat menalar dan memakai komputasi inferensi tambahan sebelum menjawab.</figcaption>
</figure>

Penalaran yang kuat belum memberi model akses ke dunia luar. Untuk membaca repositori, menjalankan tes, atau membuka situs web, model memerlukan *tools* dan lingkungan eksekusi.

## 2. AI Agent

Anthropic membedakan *workflow*, yaitu LLM dan *tools* yang diorkestrasi lewat alur yang sudah ditentukan, dari *agent*, yaitu sistem yang LLM-nya mengarahkan sendiri proses dan penggunaan *tools*-nya, dengan memperoleh "ground truth" dari lingkungan pada setiap langkah [[4]](#ref-4). Siklus sederhananya adalah **Reason → Act → Observe**: menalar, bertindak, mengamati, lalu mengulang sampai tugas selesai atau batas percobaan tercapai.

<figure class="figure" markdown="0">
{% include figures/fig2-agent-loop.svg label="fig2-cap" %}
<figcaption id="fig2-cap"><strong>Gambar 2.</strong> Siklus Reason → Act → Observe: hasil tindakan (<em>observation</em>) menjadi masukan bagi langkah penalaran berikutnya.</figcaption>
</figure>

Dalam *debugging*, misalnya, agent membaca *codebase*, menjalankan tes, memeriksa log *error*, mengusulkan perbaikan, lalu menguji ulang. Pola ini berkaitan dengan **ReAct**, yang menyisipkan jejak penalaran dan tindakan secara bergantian sehingga hasil dari lingkungan memengaruhi langkah berikutnya [[5]](#ref-5). 
> Catatan: Tidak semua implementasi agent mengikuti ReAct secara persis.

## 3. Agent Harness

Tugas panjang menimbulkan masalah tambahan. *Context window* terbatas, sesi baru tidak otomatis mewarisi informasi dari sesi sebelumnya, dan hasil kerja perlu diperiksa, bukan sekadar dinyatakan selesai oleh agent.

*Agent harness* adalah perangkat lunak pendukung yang mengatur interaksi agent dengan *tools* dan lingkungan, termasuk pengelolaan konteks, *state*, izin, dan verifikasi. Anthropic menyebut Claude Agent SDK sebagai *general-purpose agent harness* dan menegaskan bahwa *compaction* saja tidak cukup untuk menangani tugas panjang [[6]](#ref-6). Untuk keperluan tulisan ini, peran harness dirangkum dalam tiga area:

- **Konteks dan *state*:** membantu agent mengetahui apa yang sudah dikerjakan, misalnya lewat berkas progres, daftar fitur, dan riwayat Git.
- ***Guardrails*:** membatasi izin dan tindakan, serta menentukan aturan pemulihan atau *retry* saat terjadi kegagalan.
- **Verifikasi:** memeriksa hasil, misalnya dengan menjalankan tes, sebelum pekerjaan dianggap selesai.

<figure class="figure" markdown="0">
{% include figures/fig3-agent-harness.svg label="fig3-cap" %}
<figcaption id="fig3-cap"><strong>Gambar 3.</strong> Secara konseptual, harness mengelola model, tools, konteks dan state, guardrails, serta verifikasi hasil.</figcaption>
</figure>

### Contoh 1: dua peran agent dari Anthropic

Anthropic mengidentifikasi dua pola kegagalan pada *coding agent* yang bekerja melintasi banyak *context window*, meski menggunakan *compaction*. Pertama, agent mengambil terlalu banyak pekerjaan hingga konteks habis sebelum implementasi selesai. Kedua, agent pada sesi berikutnya melihat progres yang sudah ada lalu keliru menyimpulkan bahwa proyek telah selesai [[6]](#ref-6). 

> Catatan: Temuan ini berasal dari eksperimen tim mereka, bukan berarti semua agent selalu gagal dengan cara yang sama.

Solusinya membagi pekerjaan menjadi dua peran:

1. **Initializer agent** (sesi pertama) menyiapkan lingkungan: skrip `init.sh`, berkas `claude-progress.txt`, daftar fitur terstruktur dalam berkas JSON yang awalnya berstatus *failing*, serta *initial Git commit*.
2. **Coding agent** (sesi berikutnya) mengerjakan satu fitur per sesi, mengujinya (termasuk secara *end-to-end*), lalu membuat *commit* dan menulis catatan progres untuk sesi selanjutnya.

<figure class="figure" markdown="0">
{% include figures/fig4-two-agent-pattern.svg label="fig4-cap" %}
<figcaption id="fig4-cap"><strong>Gambar 4.</strong> Artefak di disk menjembatani sesi baru yang tidak otomatis membawa seluruh konteks sebelumnya.</figcaption>
</figure>

Kedua peran hanya dibedakan berdasarkan *prompt* awal, sedangkan *system prompt*, *tools*, dan harness yang digunakan tetap sama [[6]](#ref-6). Karena itu, pola ini lebih tepat dipahami sebagai pembagian tugas antarsesi, bukan bukti bahwa sistem harus menggunakan beberapa agent. Anthropic juga mencatat bahwa efektivitas satu agent serbaguna dibandingkan beberapa agent khusus, misalnya untuk *quality assurance*, masih menjadi pertanyaan terbuka [[6]](#ref-6).

### Contoh 2: pengalaman OpenAI dengan Codex

OpenAI melaporkan membangun produk beta internal dengan "0 lines of manually-written code": seluruh kodenya ditulis agent Codex [[7]](#ref-7). Kemajuan awal lebih lambat dari perkiraan karena lingkungan belum terdefinisi cukup; agent belum memiliki *tools*, abstraksi, dan struktur internal yang dibutuhkan. Pelajaran utamanya adalah merancang lingkungan, memperjelas maksud, dan membangun *feedback loop*. Penulisnya juga mengingatkan bahwa hasil itu bergantung pada *tooling* repositori mereka dan belum tentu berlaku tanpa investasi serupa [[7]](#ref-7).

Kedua contoh di atas adalah laporan pengalaman perusahaan, bukan studi komparatif independen. Meski demikian, keduanya sejalan: keberhasilan agent tidak hanya ditentukan kemampuan model, tetapi juga pada lingkungan eksekusi, pengelolaan konteks, pembatasan tindakan, dan verifikasi hasil.

## 4. Ringkasan

- LLM berperan sebagai fondasi model bahasa untuk memahami konteks dan menghasilkan teks.
- Reasoning model sebagai LLM yang dioptimalkan untuk penalaran bertahap, terkadang dengan komputasi inferensi tambahan.
- AI agent sebagai model dan *tools* dalam siklus tindakan serta umpan balik dari lingkungan.
- Agent harness sebagai perangkat lunak yang mengatur konteks, *state*, izin, dan verifikasi agar agent lebih andal pada tugas panjang.

Kualitas model penting, tetapi lingkungan eksekusi, pengelolaan konteks, batas tindakan, dan verifikasi hasil juga menentukan keandalan sistem.

## Referensi

<a id="ref-1"></a>
**[1]** OpenAI, "Learning to reason with LLMs," OpenAI, Sep. 12, 2024.
[Online]. Available: [https://openai.com/index/learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)

<a id="ref-2"></a>
**[2]** C. Snell, J. Lee, K. Xu, and A. Kumar, "Scaling LLM test-time compute optimally can be more effective than scaling model parameters," arXiv:2408.03314, Aug. 2024.
[Online]. Available: [https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)

<a id="ref-3"></a>
**[3]** DeepSeek-AI *et al.*, "DeepSeek-R1: Incentivizing reasoning capability in LLMs via reinforcement learning," arXiv:2501.12948, Jan. 2025. Versi jurnal: *Nature*, vol. 645, pp. 633–638, 2025, doi: 10.1038/s41586-025-09422-z.
[Online]. Available: [https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)

<a id="ref-4"></a>
**[4]** E. Schluntz and B. Zhang, "Building effective agents," Anthropic, Dec. 19, 2024.
[Online]. Available: [https://www.anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)

<a id="ref-5"></a>
**[5]** S. Yao *et al.*, "ReAct: Synergizing reasoning and acting in language models," in *Proc. Int. Conf. Learn. Represent. (ICLR)*, 2023, arXiv:2210.03629.
[Online]. Available: [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

<a id="ref-6"></a>
**[6]** J. Young, "Effective harnesses for long-running agents," Anthropic, Nov. 26, 2025.
[Online]. Available: [https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

<a id="ref-7"></a>
**[7]** R. Lopopolo, "Harness engineering: Leveraging Codex in an agent-first world," OpenAI, Feb. 11, 2026.
[Online]. Available: [https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)
