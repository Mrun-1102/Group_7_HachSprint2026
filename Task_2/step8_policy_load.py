from pypdf import PdfReader

reader = PdfReader("data/Helix_Pro_Policy_v2.pdf")
print("Total pages:", len(reader.pages))
print("\nSample text:")
print(reader.pages[0].extract_text()[:400])
