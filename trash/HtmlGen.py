
import os

def ReadSpacing(line):
        i = 0
        for c in line:
            if c == ' ':
                i += 1
            else:
                return line[i:], i
        return line, 0

def RemoveOuterSymbols(string):
    valid = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    i = 0
    while i < len(string) and string[i] not in valid:
        i += 1
    j = len(string) - 1
    while j > -1 and string[j] not in valid:
        j -= 1
    return string[i:j+1]

def WriteHead(title, f):
    head = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<title>' + title + '</title>',
        '</head>',
        '<body>',
        '<h1 id="' + title + '">' + title + '</h1>'
    ]
    for line in head:
        f.write(line + '\n')

def WriteClose(f):
    f.write('</body>\n</html>')

class Line:

    def __init__(self, string):
        self.text, self.spacing = ReadSpacing(string)
        self.text = self.text.strip()
        if self.text[-2:] == '--':
            self.type = 'h2'
            self.text = self.text[:-2]
        elif self.text[-1:] == ':':
            self.type = 'h3'
            self.text = self.text[:-1]
        elif self.text[-1:] == '-':
            self.type = 'h4'
            self.text = self.text[:-1]
        else:
            self.type = 'p'

    def ToHtmlElement(self, references, localrefs):
        if self.text == '':
            return '<p style="margin:0; margin-bottom:0; padding-top:0;"><br></p>'
        out = '<' + self.type + ' style="margin:0; margin-bottom:0; padding-top:0;'
        if self.spacing:
            out += 'margin-left: ' + str(self.spacing * 10) + 'px"'
        else:
            out += '"'
        if 'h' in self.type:
            sym = RemoveOuterSymbols(self.text)
            out += ' id="' + sym + '">' + self.text
        else:
            out += '>'
            tokens = self.text.split()
            for token in tokens:
                sym = RemoveOuterSymbols(token)
                if sym in localrefs:
                    out += '<a href="#' + sym + '">' + token + '</a>'
                elif sym in references:
                    if '.' in sym:
                        t, h = tuple(sym.split('.'))
                        ref = t + '.html#' + h
                        out += '<a href="' + ref + '">' + token + '</a>'
                    else:
                        out += '<a href="' + sym + '.html#' + sym + '">' + token + '</a>'
                else:
                    out += token
                out += ' '
        return out + '</' + self.type + '>'
            
class Document:

    def __init__(self, text):
        self.text = text
        self.localreferences = set()
        self.title = None
        self.lines = None
        self.Init()
        self.filename = self.title + '.html'

    def Init(self):
        self.lines = [Line(line) for line in self.text.split('\n')]
        self.title = self.lines[0].text
        self.ScanReferences()

    def ScanReferences(self):
        i = 1
        while i < len(self.lines):
            line = self.lines[i]
            if 'h' in line.type and len(line.text.split()) == 1:
                self.localreferences.add(line.text)
            i += 1

    def References(self):
        for ref in self.localreferences:
            yield self.title + '.' + ref
        yield self.title

    def WriteHtml(self, references=None, outpath=None):
        if references is None:
            references = self.localreferences
        if outpath is None:
            outpath = os.getcwd()
        outfile = os.path.join(outpath, self.title + '.html')
        with open(outfile, 'w') as f:
            WriteHead(self.title, f)
            i = 1
            while i < len(self.lines):
                line = self.lines[i]
                htmlel = line.ToHtmlElement(references, self.localreferences)
                f.write(htmlel + '\n')
                i += 1
            WriteClose(f)    

class Documentation:

    def __init__(self):
        self.references = set()
        self.documents = []

    def DocumentDirectory(self, path=None, outpath=None):
        if path is None:
            path = os.getcwd()
        if outpath is None:
            outpath = os.getcwd()
        fileTexts = []
        for root, subdirs, files in os.walk(path):
            for file in files:
                if file[-5:] == '.jdoc':
                    filepath = os.path.join(root, file)
                    with open(filepath) as f:
                        text = f.read()
                        fileTexts.append(text)
        self.Document(fileTexts, outpath)
        self.Save(outpath)

    def Document(self, texts, outpath=None):
        if outpath is None:
            outpath = os.getcwd()
        for text in texts:
            self.Add(text)
        self.Save(outpath)

    def Add(self, text):
        newdoc = Document(text)
        self.documents.append(newdoc)
        for ref in newdoc.References():
            self.references.add(ref)

    def Save(self, outpath):
        if not os.path.isdir(outpath):
            os.makedirs(outpath)
        for doc in self.documents:
            doc.WriteHtml(self.references, outpath=outpath)

if __name__ == "__main__":
    d = Documentation()
    d.DocumentDirectory(outpath='Docs')


