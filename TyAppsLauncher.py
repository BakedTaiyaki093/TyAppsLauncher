import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk
import subprocess
import requests
import sys
import os
import zipfile
from pathlib import Path
from functools import partial
import webbrowser as wbb

# バージョン情報
Version = 1.6
GITHUB_REPO = "https://github.com/BakedTaiyaki093"
VERSION_URL = "https://raw.githubusercontent.com/BakedTaiyaki093/TyAppsLauncher/main/Version.txt"
DOWNLOAD_URL = "https://github.com/BakedTaiyaki093/TyAppsLauncher/raw/refs/heads/main/releases/TyAppsLauncher.zip"
response = requests.get(VERSION_URL)
latest_version = float(response.text.strip())
# `dirct.txt` からフォルダパスを取得
with open("dirct.txt", "r", encoding="utf-8") as file:
    APP_FOLDER = Path(file.readline().strip())

# フォルダの存在確認（作成はしない）
if not APP_FOLDER.exists():
    print(f"エラー: 指定されたフォルダが存在しません → {APP_FOLDER}")
    sys.exit(1)  # フォルダがない場合は処理を停止

# フォルダのパスを設定（dirct.txtの中身を利用）
folder = APP_FOLDER

# ボタン情報のテキストファイル
button_names_file = folder / "PathIDButtonList.txt"

# 関数を管理する辞書
function_dict = {}

# ボタン表示名リスト（復元用）
button_labels = []

# **ボタン情報のテキストファイルを読み込む**
if button_names_file.exists():
    with open(button_names_file, "r", encoding="utf-8") as f:
        button_labels = [line.strip() for line in f.readlines()]
else:
    button_labels = []

def open_explorer():
    subprocess.Popen(["explorer", str(folder)], shell=True)

def open_github():
    wbb.open(GITHUB_REPO)

def loaddirct():
   
       # フォルダ選択ダイアログを表示
       path = fd.askdirectory(title="Please select the folder to save paths")
       if not path:
           mb.showwarning("Umm... Warning", "No folder selected! Please again select the folder!")
           return

       # 選択されたパスを dirct.txt に保存
       with open("dirct.txt", "w", encoding="utf-8") as file:
           file.write(path)
       mb.showinfo("Success!", f"Directory saved!: {path}") 
   
    
    
 

def check_update():
    """最新バージョンを確認"""
    try:
 
        if latest_version > Version:
            label.config(text=f"You can use a new version[@V{latest_version}] now.")
            

            result = mb.askyesnocancel(title= "Update Available", message=f"A new version[V{latest_version}] is available but we recommend download TyAppsDownLoader. Do you want to open the download page?\n Yes: Open GitHub\n No: Latest DownLoad\n Cancel: Do nothing")
            if result == True:
                 wbb.open(GITHUB_REPO)
            if result == False:
                 wbb.open(DOWNLOAD_URL)
                  
             
            
            
        else:
            label.config(text="You are using the latest version.")
    except Exception as e:
        label.config(text=f"Update Check Error: {e}")


    

def createfile():
    """新しいボタンを作成し、表示名・ファイルパスを保存"""
    file_num = len(list(folder.glob("appspath_*.txt"))) + 1  # 次のファイル番号を決定
    file_name = f"appspath_{file_num}.txt"
    file_path = folder / file_name
    file_path.touch()  # 書き込み可能なディレクトリ内に作成

    button_label = f"Button {file_num}"  # ボタンの表示名を設定
    label.config(text=f"Created: {button_label}")

    # **ボタン情報を保存**
    button_labels.append(button_label)
    with open(button_names_file, "w", encoding="utf-8") as f:
        f.write("\n".join(button_labels))

    # **ボタンとファイルの関係を関数辞書に登録**
    function_dict[button_label] = partial(execute_file, file_path)

    create_button_in_window(button_label)

def execute_file(file_path):
    """ボタンに対応するファイルを実行"""
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            file_paths = [line.strip() for line in f.readlines()]  # 各行のファイルパスを取得

        for path in file_paths:
            normalized_path = os.path.normpath(path.strip('"'))
            file_to_run = Path(normalized_path)

            print(f"実行対象のファイル: {file_to_run}")

            if file_to_run.exists():
                if file_to_run.suffix == ".py":
                    print(f"Pythonスクリプトを実行: {file_to_run}")
                    subprocess.Popen(["python", str(file_to_run)], shell=True)
                elif file_to_run.suffix in [".exe", ".bat"]:
                    print(f"実行ファイルを開く: {file_to_run}")
                    subprocess.Popen([str(file_to_run)], shell=True)
                else:
                    print(f"エラー: {file_to_run} は実行できるファイルではありません")
            else:
                print(f"エラー: {file_to_run} が見つかりません")
    else:
        print(f"エラー: {file_path} が存在しません")

def create_button_in_window(button_label):
    """表示名に対応するボタンを別ウィンドウに追加"""
    btn = tk.Button(rootf, text=button_label, command=function_dict.get(button_label, lambda: print(f"関数が見つかりません: {button_label}")))
    btn.pack()

# **メインウィンドウの作成**
root = tk.Tk()

root.title(f"TAL Main Window")
root.geometry("400x300")
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open folders...", command=loaddirct)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
button_function = tk.Button(root, text="Create appspath_X.txt in Typath folder", command=createfile)
button_function.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

label = tk.Label(root, text="Create new appspath_X.txt in Typath folder after clicking the button")
label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
button_ep = tk.Button(root, text= "Open explorer", command=open_explorer)
button_ep.place(relx = 0.5, rely = 0.7, anchor= tk.CENTER)
button_gh = tk.Button(root, text = "Open GitHub", command=open_github)
button_gh.place(relx = 0.5, rely = 0.6, anchor= tk.CENTER)

# **別ウィンドウにボタンを表示**
rootf = tk.Toplevel(root)
rootf.title(f"TyAppsLauncher@V{Version}")
rootf.geometry("400x800")

# **アプリ起動時にアップデートを確認**
check_update()

# **アプリ起動時にボタンを復元**
for file_num, button_label in enumerate(button_labels, start=1):
    file_path = folder / f"appspath_{file_num}.txt"
    function_dict[button_label] = partial(execute_file, file_path)
    create_button_in_window(button_label)

root.mainloop()