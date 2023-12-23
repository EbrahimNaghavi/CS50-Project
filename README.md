# Exploring The Human Protein Atlas Datasets with Python GUI

#### A graphical user interface to explore [pathology data](https://www.proteinatlas.org/download/pathology.tsv.zip) at [The Human Protein Atlas website](https://www.proteinatlas.org/about/download): save images of the analysis, and acquire data of your gene or pathology of interest in TSV or JSON format
#### [YouTube Video Demo](https://www.youtube.com/watch?v=28YFMvx18PE)

## 1. Introduction:
The purpose of this project is to provide a graphical user interface(GUI) that extracts specific data from [The Human Protein Atlas](https://www.proteinatlas.org/about/download), shows the data in a table, and performs some analysis based on the *gene* or *pathology* that is of interest to the user.
The *class* concept was the most challenging for me to get used to. Therefore, I availed myself of the opportunity to become acquainted with *python classes*! In this project, the user interface is treated as an object type that accepts a URL stored in the `Source` variable and outputs the information from that URL in a GUI window. Here, the user can search for genes/pathology to investigate, and save the analysis. I wrote the analytical capabilities of the GUI specifically for the [Pathology Data](https://www.proteinatlas.org/download/pathology.tsv.zip) that is archived at The Human Protein Atlas website([Downloadable Data](https://www.proteinatlas.org/about/download)). However, any of the TSV files on that [page](https://www.proteinatlas.org/about/download) can be viewed by typing the corresponding URL as a command line argument. In the resulting window, the user can filter the data to only show rows containing a keyword of their choice.
> References:
> The Human Protein Atlas [version 23.0](https://www.proteinatlas.org/about/releases#23.0)
> & Ensembl [version 109](http://feb2023.archive.ensembl.org/index.html)

## 2. A Short Guide to Operate The Program:

#### 2.1. pip install the packages in requirements.txt
#### 2.2. Type `python project.py https://www.proteinatlas.org/download/pathology.tsv.zip` in the terminal
    - View the table containing mRNA Expression and correlated Patient Survival data
    - Click on the **Gene search** or **Pathology search** button and type the gene or pathology you are interested in (the input should have at least three characters of the gene/pathology you are looking for). Two windows will pop up
    - Patient survival and mRNA: Showing the percentage of different cancer severity levels in a pie chart, and the p-value of correlation between genetic data and patient survival
    - Staining Data: Presenting the number of patients in each category of immunohistochemistry staining level
#### 2.3. Type `python project.py ` followed by the link copied from any of the TSV files archived at The Human Protein Atlas website [Downloadable Data](https://www.proteinatlas.org/about/download)
    - A simple GUI will present the data in a table
    - The data can be filtered by a keyword to rows that contain that keyword
#### 2.4. Type `python project.py -json ` followed by the name of a TSV file you extracted in previous steps
    - The TSV file will be converted to a JSON file
#### 2.5. Type `python project.py -list`
    - Here you can view the files created in the project folder
    - You can copy the gene and pathology analysis PNG images

## 3. Pathology Data

As described on [The Human Protein Atlas website](https://www.proteinatlas.org/about/download), the pathology data lists the following information for each genetic marker (mRNA expression):
- Gene (Ensembl ID) and Gene name
- Pathology that may or may not be associated with that gene
- Number of patients placed in each Immunohistochemistry staining level (High, Medium, Low, and Not detected)
- The severity of disease and p-value of patient survival and mRNA expression correlation using log-rank test (survival function comparison)
This information is displayed in the GUI window upon running the program by the following command in the terminal;

    `python project.py https://www.proteinatlas.org/download/pathology.tsv.zip`

The user can choose to filter this data by **Gene Name** or **Pathology** by clicking on the corresponding buttons at the top of the table. The user input should contain at least three characters of the gene or pathology. The newly generated tabular data will be displayed in a new tab. As well as the new filtered table, two windows will pop up;

### 3.1. Patient Survival and mRNA Correlation

![pie chart](/project/images/pie_genes_gui_analysis.png)

In this window, a pie chart will represent the percentage of rows(specific gene and pathology) containing pathology or gene searched by the user in the following categories:
- Prognostic-Favorable(light blue): The genetic data can predict the patient's survival, and medical interventions mitigate the patient's condition
- Unprognostic-Favorable(yellow): It is difficult to make predictions from genetic data, but medical interventions are impactful
- Prognostic-Unfavorable(orange): Predictable, but hard to treat
- Unprognostic-unfavorable(red): Neither the genetic data can make significant predictions, nor the patient respond to treatment
    >Note: Even though "Unprognostic" is not the correct English term to use, I decided to use the terminology observed in the original data to prevent confusion. I suspect, this may be an inaccuracy in translation. Having said that, the definition is not hard to interpret medically.

Under the pie chart, the average p-value of the correlation between genetic data and patient survival can be found. This correlation is calculated using the log-rank method, which tries to fit the survival functions of mRNA data and Patient survival together for each disease, and measures how precise one is in predicting the other. The smaller the p-value, the better mRNA expression can make prognostic predictions. Note that, here I have calculated the average of all p-values for your search. If you want to see each p-value, you can check the table.

### 3.2. Staining Data

![Staining graph](/project/images/histo_genes_gui_analysis.png)

Each row showing the number of patients at different staining levels is the result of a [immunohistochemically stained tissue microarray test](https://www.jove.com/t/3620/production-tissue-microarrays-immunohistochemistry-staining). This is a high-throughput analysis that shows the level of mRNA expression(*mentioned in Gene and Gene name column*) in a patient with a specific cancer(*Cancer column*).
In this window, you can view a histogram showing the average number of patients in four staining levels (Not detected, Low, Medium, High) who were tested for the Gene or Pathology you searched for. For a Gene like BRAF(Known to be mutated in human cancer), you can see that mRNA expression is at high levels among patients. However, I do not expect this sample size to be a good representative of global clinical data.

> On that note, I would like to emphasize that the goal of this project is to show what can be done with a similar dataset using Python programming and relevant libraries. **I do not claim that this data is scientifically accurate** or a good representation of global oncological data. **Please refer to a medical professional for your oncology questions**.

## 4. How The Program Works

### Using Class to Create a GUI Object
To my understanding, the difference between a program that uses only functions and one that utilizes classes is that the latter responds to a need for creating separate objects that behave in the same manner according to a given blueprint. What determines that behaviour is the class(the `PathGUI` class in this case). The GUI representing "normal_tissue.tsv.zip" and "subcellular_location.tsv.zip" data can be two different objects, even though both are created by calling the class `PathGUI`. This quality of classes in Python has led me to choose this framework for my final project. But before explaining this project's **class structure**, I am going to show how the `main()` function takes the user's command-line arguments to perform a few functions including class instance generation.

### 4.1. `main()` Function & Command-Line Arguments

The main function uses conditionals to call the proper function based on the user's command-line argument. The following guide will appear if the program is run without the appropriate command-line arguments:

`usage: project.py [URL] [-json tsv_file] [-list]`

This refers to the three options that the users may choose to type after the file name, `project.py`:

#### 4.1.1. type the link to pathalogy.tsv.zip or any of the other datasets with the same extension

> URL for Pathology Data = "https://www.proteinatlas.org/download/pathology.tsv.zip"

This will create and call the object *generated_gui* which is an instance of the class *PathGUI*. As a result, the GUI generated by the *tkinter library* will present itself to the user. The architecture of that GUI can be found in the [GUI Structure](gui-strc) section.

#### 4.1.2. Type 'python project.py -json ' followed by the name of an extracted TSV file
`main()` will call the function `convert_to_json(tsv)`. When the user explores the data sets using the `PathGUI` class, the following TSV files can be created (words in `{}` are subject to change):
- `loaded_{file name}.tsv` is the original file from the website. `{file name}` is what appears before the .tsv.zip extension at the URL of interest
- `edited_{file name}.tsv` is the file storing clean data
- `{charachters searched by the user}_edited_{file name}.tsv` is the file generated when the user filters data for one or more specific keywords, genes, or pathology.

If the TSV file named in the command-line argument exists in the project folder, it will be converted to a JSON file which is considered the standard for data interchange and is the primary format in many databases.

#### 4.1.3. Type 'python project.py -list'
The project folder window will open to view and copy the project files including the gene and pathology analysis PNG images;
- `Patient Survival_{gene/pathology}.png`
- `Staining Data_{gene/pathology}.png`

By selecting a file and clicking on open, a message box will notify you to confirm your selection (file name, and path), and the path is printed at the terminal.

#### 4.1.4. Code

```
def main():
    if len(sys.argv)<2 or len(sys.argv)>3:
        sys.exit("usage: project.py [URL] [-json tsv_file] [-list]")
    elif sys.argv[1] == "-json":
        convert_to_json(sys.argv[2])
    elif sys.argv[1] == "-list":
        print(show_files())
    elif len(sys.argv) == 2:
        source = sys.argv[1]
        generated_gui = PathGUI(*validated(source))
        generated_gui
    else:
        sys.exit("usage: project.py [URL] [-json tsv_file] [-list]")

def validated(link):
    ...

def show_files():
    ...

def convert_to_json(tsv):
# converts TSV files to JSON
    ...

if __name__ == "__main__":
    main()
```
- `main()` guides the program to a specific function if certain conditions are met
- `generated_gui = PathGUI(*validated(source))` unpacks source, name, and path variable values returned from the `validated()` function. Then it creates an instance of the class PathGUI named `generated_gui`.
- `validated()` utilizes the regular expression (re) library to validate the URL and identify if it is Pathology Data or another supportable data file
- `show_files()` opens a window where all the TSV, CSV, and PNG files created by the user can be viewed. The path of the selected file will be shown in the terminal
- `convert_to_json()`converts TSV files to JSON

### 4.3. [GUI Structure](#gui-strc)
#### 4.3.1. `PathGUI` Class Instantiation
At first, I created a simpler model of the `PathGUI` class for the users to be able to open all TSV files on the [Downloadable Data](https://www.proteinatlas.org/about/download) page. Then I realized the more efficient method would be to define a variable (*path*) inside *PathGUI* that changes certain functionalities if it was True versus False since there are only two different types of GUI I am considering for this project. Upon validation of the user's command-line input via the `validated` function, three variables are assigned a value:
- `source`: the URL that will be requested from [Protein Atlas](https://www.proteinatlas.org/about/download)
- `name`: the name of the extracted file without the extensions
- `path`: contains a boolean value that is **True** if the user has requested **Pathology Data**

The unpacked values for these variables are fed to the *PathGUI class* and a new object is created based on the class's blueprint (code below). If `path` is False(default), the resulting GUI can filter data by keywords only, meaning analysis functions designed for Pathology Data would not be called;

![Generic GUI](/project/images/generic_gui_main.png)

In this instance, the keyword Search button allows the user to create a new tab with rows of the original data that contain the user's typed input. The quit button will terminate the GUI.

On the other hand, if *path* is True, meaning the user has copied the link to [Pathology Data](https://www.proteinatlas.org/download/pathology.tsv.zip), the GUI window would have analysis features related to Pathology Data;

![Path GUI](/project/images/path_gui_main.png)

The Gene and Pathology search buttons will filter and analyze the data as described in **3.Pathology Data**. The reset button will run the program again to update the original data and close all the other tabs. And finally, the Quit button will do as expected.

#### 4.3.2. Class Mold Components
The GUI design consists of multiple tkinter frames, some inside of the other, that are organized by a tkinter `grid`. On the very top is the image extracted from [Protein Atlas page](https://www.proteinatlas.org/about/download), converted to PNG, and placed on the first column of the first row. The other component of that row is a *tkinter label* that satisfies my ego by housing my name! The second row is where the *ttk.Button* instances are to perform a certain `command` when clicked. finally, at the bottom, resides a ttk `Notebook` that is inside a special frame that is an instance of a descendant of `ttk.Frame`, a class named `ClosableTab`. Within that frame, the modified data extracted from [Protein Atlas](https://www.proteinatlas.org/about/download) is shown according to the  `ttk.Treeview` class blueprint.
The issue before this final design was that any new table generated by a search input would appear right below the previous table(s). Hence, after a few searches, scrolling the tables would become difficult. Also, unwanted data tables could not be closed. To fix that problem, `ttk.Notebook` and the concept of inheritance in classes came to aid;

```
class PathGUI:
    def __init__(self, source, name, path=False):
    ...
    self.tabletabs = ttk.Notebook(self.root)
    ...
    def create_table(self, filename, tabname={"Original"}):
        self.tableframe = ClosableTab(self.tabletabs) # tkinter Notebook inside ClosableTab
        ...

class ClosableTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.close_btn = ttk.Button(self, text="Close Tab", command=self.close_tab)
        self.close_btn.pack(anchor=SE)
    def close_tab(self):
        self.master.forget(self)
```

The `ClosableTab` class is a descendant of `ttk.Frame` from the *tkinter library*. The tabs housing data tables are instances of the `Notebook` class. But rather than the default `Frame`, They are given to a class that inherits from tkinter's `Frame` with the addition of a close button. Therefore, the user can go through different tabs filtered by their keyword and close the tabs.

#### 4.3.2. Code

```
class PathGUI:
    def __init__(self, source, name, path=False):
    ...
    @classmethod
    def load_data(cls, url, name):
    ...
    def create_table(self, filename, tabname={"Original"}):
    ...
    def filter_by_key(self):
    ...
    def filter_by_gene(self):
    ...
    def filter_by_pathology(self):
    ...
    def create_pie_chart(self, filename, category):
    ...
    def create_patient_data(self, filename, category1):
    ...
```

- `__init__()` is the constructor of the `PathGUI` class that initiates an instance of that class. The GUI is created by *tkinter library*.
- `load_data()` requests data from [Protein Atlas](https://www.proteinatlas.org/about/download), cleans up the data and converts data to a CSV file.
- `create_table()` creates a tab via the `ClosableTab` class that houses tabular data from the CSV file
- `filter_by_key()` creates a dataframe with rows that contain a keyword of interest and calls the previous function again with the new data. The user triggers this function when interacting with the **Keyword search button** and typing a valid keyword.
- `filter_by_gene()` is called by clicking **Gene search button** and typing a gene name. It calls `create_table()` with a new dataframe representing info related to that gene, as well as, a pie chart and a histogram (patient data) as described below.
- `filter_by_pathology()` operates like the previous function except the user input is looked for in the *Cancer* column of Pathology Data.
- `create_pie_chart()` shows what percentage of the gene/pathology experiments were categorized in the four cancer severity categories, and the average log-rank p-value that quantifies prognostication.
- `create_patient_data()` plots the average number of patients annotated for different staining levels


[gui-strc]: #gui-strc
