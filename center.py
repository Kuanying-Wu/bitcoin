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


def plot_function(coin_type, remain_coin):
    
    plot.Manager(coin_type).main(remain_coin)
    plt.tight_layout()
    return plt.gcf()  # 返回當前的圖表對象

class PlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plot Generator")

        # 設置當用戶點擊右上角 "X" 按鈕時的操作
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 輸入提示和輸入框
        self.label1 = tk.Label(root, text="請輸入查找幣(例如: BTC):")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.entry1 = tk.Entry(root)
        self.entry1.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # 投入幣數量
        self.label2 = tk.Label(root, text="請輸入剩餘可投入幣數量:")
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.entry2 = tk.Entry(root)
        self.entry2.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # 繪圖按鈕
        self.plot_button = tk.Button(root, text="繪圖", command=self.plot_graph)
        self.plot_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        
        # 圖片顯示區域
        self.image_canvas = tk.Canvas(root, width=640, height=480, bg='white')
        self.image_canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def plot_graph(self):
        try:
            coin_type = self.entry1.get()
            remain_coin = float(self.entry2.get())
<<<<<<< HEAD
            if not coin_type :
=======
            if not coin_type or not remain_coin:
>>>>>>> e475a4c1640bba637a42ac7178a26279e9fedc44
                raise ValueError("輸入不能為空")  # 檢查是否為空輸入
            fig = plot_function(coin_type, remain_coin)  # 調用繪圖函數
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
