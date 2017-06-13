import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import codecs

def extract_layout_by_page(pdf_path):
    laparams = LAParams()
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    layouts = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layouts.append(device.get_result())

    return layouts

def extract_table(path):
    pages = extract_layout_by_page(path)
    f = codecs.open("output.csv","w","utf-8")
    for page in range(0,len(pages)):
        texts = [t for t in pages[page] if isinstance(t,pdfminer.layout.LTTextBoxHorizontal)]
        rects = [r for r in pages[page] if isinstance(r,pdfminer.layout.LTRect)]
        rows = set([(int(t.y0) - (int(t.y0) % 5)) for t in texts])
        columns = set([(int(rl.x0) - (int(rl.x0) % 5) ,int(rl.x1) - (int(rl.x1) % 5) ) for rl in rects if rl.height == 2.0])
        cleaned_cols = []
        for c in columns:
            width = c[1]-c[0]
            bigger_column = [bc for bc in columns if (bc[0] <= c[0] <= bc[1] and (bc[1]-bc[0])>width)]
            if len(bigger_column)==0:
                cleaned_cols.append(c)
        if len(cleaned_cols)>0:
            for c in sorted(cleaned_cols,key=lambda c: c[0]):
                print str(page) + "," + str(c[0]) + "," + str(c[1])
        for l in sorted(rows,reverse=True):
            row=[]
            objs = sorted([t for t in texts if (int(t.y0) - (int(t.y0) % 5)) == l],key=lambda txt: txt.x0)
            for c in sorted(cleaned_cols,key=lambda h: h[0]):
                cells = [cell for cell in objs if c[0] <= int(cell.x0) <= c[1]]
                row.append('""' if len(cells) == 0 else '"' + cells[0].get_text().replace('\n',' ').rstrip() + '"')
            if len([c for c in row if c!='""'])==0:
                pass
            else:
                f.write(str(page) + ',' + str(l) + ',' + ','.join(row) + '\n')
    f.close()

extract_table(r"bax.pdf")
