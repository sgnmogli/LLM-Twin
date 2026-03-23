import sys
import subprocess

try:
    import PyPDF2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

pdf_path = sys.argv[1]
with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    print(f"Total pages: {len(reader.pages)}")

    # Extract first 20 pages to get TOC
    toc_text = ""
    for i in range(min(30, len(reader.pages))):
        toc_text += reader.pages[i].extract_text() + "\n"

with open("toc.txt", "w", encoding="utf-8") as f:
    f.write(toc_text)
print("TOC written to toc.txt")
