import tkinter as tk
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import seaborn as sns
from module import plot
import importlib as ib

def reload_module(mode_name):
    ib.reload(mode_name)
ib.reload(plot)

# 更新的繪圖函數，假設 A 現在是文字，例如 "BTC"
def plot_function(A):
    # 在這裡你可以根據 A 的值來選擇不同的數據或圖表
    # data = sns.load_dataset("iris")  # 使用 seaborn 的 Iris 數據集作為例子
    # plt.figure(figsize=(6, 4))
    # sns.scatterplot(data=data, x="sepal_length", y="sepal_width", hue="species")
    # plt.title(f"Plot for {A}")  # 在標題中顯示 A 的值
    # plt.tight_layout()
    plot.Manager('BTC').main()
    plt.tight_layout()
    return plt.gcf()  # 返回當前的圖表對象

class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plot Generator")

        # 設置當用戶點擊右上角 "X" 按鈕時的操作
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 輸入提示和輸入框
        self.label = tk.Label(root, text="請輸入查找對象(例如: BTC):")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.entry = tk.Entry(root)
        self.entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # 繪圖按鈕
        self.plot_button = tk.Button(root, text="繪圖", command=self.plot_graph)
        self.plot_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        # 圖片顯示區域
        self.image_canvas = tk.Canvas(root, width=640, height=480, bg='white')
        self.image_canvas.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def plot_graph(self):
        try:
            A = self.entry.get()  # 獲取輸入的文字 A
            if not A:
                raise ValueError("輸入不能為空")  # 檢查是否為空輸入
            fig = plot_function(A)  # 調用繪圖函數
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)
            self.imgtk = ImageTk.PhotoImage(img)
            self.image_canvas.create_image(0, 0, anchor='nw', image=self.imgtk)
        except ValueError as e:
            messagebox.showerror("輸入錯誤", str(e))
        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤: {str(e)}")

    def on_closing(self):
        if messagebox.askokcancel("退出", "你確定要退出嗎?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
