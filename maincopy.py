import tkinter as tk
import subprocess
import requests
import sys
import os
import zipfile
from pathlib import Path
from functools import partial

# バージョン情報
Version = 1.0
GITHUB_REPO = "https://github.com/BakedTaiyaki093/TyAppsLauncher"
VERSION_URL = "https://raw.githubusercontent.com/BakedTaiyaki093/TyAppsLauncher/main/Version.txt"
UPDATE_URL = "https://github.com/BakedTaiyaki093/TyAppsLauncher/raw/refs/heads/main/releases/TyAppsLauncher_latest.zip"

# 実行環境に適した `APP_FOLDER` の設定
if getattr(sys, 'frozen', False):  # .exe で動作中なら
    APP_FOLDER = Path.home() / "Documents" / "TyAppsLauncher"
else:  # Pythonスクリプトとして動作中なら
    APP_FOLDER = Path(__file__).parent

APP_FOLDER.mkdir(exist_ok=True)  # フォルダがなければ作成

# "Typath" フォルダを作成
folder = APP_FOLDER / "Typath"
folder.mkdir(exist_ok=True)

# ボタン情報のテキストファイル（"Typath" フォルダ内に保存）
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

def check_update():
    """最新バージョンを確認"""
    try:
        response = requests.get(VERSION_URL)
        latest_version = float(response.text.strip())  # 最新バージョン取得
        if latest_version > Version:
            label.config(text=f"新しいバージョン {latest_version} が利用可能です。アップデートを開始します。")
            update_app()
        else:
            label.config(text="最新のバージョンを使用しています。")
    except Exception as e:
        label.config(text=f"アップデート確認エラー: {e}")

def update_app():
    """GitHubから最新版をダウンロード＆適用"""
    try:
        response = requests.get(UPDATE_URL, stream=True)
        update_file = APP_FOLDER / "update.zip"

        with open(update_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        label.config(text="ダウンロード完了。アップデートを適用します...")
        apply_update(update_file)
    except Exception as e:
        label.config(text=f"アップデートエラー: {e}")

def apply_update(update_file):
    """アップデートを適用"""
    try:
        with zipfile.ZipFile(update_file, "r") as zip_ref:
            zip_ref.extractall(APP_FOLDER)

        label.config(text="アップデートが完了しました。アプリを再起動します。")
        restart_app()
    except Exception as e:
        label.config(text=f"アップデート適用エラー: {e}")

def restart_app():
    """アプリを再起動"""
    label.config(text="アプリを再起動します...")
    python = sys.executable
    os.execl(python, python, *sys.argv)  # プロセスを新しいバージョンに置き換え

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
root.title(f"Main window TAL@V{Version}")
root.geometry("400x300")

button_function = tk.Button(root, text="Create appspath_X.txt in Typath folder", command=createfile)
button_function.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

label = tk.Label(root, text="Create new appspath_X.txt in Typath folder after clicking the button")
label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

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
