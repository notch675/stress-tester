import asyncio
import aiohttp
import time
import random
import json
from threading import Thread
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk
from tkinter import filedialog
import platform

try:
    import darkdetect
    tema_inicial = "darkly" if darkdetect.isDark() else "flatly"
except ImportError:
    tema_inicial = "cyborg"

class StressTester:
    def __init__(self, master):
        self.master = master
        master.title("\U0001F680 Estresse HTTP")

        self.frame = ttk.Frame(master, padding=15)
        self.frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.frame, text="\U0001F310 URL alvo:").grid(row=0, column=0, sticky="w")
        self.url_entry = ttk.Entry(self.frame, width=50)
        self.url_entry.insert(0, "https://seudominio.com")
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="\U0001F501 Método:").grid(row=1, column=0, sticky="w")
        self.method_var = ttk.StringVar(value="GET")
        method_combo = ttk.Combobox(self.frame, textvariable=self.method_var, values=["GET", "POST"], state="readonly")
        method_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="\U0001F4E6 Body JSON (POST):").grid(row=2, column=0, sticky="nw")
        self.json_text = tk.Text(self.frame, height=5, width=50)
        self.json_text.grid(row=2, column=1, padx=5, pady=5)

        placeholder = 'Ex: {\n  "nome": "Felipe",\n  "idade": 30\n}'
        self.json_text.insert("1.0", placeholder)
        self.json_text.config(fg="gray")

        def remover_placeholder(event):
            if self.json_text.get("1.0", "end").strip() == placeholder:
                self.json_text.delete("1.0", "end")
                self.json_text.config(fg="black")

        self.json_text.bind("<FocusIn>", remover_placeholder)

        def validar_json_visual():
            try:
                json.loads(self.json_text.get("1.0", "end").strip())
                self.json_text.config(highlightbackground="green", highlightcolor="green", highlightthickness=2)
                return True
            except:
                self.json_text.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
                return False

        self.json_text.bind("<KeyRelease>", lambda e: validar_json_visual())

        def preencher_body_exemplo():
            exemplo = '{\n  "nome": "Felipe",\n  "idade": 30,\n  "ativo": true\n}'
            self.json_text.delete("1.0", "end")
            self.json_text.insert("end", exemplo)
            self.json_text.config(fg="black")
            validar_json_visual()

        ttk.Button(self.frame, text="\U0001F4CC Exemplo", command=preencher_body_exemplo).grid(row=2, column=2, sticky="n", padx=5)

        def limpar_body():
            self.json_text.delete("1.0", "end")
            self.json_text.config(fg="black")
            validar_json_visual()

        ttk.Button(self.frame, text="\U0001FA9F Limpar", command=limpar_body).grid(row=2, column=3, sticky="n", padx=5)

        def carregar_json_de_arquivo():
            caminho = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
            if caminho:
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                        json.loads(conteudo)
                        self.json_text.delete("1.0", "end")
                        self.json_text.insert("end", conteudo)
                        self.json_text.config(fg="black")
                        validar_json_visual()
                except Exception as e:
                    messagebox.showerror("Erro ao carregar JSON", f"O arquivo não é um JSON válido:\n{str(e)}")

        ttk.Button(self.frame, text="\U0001F4C2 Carregar", command=carregar_json_de_arquivo).grid(row=2, column=4, sticky="n", padx=5)

        self.headers_frame = ttk.LabelFrame(self.frame, text="\U0001F9E0 Cabeçalhos (Headers)", padding=10)
        self.headers_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.headers_text = ttk.Text(self.headers_frame, height=4, width=60)
        self.headers_text.pack()

        self.cookies_frame = ttk.LabelFrame(self.frame, text="\U0001F36A Cookies", padding=10)
        self.cookies_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.cookies_text = ttk.Text(self.cookies_frame, height=3, width=60)
        self.cookies_text.pack()

        ttk.Label(self.frame, text="\U0001F522 Total de requisições:").grid(row=5, column=0, sticky="w")
        self.total_entry = ttk.Entry(self.frame)
        self.total_entry.insert(0, "1000")
        self.total_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="\u2699\ufe0f Conexões simultâneas:").grid(row=6, column=0, sticky="w")
        self.conc_entry = ttk.Entry(self.frame)
        self.conc_entry.insert(0, "100")
        self.conc_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="\U0001F9E0 User-Agent:").grid(row=7, column=0, sticky="w")
        self.ua_entry = ttk.Entry(self.frame, width=50)
        self.ua_entry.insert(0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36")
        self.ua_entry.grid(row=7, column=1, padx=5, pady=5)

        self.iniciar_btn = ttk.Button(self.frame, text="\u25B6\ufe0f Iniciar Teste", bootstyle=SUCCESS, command=self.iniciar_teste)
        self.iniciar_btn.grid(row=8, column=0, columnspan=2, pady=10)

        self.progress = ttk.Progressbar(self.frame, length=400, mode='determinate')
        self.progress.grid(row=9, column=0, columnspan=2, pady=5)

        self.progress_label = ttk.Label(self.frame, text="Progresso: 0%")
        self.progress_label.grid(row=10, column=0, columnspan=2)

        self.log_text = ttk.Text(self.frame, height=15, width=70)
        self.log_text.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
        self.log_text.insert("end", "[\u2139\ufe0f] Aguardando...\n")

        ttk.Button(self.frame, text="\U0001F3A8 Alternar Tema", command=self.alternar_tema).grid(row=12, column=0, pady=5)
        ttk.Button(self.frame, text="\U0001F4BE Salvar Log", command=self.salvar_log).grid(row=12, column=1, pady=5)

        self.user_agents = [
            self.ua_entry.get(),
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/89.0.4389.82 Safari/537.36"
        ]

    def parse_key_value(self, text_widget):
        linhas = text_widget.get("1.0", "end").strip().splitlines()
        resultado = {}
        for linha in linhas:
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                resultado[chave.strip()] = valor.strip()
        return resultado

    def log(self, mensagem, tipo="info"):
        cor = {
            "info": "blue",
            "success": "green",
            "error": "red"
        }.get(tipo, "black")
        self.log_text.insert("end", mensagem + "\n", tipo)
        self.log_text.tag_config(tipo, foreground=cor)
        self.log_text.see("end")

    def salvar_log(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de texto", "*.txt")])
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(self.log_text.get("1.0", "end"))
            self.log("[\U0001F4BE] Log salvo com sucesso!", tipo="success")

    def alternar_tema(self):
        temas = ["cyborg", "darkly", "flatly", "cosmo", "journal", "minty"]
        atual = self.master.style.theme.name
        proximo = temas[(temas.index(atual) + 1) % len(temas)] if atual in temas else temas[0]
        self.master.after(200, lambda: self.master.style.theme_use(proximo))
        self.log(f"[\U0001F3A8] Tema alterado para: {proximo}", tipo="info")

    def iniciar_teste(self):
        try:
            self.total = min(int(self.total_entry.get()), 10000)
            self.concorrentes = min(int(self.conc_entry.get()), 1000)
        except ValueError:
            messagebox.showerror("Erro", "Total e Conexões precisam ser números inteiros.")
            return

        if self.method_var.get() == "POST":
            try:
                self.json_body = json.loads(self.json_text.get("1.0", "end"))
            except json.JSONDecodeError:
                messagebox.showerror("Erro JSON", "Body JSON inválido!")
                return
        else:
            self.json_body = None

        self.headers = self.parse_key_value(self.headers_text)
        self.cookies = self.parse_key_value(self.cookies_text)

        self.iniciar_btn.config(state="disabled")
        Thread(target=self.run_async_test).start()

    def run_async_test(self):
        asyncio.run(self.executar_teste())

    def get_rotated_headers_and_cookies(self):
        headers = self.headers.copy()
        headers["User-Agent"] = random.choice(self.user_agents)
        cookies = self.cookies.copy()
        return headers, cookies

    async def executar_teste(self):
        self.url = self.url_entry.get()
        self.metodo = self.method_var.get()
        self.erros = 0
        self.respostas = {}
        self.progress["value"] = 0
        self.progress_label.config(text="Progresso: 0%")
        self.log(f"[\U0001F680] Iniciando teste em: {self.url} | Método: {self.metodo}")
        inicio = time.time()

        self.semaforo = asyncio.Semaphore(self.concorrentes)
        tarefas = [self.requisitar(i) for i in range(self.total)]
        await asyncio.gather(*tarefas)

        fim = time.time()
        total_ok = sum(self.respostas.values())
        taxa_sucesso = 100 * total_ok / self.total
        self.log(f"\n✅ Teste concluído em {round(fim - inicio, 2)} segundos.")
        self.log(f"📊 Respostas: {self.respostas}")
        self.log(f"❌ Erros: {self.erros}")
        self.log(f"🎯 Taxa de sucesso: {taxa_sucesso:.2f}%")
        self.iniciar_btn.config(state="normal")

    async def requisitar(self, i):
        headers, cookies = self.get_rotated_headers_and_cookies()
        await asyncio.sleep(random.uniform(0.1, 0.5))

        connector = aiohttp.TCPConnector(ssl=False)
        try:
            async with self.semaforo:
                async with aiohttp.ClientSession(connector=connector) as session:
                    if self.metodo == "POST":
                        async with session.post(self.url, json=self.json_body, headers=headers, cookies=cookies, timeout=5) as resp:
                            status = resp.status
                    else:
                        async with session.get(self.url, headers=headers, cookies=cookies, timeout=5) as resp:
                            status = resp.status

                    self.respostas[status] = self.respostas.get(status, 0) + 1
                    self.log(f"[{status}] {resp.url} | UA: {headers.get('User-Agent', 'N/A')}")
        except Exception as e:
            self.erros += 1
            self.log(f"[❌ ERRO] {str(e)}", tipo="error")

        self.progress["value"] += 1
        self.progress_label.config(text=f"Progresso: {int(self.progress['value'] / self.total * 100)}%")
        self.master.update_idletasks()

# Executar a aplicação
root = ttk.Window(themename=tema_inicial)
app = StressTester(root)
root.mainloop()
