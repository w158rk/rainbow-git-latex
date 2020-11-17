from transform import *

infile = "E:/develop/rainbow-git-latex/test/samplepaper.tex"

def main():
    doc = Document()
    doc.load(infile)
    doc.mark()
    doc.colorize()
    doc.output()

if __name__ == "__main__":
    main()