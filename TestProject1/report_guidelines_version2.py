import os
import datetime
import subprocess
import sys
from PyPDF2 import PdfReader, PdfWriter

# Get the current date
date = datetime.date.today().strftime("%Y-%m-%d")

# Get your last name and initial
first_name = "John"
last_name = "Doe"
initial = "J"

# Get the project number (you'll need to replace this with the actual project number)
project_number = "1"

# Get the input and output file names
input_file = "project1.ipynb"
output_file = f"{last_name}_{initial}_HW{project_number}.pdf"

# Check if the input file exists
if not os.path.exists(input_file):
    raise FileNotFoundError(f"Input file {input_file} not found.")

# Generate the PDF file using jupyter nbconvert
subprocess.run(["jupyter", "nbconvert", "--to", "pdf", input_file])

# Check if the generated PDF file exists
generated_pdf = f"{input_file.replace('.ipynb', '')}.pdf"
if not os.path.exists(generated_pdf):
    raise FileNotFoundError(f"Generated PDF file {generated_pdf} not found.")

# Delete the existing output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

# Rename the PDF file
os.rename(generated_pdf, output_file)


# Define a custom LaTeX template
latex_template = r"""
\documentclass{{article}}
\usepackage{{fancyhdr}}
\pagestyle{{fancy}}
\renewcommand{{\headrulewidth}}{{0pt}}
\renewcommand{{\footrulewidth}}{{0pt}}

\begin{{document}}

\begin{{titlepage}}
    \centering
    \vspace*{{2cm}}
    \Huge{{\textbf{{Project Number {project_number}}}}} \\
    \vspace*{{1.5cm}}
    \normalsize{{\textbf{{Author: {first_name} {last_name}}}}} \\
    \vspace*{{0.5cm}}
    \normalsize{{\textbf{{Date of Submission: {{\today}}}}}}
\end{{titlepage}}

\end{{document}}
"""

data = {
    'project_number': project_number,
    'first_name': first_name,
    'last_name': last_name
}

latex_template = latex_template.format(**data)

'''
#\input{notebook.tex}

#\begin{titlepage}
#    \centering
#    \vspace*{2cm}
#    \Huge{\textbf{Title Page}}
#    \vspace*{1cm}
#    \normalsize{\textbf{Author}}
#    \vspace*{2cm}
#    \normalsize{\textbf{Date}}
#\end{titlepage}

'''


# Write the LaTeX template to a file
with open("template.tex", "w") as f:
    f.write(latex_template)

# Generate the LaTeX file for the notebook
subprocess.run(["jupyter", "nbconvert", "--to", "latex", input_file])

# Generate the title page PDF file
#subprocess.run(["pdflatex", "titlepage.tex"])
subprocess.run(["pdflatex", "template.tex"])

# Check if the title page PDF file exists
#titlepage_pdf = "titlepage.pdf"
#if not os.path.exists(titlepage_pdf):
#    raise FileNotFoundError(f"Title page PDF file {titlepage_pdf} not found.")

template_pdf = "template.pdf"
if not os.path.exists(template_pdf):
    raise FileNotFoundError(f"Title page PDF file {template_pdf} not found.")


# Combine the title page and report PDF files using PyPDF2
pdf1 = PdfReader(template_pdf)
pdf2 = PdfReader(output_file)

pdf_writer = PdfWriter()

for page in pdf1.pages:
    pdf_writer.add_page(page)

for page in pdf2.pages:
    pdf_writer.add_page(page)

with open(output_file, "wb") as fh:
    pdf_writer.write(fh)

