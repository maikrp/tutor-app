import PyPDF2

PDF_FILE = "ajustes.pdf"  # nombre de tu PDF en la carpeta actual

def debug_pdf(pdf_path: str):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num, page in enumerate(reader.pages, start=1):
            txt = page.extract_text() or ""
            lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
            
            print(f"\n=== Página {page_num} ({len(lines)} líneas) ===")
            for i, ln in enumerate(lines):
                print(f"{i}: {ln}")
            print("=" * 50)

if __name__ == "__main__":
    debug_pdf(PDF_FILE)
