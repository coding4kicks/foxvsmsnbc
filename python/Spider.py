"""	Web Crawler - an icky spider that crawls the user's site.
		1) Only searches URLs with the user provided host name
		2) Passes the page back to a concurrent process to index the site
		3) Performs a Breadth First Search (BFS) - not BFFs
		4) Has a max pages, indicates where to stop, so it't doesn't go crazy and index the whole web.
		5) Pulls pages to search from the datastructure to which the parser adds them (need a buffer)
"""
import urllib
import cPickle
from Parser import *

class Spider:
    #############################
    ## CONSTANTS AND VARIABLES
    ###############################

    ## URI or URL of the site
    site_url = ''

    ## List of saved content files
    file_list = []

    ## Queue of links to follow
    link_queue = []

    ## List of processed links
    links_processed = []

    ## Max pages to search
    MAX = 10

    ## the current document number
    doc_num = 1

    ## the current document name
    doc_name = "doc1"

    # A dictionary of links
    dic_links = {}

    #############################
    ## METHODS: PROCEDURES AND FUNCTIONS
    ###############################

    """ Initialize Web Crawler - Constructor
            Arguments 	- Site_Link (URI)
            Returns		- Web Crawler
    """
    def __init__(self, site):

            self.site_url = site

    """ Start Web Crawler
            Arguments 	- Web Crawler
            Returns		- HTML Documents
    """
    def run(self):

        ## try to get the initial page
        try:

            ## open and read the initial page's data
            f = urllib.urlopen(self.site_url)
            data = f.read()
            f.close

            ## create a parser and run it on the initial page
            parser = Parser(self.site_url)
            parser.run(data, self.doc_name)

            ## get the initial links
            self.link_queue = parser.get_links()

            ## add url to processed list
            self.links_processed += [self.site_url]

            ## add to link dictionary
            self.dic_links[self.doc_name] = self.site_url

            ## increment the document number and name
            self.doc_num = self.doc_num + 1
            self.doc_name = "doc" + str(self.doc_num)

#            print("Print the Links: Test")
#            i = 0
#            for link in self.link_queue:
#                print(link)
#                i = i + 1
#                if i == 10:
#                    break
        except:
            print("Problem with the initial page")

        ## while start is less than max, index more pages
        counter = 0
        while counter < self.MAX:

            ## get the next link
            link = self.link_queue.pop(0)

            if link not in self.links_processed:

                ## try to process the page
                try:

                    ## open and read in the page
                    f = urllib.urlopen(link)
                    data = f.read()
                    f.close

                    ## create a parser and run it on the initial page
                    parser.run(data, self.doc_name)

                    ## get additional links
                    self.link_queue += parser.get_links()

                    ## add url to processed list
                    self.links_processed += [link]

                    ## increment the document number and name
                    self.doc_num = self.doc_num + 1
                    self.doc_name = "doc" + str(self.doc_num)

                ## problem processing page
                except:

                        print("Problem processing: " + link)
                        continue

                ## increment counter
                counter = counter + 1
                print(counter)
                
                ## add to link dictionary
                self.dic_links[self.doc_name] = self.site_url

        ## get the file list
        self.file_list = parser.get_file_list()

        ## save the dictionary of links as an object for later reference
        try:

            ## save the index ***** LATER REPLACE index with SITE-NAME *****
            outfile = open("Files/Links/link_dic.lk", "wb")
            cPickle.dump(self.dic_links, outfile, 2)

        except:

            ## an error occured - probably opening a file
            print("Problem Pickling the Links")

        finally:

            ## release the files
            outfile.close()

    """ Return File List
            Arguments 	-
            Returns	- File list
    """
    def get_file_list(self):

        return self.file_list

    """ Stop Web Crawler
            Arguments 	- HTML Document
            Returns		- Event Listerner
    """

    """ Return Documents
            Arguments 	- HTML Document
            Returns		- HTML Document
    """

    """ Switch Page
            Arguments 	- None
            Returns		- Query String (Obejct or String)
    """

    """ Queue Links
            Arguments 	- Document, Host Name
            Returns		- None: Adds Page to Queue (List)
    """

    """ Check Depth
            Arguments 	- Document, Host Name
            Returns		- None: Adds Page to Queue (List)
    """

    #############################
    ## HELPER METHODS
    ###############################