import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
try:
    df = pd.read_csv("jobs.csv")
except FileNotFoundError:
    messagebox.showerror("Error", "jobs.csv file not found!")
    exit()

# ---------------- Functions ---------------- #

def show_skill_chart():
    skill_counts = df["Skill"].value_counts()

    plt.figure(figsize=(8, 5))
    skill_counts.plot(kind="bar")
    plt.title("Most Demanded Skills")
    plt.xlabel("Skills")
    plt.ylabel("Number of Jobs")
    plt.tight_layout()
    plt.show()


def show_salary_chart():
    salary_data = df.groupby("Skill")["Salary"].mean()

    plt.figure(figsize=(8, 5))
    salary_data.plot(kind="bar")
    plt.title("Average Salary by Skill")
    plt.xlabel("Skill")
    plt.ylabel("Average Salary")
    plt.tight_layout()
    plt.show()


def search_skill():
    skill = search_entry.get().strip()

    if not skill:
        messagebox.showwarning("Warning", "Enter a skill!")
        return

    result = df[df["Skill"].str.lower() == skill.lower()]

    if len(result) == 0:
        result_label.config(
            text=f"No jobs found for '{skill}'"
        )
    else:
        result_label.config(
            text=f"Found {len(result)} job(s) requiring '{skill}'"
        )


def show_top_jobs():
    top_jobs = df.sort_values(
        by="Salary",
        ascending=False
    ).head(5)

    output = ""

    for _, row in top_jobs.iterrows():
        output += (
            f"{row['Job Title']} | "
            f"{row['Company']} | "
            f"₹{row['Salary']:,}\n"
        )

    messagebox.showinfo(
        "Top 5 Highest Paying Jobs",
        output
    )


# ---------------- Statistics ---------------- #

total_jobs = len(df)
top_skill = df["Skill"].value_counts().idxmax()
avg_salary = int(df["Salary"].mean())
highest_salary = int(df["Salary"].max())

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Job Market Analyzer")
root.geometry("900x650")
root.resizable(False, False)

title = tk.Label(
    root,
    text="📊 Job Market Analyzer",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)

# Statistics Frame
stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

tk.Label(
    stats_frame,
    text=f"Total Jobs: {total_jobs}",
    font=("Arial", 12, "bold")
).grid(row=0, column=0, padx=20)

tk.Label(
    stats_frame,
    text=f"Top Skill: {top_skill}",
    font=("Arial", 12, "bold")
).grid(row=0, column=1, padx=20)

tk.Label(
    stats_frame,
    text=f"Avg Salary: ₹{avg_salary:,}",
    font=("Arial", 12, "bold")
).grid(row=0, column=2, padx=20)

tk.Label(
    stats_frame,
    text=f"Highest Salary: ₹{highest_salary:,}",
    font=("Arial", 12, "bold")
).grid(row=0, column=3, padx=20)

# Search Section
search_frame = tk.Frame(root)
search_frame.pack(pady=20)

tk.Label(
    search_frame,
    text="Search Skill:",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10)

search_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 12)
)
search_entry.grid(row=0, column=1)

search_btn = tk.Button(
    search_frame,
    text="Search",
    command=search_skill,
    width=12
)
search_btn.grid(row=0, column=2, padx=10)

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 12)
)
result_label.pack()

# Table
table_frame = tk.Frame(root)
table_frame.pack(pady=20)

columns = list(df.columns)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

for _, row in df.iterrows():
    tree.insert("", tk.END, values=list(row))

tree.pack()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

skill_chart_btn = tk.Button(
    button_frame,
    text="Skill Demand Chart",
    command=show_skill_chart,
    width=20
)
skill_chart_btn.grid(row=0, column=0, padx=10)

salary_chart_btn = tk.Button(
    button_frame,
    text="Salary Analysis",
    command=show_salary_chart,
    width=20
)
salary_chart_btn.grid(row=0, column=1, padx=10)

top_jobs_btn = tk.Button(
    button_frame,
    text="Top Paying Jobs",
    command=show_top_jobs,
    width=20
)
top_jobs_btn.grid(row=0, column=2, padx=10)

# Footer
footer = tk.Label(
    root,
    text="Built with Python, Tkinter, Pandas & Matplotlib",
    font=("Arial", 10)
)
footer.pack(side="bottom", pady=10)

root.mainloop()