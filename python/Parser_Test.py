## Parser_Test.py
## unit test for parser

from Parser import *

def test():

    #try:
    	print("Open File")
        file_name = "Files/Pages/cnn.html"
        infile = open( file_name, "r")
        doc = infile.read()
        infile.close()
        print("Initialize Parser")
        psr = Parser("http://www.cnn.com")
        print("Run Parser")
        psr.run(doc, "cnn")
        print("Get the Links")
        links = psr.get_links()
        print("Print the Links")
        i = 0
        for link in links:
            print(link)
            i = i + 1
            if i == 10:
                break
        print("Check the file list")
        file_list = psr.get_file_list()
        for file in file_list:
            print(file)

    #except:
        #print("Error during parsing test.")


if __name__ == "__main__":

    test()