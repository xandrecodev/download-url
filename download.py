import mimetypes
import os
import threading
import urllib.request
from tkinter import END, Button, Frame, Label, StringVar, Tk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from urllib.parse import urlsplit


def parse_urls(text):
    urls = [url.strip() for url in text.split(";") if url.strip()]
    if not urls:
        raise ValueError("Cole pelo menos um link.")

    invalid_urls = [
        url
        for url in urls
        if urlsplit(url).scheme not in ("http", "https")
        or not urlsplit(url).netloc
    ]
    if invalid_urls:
        raise ValueError(
            "Estes links não parecem válidos (use http:// ou https://):\n"
            + "\n".join(invalid_urls)
        )

    return urls


def download_images(urls, destination, log):
    os.makedirs(destination, exist_ok=True)
    baixadas = 0
    falhas = 0

    for index, url in enumerate(urls, start=1):
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                content_type = response.headers.get_content_type()
                if not content_type.startswith("image/"):
                    raise ValueError(
                        f"A resposta não é uma imagem "
                        f"(Content-Type: {content_type})"
                    )

                extension = (
                    mimetypes.guess_extension(content_type)
                    or os.path.splitext(urlsplit(url).path)[1].lower()
                    or ".img"
                )
                if extension == ".jpe":
                    extension = ".jpg"

                filename = f"imagem-{index}{extension}"
                content = response.read()
                if not content:
                    raise ValueError("A resposta veio vazia")

            with open(os.path.join(destination, filename), "wb") as image_file:
                image_file.write(content)

            baixadas += 1
            log(f"[{index}/{len(urls)}] Baixada: {filename}")
        except Exception as error:
            falhas += 1
            log(f"[{index}/{len(urls)}] Falha: {url}\n    {error}")

    return baixadas, falhas


class ImageDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Baixar imagens de links")
        self.root.geometry("720x560")
        self.root.minsize(560, 420)

        self.destination = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "imagens_baixadas"
        )

        self._build_interface()

    def _build_interface(self):
        Label(
            self.root,
            text="Cole os links das imagens separados por ponto e vírgula (;):",
            anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 4))

        self.links_input = ScrolledText(self.root, height=8, wrap="word")
        self.links_input.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        self.destination_label = StringVar(value=self.destination)
        Label(self.root, text="Pasta para salvar:", anchor="w").pack(
            fill="x", padx=12
        )
        destination_frame = Frame(self.root)
        destination_frame.pack(fill="x", padx=12, pady=(4, 10))
        Label(
            destination_frame,
            textvariable=self.destination_label,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)
        Button(
            destination_frame,
            text="Escolher pasta...",
            command=self._choose_destination,
        ).pack(side="right", padx=(8, 0))

        self.download_button = Button(
            self.root, text="Baixar imagens", command=self._start_download
        )
        self.download_button.pack(padx=12, pady=(0, 10))

        Label(self.root, text="Progresso:", anchor="w").pack(fill="x", padx=12)
        self.log_output = ScrolledText(self.root, height=10, state="disabled")
        self.log_output.pack(fill="both", expand=True, padx=12, pady=(4, 12))

    def _choose_destination(self):
        selected = filedialog.askdirectory(
            title="Escolha onde salvar as imagens",
            initialdir=self.destination,
        )
        if selected:
            self.destination = selected
            self.destination_label.set(selected)

    def _start_download(self):
        try:
            urls = parse_urls(self.links_input.get("1.0", END))
        except ValueError as error:
            messagebox.showerror("Links inválidos", str(error))
            return

        self.download_button.config(state="disabled")
        self._write_log(f"Iniciando download de {len(urls)} imagem(ns)...")
        threading.Thread(
            target=self._download_worker, args=(urls,), daemon=True
        ).start()

    def _download_worker(self, urls):
        try:
            baixadas, falhas = download_images(
                urls,
                self.destination,
                lambda message: self.root.after(0, self._write_log, message),
            )
            self.root.after(
                0,
                self._finish_download,
                baixadas,
                falhas,
            )
        except Exception as error:
            self.root.after(0, self._download_error, str(error))

    def _finish_download(self, baixadas, falhas):
        self._write_log(
            f"Concluído: {baixadas} baixada(s), {falhas} falha(s)."
        )
        self.download_button.config(state="normal")
        messagebox.showinfo(
            "Download concluído",
            f"{baixadas} imagem(ns) baixada(s).\n{falhas} falha(s).\n"
            f"Local: {self.destination}",
        )

    def _download_error(self, error):
        self.download_button.config(state="normal")
        self._write_log(f"Erro ao iniciar downloads: {error}")
        messagebox.showerror("Erro no download", error)

    def _write_log(self, message):
        self.log_output.config(state="normal")
        self.log_output.insert(END, message + "\n")
        self.log_output.see(END)
        self.log_output.config(state="disabled")


if __name__ == "__main__":
    app_root = Tk()
    ImageDownloader(app_root)
    app_root.mainloop()
