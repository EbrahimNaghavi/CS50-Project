import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import cairosvg
import tempfile
import requests
import zipfile
import io
import pandas as pd
import subprocess
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import colormaps
import numpy as np
import re
import csv
import json


class PathGUI:
    def __init__(self, source, name, path=False):
        self.name = name
        self.root = Tk()
        self.root.title("The Human Protein Atlas Pathology Data")
        # Label on the top
        self.frame0 = ttk.Frame(self.root)
        self.frame0.pack(fill="both")
        self.frame0.columnconfigure(0, weight=1)
        self.frame0.columnconfigure(1, weight=1)
        self.style = ttk.Style(self.root)
        self.style.configure(
            "NoBorder.TLabel",
            background="white",
            foreground="gray",
            anchor="center",
            relief="raised",
            font=("Helvetica", 13, "bold"),
            borderwidth=0,
        )
        self.label = ttk.Label(
            self.frame0,
            padding=15,
            text="mRNA Expression and Patient Survival by Ebrahim Naghavi",
            style="TLabel",
        )
        self.label.grid(row=0, column=1, sticky="we")

        self.image_path = "https://www.proteinatlas.org/images_static/logo.svg"
        self.response = requests.get(self.image_path)
        self.svg_content = self.response.content
        # Convert SVG to PNG
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_png:
            cairosvg.svg2png(bytestring=self.svg_content, write_to=temp_png.name)
            self.temp_png_path = temp_png.name
        self.tkimage = Image.open(self.temp_png_path)
        self.tkimage = self.tkimage.resize((650, 50), Image.Resampling.NEAREST)
        self.tkimage = ImageTk.PhotoImage(self.tkimage)
        self.label2 = ttk.Label(self.frame0, image=self.tkimage, style="TLabel")
        self.label2.image = self.tkimage
        self.label2.grid(row=0, column=0, sticky="we")

        # 4 buttons in a 4-column-self.frame
        if not path:
            self.frame = ttk.Frame(self.root)
            self.frame.pack(fill="both")
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.style.configure("TButton", foreground="blue", font=("Arial", 10))
            self.gene_btn = ttk.Button(
                self.frame, text="Keyword search", command=self.filter_by_key
            )
            self.gene_btn.grid(row=0, column=0, sticky="we")
            self.path_btn = ttk.Button(
                self.frame, text="Quit", command=self.root.destroy
            )
            self.path_btn.grid(row=0, column=1, sticky="we")
        # for pathology file
        elif path:
            self.frame = ttk.Frame(self.root)
            self.frame.pack(fill="both")
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)
            self.frame.columnconfigure(2, weight=1)
            self.frame.columnconfigure(3, weight=1)
            self.gene_btn = ttk.Button(
                self.frame, text="Gene search", command=self.filter_by_gene
            )
            self.gene_btn.grid(row=0, column=0, sticky="we")
            self.path_btn = ttk.Button(
                self.frame, text="Pathology search", command=self.filter_by_pathology
            )
            self.path_btn.grid(row=0, column=1, sticky="we")
            self.reset_btn = ttk.Button(
                self.frame, text="Reset", command=lambda: self.reset(self.root)
            )
            self.reset_btn.grid(row=0, column=2, sticky="we")
            self.quit_btn = ttk.Button(
                self.frame, text="Quit", command=self.root.destroy
            )
            self.quit_btn.grid(row=0, column=3, sticky="we")
        # This is where the tabs go
        self.tabletabs = ttk.Notebook(self.root)
        self.tabletabs.pack(fill="both", expand=True)
        self.load_data(url=source, name=self.name)
        self.create_table(filename=f"edited_{self.name}.tsv")
        self.root.geometry("{}x{}".format(1500, 700))
        self.root.mainloop()

    @classmethod
    def load_data(cls, url, name):
        original = requests.get(url)
        original.raise_for_status()
        zip_file = zipfile.ZipFile(io.BytesIO(original.content))
        if f"{name}.tsv" not in zip_file.namelist():
            raise ValueError(f"{name}.tsv is no longer in Protein Atlas archive")
        with zip_file.open(f"{name}.tsv") as file:
            content = file.read().decode("utf-8")
        with open(f"loaded_{name}.tsv", "w") as tsvfile:
            tsvfile.write(content)
        p_data = pd.read_csv(f"loaded_{name}.tsv", sep="\t")
        if str(name) == "pathology":
            p_data = p_data.dropna(
                axis="index",
                how="all",
                subset=["High", "Medium", "Low", "Not detected"],
            )
            p_data = p_data.dropna(
                axis="index",
                how="all",
                subset=[
                    "prognostic - favorable",
                    "unprognostic - favorable",
                    "prognostic - unfavorable",
                    "unprognostic - unfavorable",
                ],
            )
        p_data = p_data.drop_duplicates()
        p_data.to_csv(f"edited_{name}.tsv", sep="\t", index=False)

    def create_table(self, filename, tabname={"Original"}):
        self.tableframe = ClosableTab(self.tabletabs)
        self.tableframe.pack(fill="both", expand=True)
        self.table = ttk.Treeview(self.tableframe)
        self.table.pack(fill="both", expand=True)
        self.table.tag_configure("custom", foreground="red")
        # Scrolling
        self.vertical = ttk.Scrollbar(
            self.table, orient="vertical", command=self.table.yview
        )
        self.horizontal = ttk.Scrollbar(
            self.table, orient="horizontal", command=self.table.xview
        )
        self.table.configure(
            yscrollcommand=self.vertical.set, xscrollcommand=self.horizontal.set
        )
        self.vertical.pack(side="right", fill="y")
        self.horizontal.pack(side="bottom", fill="x")
        # Put data inside table
        self.data = pd.read_csv(str(filename), sep="\t")
        for _, row in self.data.iterrows():
            self.table.insert("", "end", values=list(row))
        self.table["columns"] = list(pd.read_csv(str(filename), sep="\t").columns)
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
        self.table.column("#0", width=0)
        self.tabletabs.add(self.tableframe, text=f"{'|'.join(tabname)}")

    def filter_by_key(self):
        name = self.name
        # ask for a key in a new window
        self.questionk = simpledialog.askstring(
            "Filter data by keyword", "Only show rows containing this keyword:"
        )
        if not self.questionk:
            return
        elif self.questionk:
            # create a new TSV file for that gene
            self.og_data = pd.read_csv(f"edited_{name}.tsv", sep="\t")
            # select row if the keyword is in any of the columns
            self.filtered_data = self.og_data[
                self.og_data.map(
                    lambda a: self.questionk.lower() in str(a).lower()
                ).any(axis=1)
            ]

            if self.filtered_data.empty or len(self.questionk) < 3:
                messagebox.showinfo(
                    "Try Again!",
                    "Make sure your keyword exists in the table and has "
                    "at least three characters!",
                )
                raise ValueError
            else:
                self.filtered_data.to_csv(
                    f"{self.questionk.upper()}_edited_{name}.tsv", sep="\t", index=False
                )
                self.n_data = pd.read_csv(
                    f"{self.questionk.upper()}_edited_{name}.tsv", sep="\t"
                )
                self.create_table(
                    filename=f"{self.questionk.upper()}_edited_{name}.tsv",
                    tabname=["", f"{self.questionk.upper()}"],
                )

    def filter_by_gene(self):
        # ask gene in a new window
        self.questiong = simpledialog.askstring(
            "Filter data by gene", "What is your gene of interest?"
        )
        if not self.questiong:
            return
        elif self.questiong:
            # create a new TSV file for that gene
            self.og_data = pd.read_csv("edited_pathology.tsv", sep="\t")
            self.filtered_data = self.og_data[
                self.og_data["Gene name"].str.contains(self.questiong, case=False)
            ]
            if self.filtered_data.empty or len(self.questiong) < 3:
                messagebox.showinfo(
                    "Try Again!",
                    "Make sure your input contains some of the gene name and has "
                    "at least three characters!",
                )
                raise ValueError
            else:
                self.filtered_data.to_csv(
                    f"{self.questiong.upper()}_edited_pathology.tsv",
                    sep="\t",
                    index=False,
                )
                self.n_data = pd.read_csv(
                    f"{self.questiong.upper()}_edited_pathology.tsv", sep="\t"
                )
                self.create_table(
                    filename=f"{self.questiong.upper()}_edited_pathology.tsv",
                    tabname=set(self.n_data["Gene name"]),
                )
                self.create_pie_chart(
                    filename=f"{self.questiong.upper()}_edited_pathology.tsv",
                    category=set(self.n_data["Gene name"]),
                )
                self.create_patient_data(
                    filename=f"{self.questiong.upper()}_edited_pathology.tsv",
                    category1=set(self.n_data["Gene name"]),
                )

    def filter_by_pathology(self):
        # ask gene in a new window
        self.questionp = simpledialog.askstring(
            "Filter data by pathology", "What pathology are you looking for?"
        )
        if not self.questionp:
            return
        elif self.questionp:
            # create a new TSV file for that gene
            self.og_data1 = pd.read_csv("edited_pathology.tsv", sep="\t")
            self.filtered_data1 = self.og_data1[
                self.og_data1["Cancer"].str.contains(self.questionp, case=False)
            ]
            if self.filtered_data1.empty or len(self.questionp) < 3:
                messagebox.showinfo(
                    "Try Again!",
                    "Make sure your input contains some of the pathology name and has "
                    "at least three characters!",
                )
                raise ValueError
            else:
                self.filtered_data1.to_csv(
                    f"{self.questionp.upper()}_edited_pathology.tsv",
                    sep="\t",
                    index=False,
                )
                self.n_data1 = pd.read_csv(
                    f"{self.questionp.upper()}_edited_pathology.tsv", sep="\t"
                )
                self.create_table(
                    filename=f"{self.questionp.upper()}_edited_pathology.tsv",
                    tabname=set(self.n_data1["Cancer"]),
                )
                self.create_pie_chart(
                    filename=f"{self.questionp.upper()}_edited_pathology.tsv",
                    category=set(self.n_data1["Cancer"]),
                )
                self.create_patient_data(
                    filename=f"{self.questionp.upper()}_edited_pathology.tsv",
                    category1=set(self.n_data1["Cancer"]),
                )

    def create_pie_chart(self, filename, category):
        self.e_data = pd.read_csv(str(filename), sep="\t")
        self.data = {
            "Category": [
                "prognostic-favorable",
                "unprognostic-favorable",
                "prognostic-unfavorable",
                "unprognostic-unfavorable",
            ],
            "count": [
                self.e_data["prognostic - favorable"].count(),
                self.e_data["unprognostic - favorable"].count(),
                self.e_data["prognostic - unfavorable"].count(),
                self.e_data["unprognostic - unfavorable"].count(),
            ],
            "sum": [
                self.e_data["prognostic - favorable"].sum(),
                self.e_data["unprognostic - favorable"].sum(),
                self.e_data["prognostic - unfavorable"].sum(),
                self.e_data["unprognostic - unfavorable"].sum(),
            ],
        }
        self.p_data = pd.DataFrame(self.data)
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.p_data.plot(
            kind="pie",
            y="count",
            labels=self.p_data["Category"],
            colors=["lightskyblue", "yellow", "orange", "red"],
            autopct="%1.1f%%",
            startangle=140,
            ax=self.ax,
            legend=False,
        )
        self.ax.set_ylabel("")
        # pop-up window
        self.pop_up = tkinter.Toplevel(self.root)
        self.pop_up.title("Patient Survival and mRNA")
        # Put the chart in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.pop_up)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()
        # Avg log-rank p
        self.avg = self.p_data["sum"].sum() / self.p_data["count"].sum()
        self.label1 = ttk.Label(
            self.pop_up,
            padding=10,
            font=("Arial", 10),
            text=f"log-rank p value average for patient survival and mRNA correlation: {self.avg:.4f}",
        )
        self.label2 = ttk.Label(
            self.pop_up,
            padding=10,
            font=("Arial", 10),
            text=f'mRNA/Cancer: {",".join(category)}',
        )
        self.label2.pack(anchor="center", fill="both", side="bottom")
        self.label1.pack(anchor="center", fill="both", side="bottom")
        # Save the figure as image
        self.fig.savefig(f"Patient Survival_{','.join(category)}")

    def create_patient_data(self, filename, category1):
        self.o_data = pd.read_csv(str(filename), sep="\t")
        self.data = {
            "Category": ["High", "Medium", "Low", "Not detected"],
            "count": [
                self.o_data["High"].count(),
                self.o_data["Medium"].count(),
                self.o_data["Low"].count(),
                self.o_data["Not detected"].count(),
            ],
            "sum": [
                self.o_data["High"].sum(),
                self.o_data["Medium"].sum(),
                self.o_data["Low"].sum(),
                self.o_data["Not detected"].sum(),
            ],
        }
        # calculate the average number of patients annotated for different staining levels
        self.y_values = [
            self.data["sum"][3] / self.data["count"][3],
            self.data["sum"][2] / self.data["count"][2],
            self.data["sum"][1] / self.data["count"][1],
            self.data["sum"][0] / self.data["count"][0],
        ]
        # use list comprehension to round the number of patients
        self.rounded_y = [round(i, 0) for i in self.y_values]
        self.x_title = [
            "Not detected",
            "Low",
            "Medium",
            "High",
        ]
        # pop-up window
        self.pop_up = tkinter.Toplevel(self.root)
        self.pop_up.title("Staining Data")
        # Put the chart in the Tkinter window
        self.fig1 = Figure(figsize=(6, 4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        # add color gradient
        self.colorgrad = colormaps.get_cmap("Blues")
        self.normal = np.array(self.rounded_y) / max(self.rounded_y)
        self.colors = self.colorgrad(self.normal)

        self.ax1.bar(self.x_title, self.rounded_y, color=self.colors, edgecolor="black")
        self.ax1.set_xlabel("Level of Staining")
        self.ax1.set_ylabel("Number of Patients")
        self.ax1.set_title(
            "Average number of patients annotated for different staining levels"
        )
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.pop_up)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack()

        self.label3 = ttk.Label(
            self.pop_up,
            padding=10,
            font=("Arial", 10),
            text=f'mRNA/Cancer: {",".join(category1)}',
        )
        self.label3.pack(anchor="center", fill="both", side="bottom")
        # Save the figure as image
        self.fig.savefig(f"Staining Data_{','.join(category1)}")

    @classmethod
    def reset(cls, root):
        subprocess.Popen([sys.executable, "project.py"])
        root.destroy()


class ClosableTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.close_btn = ttk.Button(self, text="Close Tab", command=self.close_tab)
        self.close_btn.pack(anchor=SE)

    def close_tab(self):
        self.master.forget(self)


### main() Function & Command-Line Arguments:


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.exit("usage: project.py [URL] [-json tsv_file] [-list]")
    elif sys.argv[1] == "-json":
        convert_to_json(sys.argv[2])
    elif sys.argv[1] == "-list":
        path = filedialog.askopenfilename()
        messagebox.showinfo(
            "Selected File",
            f"ctrl + click on this path to open your selected file via TERMINAL: {show_files(path)}",
        )
        print(show_files(path))
    elif len(sys.argv) == 2:
        source = sys.argv[1]
        generated_gui = PathGUI(*validated(source))
        generated_gui
    else:
        sys.exit("usage: project.py [URL]] [-json tsv_file] [-list]")


def validated(link):
    source = link
    if matches := re.search(
        r"(https?://)?(www\.)?proteinatlas\.org/download/(.+\.tsv\.zip)", link
    ):
        if matches.group(3) == "pathology.tsv.zip":
            name = "pathology"
            path = True
            return source, name, path
        else:
            name = matches.group(3)[: -len(".tsv.zip")]
            print(f"View the raw data of {name} (no analysis)")
            return source, name
    else:
        raise ValueError(
            "Please copy a URL with .tsv.zip extension from https://www.proteinatlas.org/about/download"
        )


def show_files(p):
    if path_matches := re.search(
        r'^/([^\\/:*?"<>|]+\/)*[^\\/:*?"<>|]+\.[A-Za-z]{2,4}', p
    ):
        return p
    else:
        return f"No file in the correct format was selected"


def convert_to_json(tsv):
    try:
        table = []
        with open(tsv, "r") as file:
            reader = csv.DictReader(file, delimiter="\t")
            for row in reader:
                table.append(row)
        with open(f"{tsv[:-len('.tsv')]}.json", "w") as file1:
            json.dump(table, file1, indent=4)
            return f"{tsv[:-len('.tsv')]}.json is created in project folder"
    except FileNotFoundError:
        raise ValueError("Please choose an existing file")


if __name__ == "__main__":
    main()
