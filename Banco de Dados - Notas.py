import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Função para carregar notas do arquivo
def load_notes():
    if os.path.exists('notes.json'):
        with open('notes.json', 'r') as file:
            return json.load(file)
    return []

# Função para salvar notas no arquivo
def save_notes(notes):
    with open('notes.json', 'w') as file:
        json.dump(notes, file)

# Função para adicionar nova nota
def add_note():
    note_text = note_text_area.get("1.0", tk.END).strip()
    note_date = date_entry.get()

    if note_text and note_date:
        notes = load_notes()
        notes.append({'text': note_text, 'date': note_date})
        save_notes(notes)
        note_text_area.delete("1.0", tk.END)
        date_entry.delete(0, tk.END)
        display_notes()
        messagebox.showinfo("Sucesso", "Nota salva com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

# Função para exibir notas na tabela
def display_notes(filter_text=""):
    for row in tree.get_children():
        tree.delete(row)
    notes = load_notes()
    for note in notes:
        if filter_text.lower() in note['text'].lower() or filter_text in note['date']:
            tree.insert("", tk.END, values=(note['text'], note['date']))

# Função para buscar notas
def search_notes():
    filter_text = search_entry.get().strip()
    display_notes(filter_text)

# Função para selecionar uma nota para edição
def select_note_for_edit(event):
    selected_item = tree.selection()
    if selected_item:
        note = tree.item(selected_item)["values"]
        note_text_area.delete("1.0", tk.END)
        note_text_area.insert("1.0", note[0])
        date_entry.delete(0, tk.END)
        date_entry.insert(0, note[1])
        edit_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)
        global current_edit_index
        current_edit_index = tree.index(selected_item)

# Função para editar a nota selecionada
def edit_note():
    note_text = note_text_area.get("1.0", tk.END).strip()
    note_date = date_entry.get()

    if note_text and note_date:
        notes = load_notes()
        notes[current_edit_index] = {'text': note_text, 'date': note_date}
        save_notes(notes)
        display_notes()
        clear_fields()
        messagebox.showinfo("Sucesso", "Nota editada com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

# Função para excluir a nota selecionada
def delete_note():
    notes = load_notes()
    notes.pop(current_edit_index)
    save_notes(notes)
    display_notes()
    clear_fields()
    messagebox.showinfo("Sucesso", "Nota excluída com sucesso!")

# Função para limpar os campos
def clear_fields():
    note_text_area.delete("1.0", tk.END)
    date_entry.delete(0, tk.END)
    edit_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)

# Configuração da janela principal
root = tk.Tk()
root.title("Gerenciar Notas")
root.geometry("600x500")
root.configure(bg="#f0f8ff")

# Título
title_label = tk.Label(root, text="Adicionar Nota", font=("Segoe UI", 16), bg="#f0f8ff", fg="#2c3e50")
title_label.pack(pady=10)

# Área de texto para a nota
note_text_area = tk.Text(root, height=5, width=50, font=("Segoe UI", 12))
note_text_area.pack(pady=10)

# Campo de data
date_entry = tk.Entry(root, font=("Segoe UI", 12))
date_entry.pack(pady=5)
date_entry.insert(0, "DD-MM-YYYY")

# Botão de salvar
save_button = tk.Button(root, text="Salvar Nota", command=add_note, bg="#27ae60", fg="white")
save_button.pack(pady=5)

# Botão de editar
edit_button = tk.Button(root, text="Editar Nota", command=edit_note, bg="#f39c12", fg="white", state=tk.DISABLED)
edit_button.pack(pady=5)

# Botão de excluir
delete_button = tk.Button(root, text="Excluir Nota", command=delete_note, bg="#e74c3c", fg="white", state=tk.DISABLED)
delete_button.pack(pady=5)

# Barra de busca
search_label = tk.Label(root, text="Buscar Nota:", font=("Segoe UI", 12), bg="#f0f8ff", fg="#2c3e50")
search_label.pack(pady=5)
search_entry = tk.Entry(root, font=("Segoe UI", 12), width=30)
search_entry.pack(pady=5)
search_button = tk.Button(root, text="Buscar", command=search_notes, bg="#3498db", fg="white")
search_button.pack(pady=5)

# Tabela para exibir as notas
columns = ("Nota", "Data")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("Nota", text="Nota")
tree.heading("Data", text="Data")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Associar a seleção da tabela ao evento de editar
tree.bind("<ButtonRelease-1>", select_note_for_edit)

# Chamar função para exibir notas ao iniciar
display_notes()

# Iniciar o loop principal
root.mainloop()
