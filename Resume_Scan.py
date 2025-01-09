import PyPDF2
a = PyPDF2.PdfReader('/media/dhruv/Local Disk/Speech_Recognition/Dhruv_resume.pdf')
print(a.metadata)
print(len(a.pages))
str = ""
for i in range(len(a.pages)):
    str += a.pages[i].extract_text()

with open("text.txt","w", encoding="utf-8") as f:
    f.write(str)