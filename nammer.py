import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".tif"}

def choose_folder():
    folder = filedialog.askdirectory(title="Selecione a pasta com as imagens")
    if folder:
        folder_var.set(folder)

def rename_images():
    folder = Path(folder_var.get())
    prefix = prefix_var.get().strip()

    if not folder.is_dir():
        messagebox.showerror("Erro", "Selecione uma pasta válida.")
        return

    if not prefix:
        messagebox.showerror("Erro", "Informe um prefixo.")
        return

    images = sorted(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS],
        key=lambda p: p.name.lower()
    )

    if not images:
        messagebox.showinfo("Resultado", "Nenhuma imagem encontrada na pasta.")
        return

    # Evita colisões: primeiro usa nomes temporários.
    temp_files = []
    for i, image in enumerate(images, 1):
        temp = folder / f".__renaming_tmp_{i:06d}{image.suffix.lower()}"
        while temp.exists():
            temp = folder / f".__renaming_tmp_{i:06d}_x{image.suffix.lower()}"
        image.rename(temp)
        temp_files.append((temp, image.suffix.lower()))

    for i, (temp, suffix) in enumerate(temp_files, 1):
        target = folder / f"{prefix} {i}{suffix}"
        temp.rename(target)

    messagebox.showinfo(
        "Concluído",
        f"{len(images)} imagem(ns) renomeada(s).\n\n"
        f"Formato: {prefix} 1, {prefix} 2, {prefix} 3..."
    )

root = tk.Tk()
root.title("Renomeador de Imagens")
root.geometry("560x220")
root.resizable(False, False)

folder_var = tk.StringVar()
prefix_var = tk.StringVar(value="imagem_name")

tk.Label(root, text="Pasta das imagens:").pack(anchor="w", padx=20, pady=(20, 5))

frame = tk.Frame(root)
frame.pack(fill="x", padx=20)

tk.Entry(frame, textvariable=folder_var).pack(side="left", fill="x", expand=True)
tk.Button(frame, text="Selecionar...", command=choose_folder).pack(side="right", padx=(8, 0))

tk.Label(root, text="Prefixo:").pack(anchor="w", padx=20, pady=(20, 5))
tk.Entry(root, textvariable=prefix_var).pack(fill="x", padx=20)

tk.Label(
    root,
    text='Exemplo: "imagem_name 1.jpg", "imagem_name 2.jpg", "imagem_name 3.jpg"',
    fg="gray"
).pack(anchor="w", padx=20, pady=(8, 15))

tk.Button(
    root,
    text="RENOMEAR IMAGENS",
    command=rename_images,
    height=2
).pack(pady=5)

root.mainloop()
