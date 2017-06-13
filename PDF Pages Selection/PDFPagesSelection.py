from PyPDF2 import PdfFileWriter, PdfFileReader

def selectPages(path):
    inputfile = PdfFileReader(path, 'rb')
    outputfile = PdfFileWriter()
    pageCodes = ['C2.1','VOL2.1','VOL2.2','C2.2','VOL3','C3','VOL5.10','C5.10','VOL6','C6']
    for pagenum in xrange(inputfile.getNumPages()):
        page = inputfile.getPage(pagenum).extractText()

        if pagenum == 0:
            outputfile.addPage(inputfile.getPage(pagenum))
        for pageCode in pageCodes:
            if pageCode in page:
                outputfile.addPage(inputfile.getPage(pagenum))

    with open('new'+path+'.pdf', 'wb') as f:
       outputfile.write(f)

if __name__ == '__main__':
    selectPages('janss.pdf')
    selectPages('bax.pdf')
