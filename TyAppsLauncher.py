import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import IntVar
from tkinter import simpledialog
# -*- coding: utf-8 -*-
import subprocess
import requests
import sys
import os
import zipfile
from pathlib import Path
from functools import partial
import webbrowser as wbb
import hashlib

# バージョン情報
Version = 1.81
GITHUB_REPO = "https://github.com/BakedTaiyaki093"
GITHUB_TYAPPSLAUNCHER = "https://github.com/BakedTaiyaki093/TyAppsLauncher"
VERSION_URL = "https://raw.githubusercontent.com/BakedTaiyaki093/TyAppsLauncher/main/Version.txt"
DOWNLOAD_URL = "https://github.com/BakedTaiyaki093/TyAppsLauncher/raw/refs/heads/main/releases/TyAppsLauncher.zip"


restart = "launch.bat"
response = requests.get(VERSION_URL)
latest_version = float(response.text.strip())

talver = requests.get(VERSION_URL).text.strip()  # TyAppsLauncherの最新バージョンを取得


# pow_1 = Settings.txtの1行目の値を保存するためのIntVar
# pow_2 = Settings.txtの2行目の値を保存するためのIntVar
# pow_3 = Settings.txtの3行目の値を保存するためのIntVar
# pow_1 = 起動時にアップデートを確認するかどうかの設定
# pow_2 = テーマの設定
# pow_3 = ウィンドウの表示モードの設定（0: メインウィンドウ, 1: アプリ一覧ウィンドウ）


# `dirct.txt` からフォルダパスを取得
with open("dirct.txt", "r", encoding="utf-8") as file:
    APP_FOLDER = Path(file.readline().strip())

# Settings.txtから設定値を読み込む
# (ここでは特に設定値は使用しないが、必要に応じて読み込むことができる)


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


def ifroot():
    settings = load_settings()  # Settings.txtから設定を読み込む
    if settings["theme"] == 0:
        default_theme()
    if settings["theme"] == 1:
        red_theme()
    if settings["theme"] == 2:
        black_theme()
    if settings["theme"] == 3:
        blue_theme()
    if settings["theme"] == 4:
        green_theme()
    if settings["theme"] == 5:
        yellow_theme()

def clear_widget():
    """ウィジェットをクリアする関数"""
    for widget in root.winfo_children():
        widget.destroy()
def utf8_to_bytes(pow_5):
    return list(pow_5.encode('utf-8'))
    
def decode_utf8_to_bytes():
    """UTF-8バイト列を文字列に変換する関数"""
    return pow_5.decode('utf-8') if isinstance(pow_5, bytes) else str(pow_5)

def resetpw():
    global pow_5
    rspwask = mb.askyesno("Reset Password?", "Do you really want to reset password?")
    if rspwask:
        
     pow_5 = ""
     pow_6.set(0)
     pow_5save()
     pow_6save()
    elif rspwask == False:
        return

def ifpassword():
    createrootfirst()  # 最初のウィンドウを作成
    root.destroy()  # 既存のウィンドウを閉じる
    global pow_5  # 忘れずに
    settings = load_settings()
    pow_5 = settings.get("password", "")  # 念のため再取得
    if settings["enablepassword"] == 1:
        dialogpassword()
    if settings["enablepassword"] == 0:
        createrootfirst()

def hash_password(password):
    """パスワードをSHA-256でハッシュ化して16進文字列で返す"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def setpassword():
    global pow_5
    pw = simpledialog.askstring("Set Password", "Please enter a password to enter TyAppsLauncher:")

    
    if pw:
        mb.showinfo("Password Set", "Password has been set successfully.")
        pow_5 = hash_password(pw)  # ハッシュ化して保存
        pow_5save()
    else:
        mb.showwarning("Warning", "No password entered. Please set a password to access the settings.")
        pow_6.set(0)
        pow_6save()
        
def exit_app_pw():
    exit = mb.askyesno("Exit", "Are you sure you want to exit?")
    if exit:
        root.quit()
    if exit == False:
        ifpassword()
    

 
def dialogpassword():
    pw = simpledialog.askstring("Password", "Please enter the password to enter TyAppsLauncher:")
    
    

    if pw == None:
        exit_app_pw()  # ユーザーがキャンセルした場合、アプリを終了
        return

    if hash_password(pw) == pow_5:
       createrootfirst()
    else:
        mb.showerror("Error", "Incorrect password. Please try again.")
        dialogpassword()  # パスワードが間違っている場合、再度入力を促す
        return
  
        
def topwindow():
    if pow_4.get() == 0:
    # pow_4が0の場合、ウィンドウを通常の位置に戻す
        root.attributes("-topmost", False) 
    if pow_4.get() == 1:
    # pow_4が1の場合、ウィンドウを最前面に設定    
       root.attributes("-topmost", True)  # ウィンドウを最前面に設定
    pow_4save()  # pow_4の値をSettings.txtに保存        

def clear_settings():
    """Settings.txtを初期化する関数"""
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.write("0\n0\n0\n0\n\n0")  # 初期値を設定
    pow_1.set(0)
    pow_2.set(0)
    pow_3.set(0)
    pow_4.set(0)
    pow_5 = str()  # pow_5を空文字列に設定
    pow_6.set(0)  # pow_6を0に設定
    wcs = mb.askyesnocancel("Are you sure?", "Do you want to clear the settings and restart the app?\nYes: Clear settings and restart\nNo: Clear settings but do not restart\nCancel: Do nothing")
    createmenubar()
    
    # ユーザーの選択に応じて処理を分岐
    if wcs == True:
       restartapp()  # ウィジェットをクリア
    if wcs == False:
        
        mb.showinfo("Settings Cleared", "Settings have been cleared. Please restart the app manually.")
        ifroot()  # テーマを適用
        createroot()  # 初期ウィンドウを再作成
        return
    if wcs == None:
        return
    
    createroot() # 初期ウィンドウを再作成
    ifroot()  # テーマを適用

def createrootfirst():
    """最初のウィンドウを作成"""
    global root, pow_1, label, button_function, pow_2, pow_3, pow_4, pow_5, pow_6
    
    root = tk.Tk()  # 新しいウィンドウを作成
    pow_1 = IntVar()
    pow_2 = IntVar()# 設定を保存するためのIntVar
    pow_3 = IntVar()# 設定を保存するためのIntVar
    pow_4 = IntVar()# 設定を保存するためのIntVar
    pow_5 = str()# 設定を保存するためのstr
    pow_6 = IntVar()# 設定を保存するためのIntVar
 
    settings = load_settings()  # Settings.txtから設定を読み込む
    root.title(f"Main Window TAL@V{Version}")
    root.geometry("400x250+500+300")  # ウィンドウのサイズと位置を設定
    root.iconbitmap("assets/tal3.ico")  # アイコンの設定（必要に応じて変更）
    
    button_function = tk.Button(root, text="Create appspath_X.txt in Typath folder", command=createfile)
    button_function.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    label = tk.Label(root, text="Create new appspath_X.txt in Typath folder after clicking the button")
    label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    pow_1.set(settings["EnableCheckUpdatelaunchapp"])  # Settings.txtから読み込んだ値を設定
    pow_2.set(settings["theme"])# Settings.txtから読み込んだ値を設定
    pow_3.set(int(settings["windowmode"]))# Settings.txtから読み込んだ値を設定
    pow_4.set(int(settings["alwaysontop"]))# Settings.txtから読み込んだ値を設定
    pow_5 = (settings.get("password", ""))  # Settings.txtから読み込んだ値を設定（パスワードがない場合は空文字列）
    pow_6.set(int(settings["enablepassword"]))  # Settings.txtから読み込んだ値を設定（パスワードの有効化）
    ifroot()  # テーマを適用
    root.protocol("WM_DELETE_WINDOW", exit_app)  # ウィンドウの閉じるボタンにexit_appを設定        
    createmenubar()  # メニューバーを作成
    if pow_3.get() == 0:
        createroot()
    if pow_3.get() == 1:
        createrootf()
    if pow_3.get() == 2:
        createinfo()
    topwindow()  # ウィンドウの常に最前面に表示する設定を適用

def createroot():
   
    clear_widget()  # 既存のウィジェットをクリア
      # 新しいウィンドウを作成
    root.title(f"TyAppsLauncher@V{Version} - Main Window")
    root.geometry("400x250+500+300")  # ウィンドウのサイズと位置を設定
    root.iconbitmap("assets/tal3.ico")  # アイコンの設定（必要に応じて変更
    global button_function, label
    button_function = tk.Button(root, text="Create txt for registration app", command=createfile)
    button_function.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    label = tk.Label(root, text="Create new registration txt file in Folder after clicking the button")
    label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    label1 = tk.Label(root, text=f"TyAppsLauncher@V{Version}")
    label1.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    createmenubar()
    pow_3.set(0)  # pow_3の値を0に設定
    pow_3save()  # pow_3の値をSettings.txtに保存

def createinfo():
    clear_widget()  # 既存のウィジェットをクリア

    root.title(f"TyAppsLauncher@V{Version} - Info Window")
    root.geometry("400x250+500+300")  # ウィンドウのサイズと位置を設定
    root.iconbitmap("assets/tal3.ico")  # アイコンの設定（必要に応じて変更）
    label = tk.Label(root, text="TyAppsLauncher is a simple app launcher. \n You can register apps easyly and launch them. :D")
    button_function= tk.Button(root, text=f"Open TyAppsLauncher@V{talver} GitHub", command=open_github_tal)
    button_function.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    
    button_function2 = tk.Button(root, text="Developed by BakedTaiyaki093", command=open_github)
    button_function2.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    createmenubar()  # メニューバーを作成
    pow_3.set(2)  # pow_3の値を2に設定
    pow_3save()  # pow_3の値をSettings.txtに保存

def createrootf():
    # 既存のウィンドウを閉じる
    clear_widget()  # 既存のウィジェットをクリア
    
    root.title(f"TyAppsLauncher@V{Version} - Apps Window")
    root.geometry("400x800+500+300")  # 別ウィンドウのサイズと位置を設定
    root.iconbitmap("assets/tal3.ico")# アイコンの設定（必要に応じて変更）
    root.after(100, createbuttons)  # ボタンを作成する関数を呼び出す
    createmenubar()
    pow_3.set(1)  # pow_3の値を0に設定
    pow_3save()  # pow_3の値をSettings.txtに保存

def createbuttons():
    for file_num, button_label in enumerate(button_labels, start=1):
        file_path = folder / f"appspath_{file_num}.txt"
        function_dict[button_label] = partial(execute_file, file_path)
        create_button_in_window(button_label)  

def default_theme():
    """デフォルトのテーマを適用する関数"""
    
    root.tk_setPalette(background='SystemButtonFace')  # 背景色をデフォルトに設定
    root.option_add('*TButton*highlightBackground', 'SystemButtonFace')  # ボタンのハイライト背景色をデフォルトに設定
    root.option_add('*TButton*highlightColor', 'SystemButtonText')  # ボタンのハイライト色をデフォルトに設定
    root.option_add('*TLabel*foreground', 'SystemButtonText')  # ラベルの文字色をデフォルトに設定
    pow_2.set(0)  # pow_2の値を0に設定

    
    
    pow_2save()  # pow_2の値をSettings.txtに保存

def red_theme():
    """赤いテーマを適用する関数"""
    
    root.tk_setPalette(background="#FF4A4A")  # 背景色を赤に設定
    root.option_add('*TButton*highlightBackground', '#ff4a4a')  # ボタンのハイライト背景色を設定
    root.option_add('*TButton*highlightColor', '#000000')  # ボタンのハイライト色を設定
    root.option_add('*TLabel*foreground', '#000000')  # ラベルの文字色をblackに設定
    
    pow_2.set(1)  # pow_2の値を1に設定
    pow_2save()# pow_2の値をSettings.txtに保存
    

def black_theme():
    """赤いテーマを適用する関数"""
    
    root.tk_setPalette(background="#3A3939")  # 背景色をblackに設定
    root.option_add('*TButton*highlightBackground', "#3A3939")  # ボタンのハイライト背景色を設定
    root.option_add('*TButton*highlightColor', "#ffffff")  # ボタンのハイライト色を設定
    root.option_add('*TLabel*foreground', '#ffffff')  # ラベルの文字色をblackに設定
    
    pow_2.set(2)  # pow_2の値を2に設定
    pow_2save()  # pow_2の値をSettings.txtに保存     

def blue_theme():
    """青いテーマを適用する関数"""
    
    root.tk_setPalette(background="#58A0FF")  # 背景色を青に設定
    root.option_add('*TButton*highlightBackground', "#58a0ff")  # ボタンのハイライト背景色を設定
    root.option_add('*TButton*highlightColor', "#000000")  # ボタンのハイライト色を設定
    root.option_add('*TLabel*foreground', '#000000')  # ラベルの文字色をblackに設定
    
    pow_2.set(3)  # pow_2の値を3に設定
    pow_2save()  # pow_2の値をSettings.txtに保存

def green_theme():
    """緑のテーマを適用する関数"""
    
    root.tk_setPalette(background="#74ff74")  # 背景色を緑に設定
    root.option_add('*TButton*highlightBackground', "#74FF74")  # ボタンのハイライト背景色を設定
    root.option_add('*TButton*highlightColor', "#000000")  # ボタンのハイライト色を設定
    root.option_add('*TLabel*foreground', '#000000')  # ラベルの文字色をblackに設定
    
    pow_2.set(4)  # pow_2の値を4に設定
    pow_2save()  # pow_2の値をSettings.txtに保存

def yellow_theme():
    """黄色のテーマを適用する関数"""
    
    root.tk_setPalette(background="#FFFF62")  # 背景色を黄色に設定
    root.option_add('*TButton*highlightBackground', "#ffff62")  # ボタンのハイライト背景色を設定
    root.option_add('*TButton*highlightColor', "#000000")  # ボタンのハイライト色を設定
    root.option_add('*TLabel*foreground', '#000000')  # ラベルの文字色をblackに設定
    
    pow_2.set(5)  # pow_2の値を5に設定
    pow_2save()  # pow_2の値をSettings.txtに保存

def createmenubar():
    root.iconbitmap("assets/tal3.ico")# アイコンの設定（必要に応じて変更）
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open Folders...", command=loaddir)
    filemenu.add_command(label="Open Explorer", command=open_explorer)
    filemenu.add_command(label="Open Author GitHub", command=open_github)
    filemenu.add_command(label="Open TyAppsLauncher GitHub", command=open_github_tal)
   
    filemenu.add_command(label="Open README", command=open_github_readme)
    
    filemenu.add_separator()
    filemenu.add_command(label="Restart", command=restartapp)
    filemenu.add_command(label="Exit", command=exit_app)
    menubar.add_cascade(label="Menu", menu=filemenu)
    # 設定メニューの作成
    thememenu = tk.Menu(menubar, tearoff=0)
    thememenu.add_command(label= "Default Theme", command=default_theme)
    thememenu.add_command(label= "Red Theme", command=red_theme)
    thememenu.add_command(label= "Black Theme", command=black_theme)
    thememenu.add_command(label= "Blue Theme", command=blue_theme)
    thememenu.add_command(label= "Green Theme", command=green_theme)
    thememenu.add_command(label= "Yellow Theme", command=yellow_theme)
    pow_1.set(0)# 初期値を0に設定
    pow_1.set(settings["EnableCheckUpdatelaunchapp"]) # Settings.txtから読み込んだ値を設定
    settingmenu = tk.Menu(menubar, tearoff=0)
    settingmenu.add_command(label="Version Information", command=verin)
    settingmenu.add_command(label="Check Update", command=check_update)
    
    settingmenu.add_cascade(label="Theme", menu=thememenu)  # テーマメニューを追加
    settingmenu.add_command(label="Set Password", command=setpassword)
    settingmenu.add_checkbutton(label="Enable Password", variable=pow_6 , command=onpassword)
    settingmenu.add_separator()
    settingmenu.add_command(label= "Reset Password", command=resetpw)
    settingmenu.add_command(label="Clear Settings", command=clear_settings)
    menubar.add_cascade(label="Settings", menu=settingmenu)
    # ウィンドウメニューの作成
    window = tk.Menu(menubar, tearoff=0)
    window.add_command(label="Main Window", command=createroot)
    window.add_command(label="Apps Window", command=createrootf)
    window.add_command(label="Info Window", command=createinfo)
    window.add_checkbutton(label="Always on Top", variable=pow_4, command=topwindow)
    menubar.add_cascade(label="Window", menu=window)


    root.config(menu=menubar)

#functions
def verin():
    """バージョン情報を表示"""
    mb.showinfo("Version Information", f"TyAppsLauncher Version: {Version}\nLatest Version: {latest_version}\nGitHub Repository: {GITHUB_REPO}")

def exit_app():
    """アプリを終了"""
    exit = mb.askyesno("Exit", "Are you sure you want to exit?")
    if exit:
        root.quit()
    if exit == False:
        return

def pow_1save():
    """pow_1の値をSettings.txtの1行目に保存"""
    try:
        with open("Settings.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    while len(lines) < 1:
        lines.append("\n")
    lines[0] = str(pow_1.get()) + "\n"
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

def pow_2save():
    """pow_2の値をSettings.txtの2行目に保存"""
    try:
        with open("Settings.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    while len(lines) < 2:
        lines.append("\n")
    lines[1] = str(pow_2.get()) + "\n"
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

def pow_3save():
    """pow_3の値をSettings.txtの3行目に保存"""
    try:
        with open("Settings.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    while len(lines) < 3:
        lines.append("\n")
    lines[2] = str(pow_3.get()) + "\n"
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

def pow_4save():
    """pow_4の値をSettings.txtの4行目に保存"""
    try:
        with open("Settings.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    while len(lines) < 4:
        lines.append("\n")
    lines[3] = str(pow_4.get()) + "\n"
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

def pow_5save():
    """pow_5の値をSettings.txtの5行目に保存"""
    try:
        with open("Settings.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    while len(lines) < 5:
        lines.append("\n")
    lines[4] = str(pow_5) + "\n"
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

def pow_6save():
    """pow_6の値をSettings.txtの6行目に保存"""
    try:
        with open("Settings.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    while len(lines) < 6:
        lines.append("\n")
    lines[5] = str(pow_6.get()) + "\n"
    with open("Settings.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

def onpassword():
    setpassword()
    pow_6save()

def open_explorer():
    subprocess.Popen(["explorer", str(folder)], shell=True)

def restartapp():
    """アプリを再起動"""
    if mb.askyesno("Restarting", "Are you sure you want to restarting?"):
     root.destroy()
     os.system(restart)  # launch.batを実行してアプリを再起動

def open_github():
    wbb.open(GITHUB_REPO)

def open_github_tal():
    wbb.open(GITHUB_TYAPPSLAUNCHER)


    
def open_github_readme():
    """README.mdをGitHubで開く"""
    readme_url = "https://github.com/BakedTaiyaki093/TyAppsLauncher/blob/main/README.md"
    wbb.open(readme_url)  # GitHubのREADME.mdを開く

def loaddir():
   
       # フォルダ選択ダイアログを表示
       path = fd.askdirectory(title="Please select the folder to save paths")
       if not path:
           mb.showwarning("Umm... Warning", "No folder selected! Please again select the folder!")
           return

       # 選択されたパスを dirct.txt に保存
       with open("dirct.txt", "w", encoding="utf-8") as file:
           file.write(path)
       result = mb.askyesnocancel("Success!", f"Directory saved!: {path}\nPlease restart now. \nDo you want to restart the app?")
       if result:
            restartapp()
              
              
       elif not result:
            mb.showinfo("Message","Please restart the app manually now.")   
    

 
def check_update():
    """最新バージョンを確認"""
    global label
    try:
        if latest_version > Version:
            result = mb.askyesnocancel(
                title="Update Available",
                message=f"A new version[V{latest_version}] is available.\n If you are using InstallVersion, we don't recommend download it.\n Do you want to download?\n Yes: Open GitHub\n No: Latest DownLoad\n Cancel: Do nothing"
            )
            if result == True:
                open_github()
            if result == False:
                wbb.open(DOWNLOAD_URL)
            if label is not None and hasattr(label, "winfo_exists") and label.winfo_exists():
                label.config(text=f"You can use a new version[@V{latest_version}] now.")
        else:
            if label is not None and hasattr(label, "winfo_exists") and label.winfo_exists():
                label.config(text="You are using the latest version.")
            mb.showinfo("Update is nothing.", "Not find a new version, You are using the latest version now.")
    except Exception as e:
        if label is not None and hasattr(label, "winfo_exists") and label.winfo_exists():
            label.config(text=f"Update Check Error: {e}")

def load_settings():
    """Settings.txtを行ごとに読み込んで辞書で返す"""
    settings_dict = {}
    with open("Settings.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    # 空文字列の場合は0を使う
    settings_dict["EnableCheckUpdatelaunchapp"] = int(lines[0]) if len(lines) > 0 and lines[0].isdigit() else 0
    settings_dict["theme"] = int(lines[1]) if len(lines) > 1 and lines[1].isdigit() else 0
    settings_dict["windowmode"] = int(lines[2]) if len(lines) > 2 and lines[2].isdigit() else 0
    settings_dict["alwaysontop"] = int(lines[3]) if len(lines) > 3 and lines[3].isdigit() else 0
    settings_dict["password"] = lines[4] if len(lines) > 4 else ""  # パスワードは文字列として保存
    settings_dict["enablepassword"] = int(lines[5]) if len(lines) > 5 and lines[5].isdigit() else 0  # パスワードの有効化設定
    return settings_dict

settings = load_settings()
pow_5 = settings.get("password", "")  # ここで必ず初期化
    

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
    btn = tk.Button(root, text=button_label, command=function_dict.get(button_label, lambda: print(f"関数が見つかりません: {button_label}")))
    btn.pack()


# **メインウィンドウの作成**

ifpassword()











# **アプリ起動時にアップデートを確認**


if pow_1.get() == 1: 
 check_update()




root.mainloop()