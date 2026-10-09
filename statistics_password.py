import tkinter as tk
from tkinter import ttk, messagebox
from itertools import permutations

current = []   # كل كلمات المرور الممكنة


def generate():
    global current
    s = entry_digits.get().strip()

    # 1) تحقق من المدخلات
    if len(s) != 6 or not s.isdigit():
        messagebox.showerror("Error", "Enter exactly 6 digits, e.g. 123456")
        return

    # 2) توليد كل الترتيبات بدون تكرار
    current = sorted(set("".join(p) for p in permutations(s)))

    # 3) ملء الجدول: رقم الصف، الكلمة، مجموع الأرقام، هل الرقم زوجي
    tree.delete(*tree.get_children())
    sum_even_count = 0
    num_even_count = 0

    for i, pw in enumerate(current, start=1):
        digit_sum = sum(int(c) for c in pw)
        num_is_even = int(pw) % 2 == 0

        if digit_sum % 2 == 0:
            sum_even_count += 1
        if num_is_even:
            num_even_count += 1

        tree.insert("", "end", iid=str(i),
                    values=(i, pw, digit_sum, "Yes" if num_is_even else "No"))

    # 4) الإحصاء
    n = len(current)
    result_var.set(
        f"Total = {n}  |  P(sum even) = {sum_even_count / n:.4f}  |  "
        f"P(number even) = {num_even_count / n:.4f}"
    )


def search():
    guess = entry_search.get().strip()
    if not current:
        messagebox.showinfo("Info", "Generate the table first.")
        return
    if guess in current:
        idx = current.index(guess) + 1
        tree.selection_set(str(idx))
        tree.see(str(idx))
        result_var.set(f"{guess} is number {idx} of {len(current)}  |  P = {1 / len(current):.5f}")
    else:
        result_var.set(f"{guess} is NOT possible with these digits")


# ---------------- الواجهة ----------------
root = tk.Tk()
root.title("Password Sample Space")

top = ttk.Frame(root, padding=10)
top.pack(fill="x")

ttk.Label(top, text="6 digits:").grid(row=0, column=0)
entry_digits = ttk.Entry(top, width=10)
entry_digits.grid(row=0, column=1, padx=5)
ttk.Button(top, text="Generate", command=generate).grid(row=0, column=2)

ttk.Label(top, text="Search:").grid(row=0, column=3, padx=(20, 0))
entry_search = ttk.Entry(top, width=10)
entry_search.grid(row=0, column=4, padx=5)
ttk.Button(top, text="Find", command=search).grid(row=0, column=5)

frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame, columns=("n", "password", "sum", "even"),
                    show="headings", height=15)
for col, text, w in [("n", "#", 60), ("password", "Password", 120),
                     ("sum", "Digit sum", 90), ("even", "Number even?", 110)]:
    tree.heading(col, text=text)
    tree.column(col, width=w, anchor="center")

scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

result_var = tk.StringVar()
ttk.Label(root, textvariable=result_var, padding=10).pack()

root.mainloop()
