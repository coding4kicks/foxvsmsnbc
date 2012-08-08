## Spider_Test.py
## unit test for spider

from Spider import *

def test():

    #try:
    	print("Create Link")
        link = "http://www.cnn.com"
        print("Initialize the Spider")
        sdr = Spider(link)
        print("Run Spider")
        sdr.run()
        print("Check the file list")
        file_list = sdr.get_file_list()
        for file in file_list:
            print(file)

    #except:
     #   print("Error during crawl test.")


if __name__ == "__main__":

    test()