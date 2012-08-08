"""	Parser - recieves a document and does its thing.
		1) Called by the spider
                2) Saves the content to a file
                3) Provides the spider with links to follow
		2) Separates the following into datastructures (as of now, only links and content)
			=> Links (file type: .lnk)
			=> Content (file type: .cnt)
			=> Meta (file type: .mta)
			=> Other HTML elements may be added
"""

#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

class Parser:

    ############################
    # CONSTANTS AND VARIABLES
    ##############################

    # Host url received from the spider
    host_url = ''

    # List of links
    link_list = []

    ## List of saved content files
    file_list = []

    # Array of meta key words

    ############################
    # METHODS: PROCEDURES AND FUNCTIONS
    ##############################

    """ Initialize Parser	- Constructor
            Arguments 	- A Spider
            Returns		- A Parser
    """
    def __init__(self, host):

        self.host_url = host

    """ Start Parser
            Arguments 	- A Parser (self)
            Returns	- A list of links, content words, document pointers
    """
    def run(self, doc, doc_name):

        ## try to process the file
        try:

            ## set up the parser
            out = BeautifulSoup(doc, "html5lib")
            output = ''
            links = ''

            ## find content for specified tags
            for tag in out.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
                output += (tag.text + " ")

            ## find all the links
            for link in out.find_all('a'):
                links += str(link.get('href')) + " \n"

            ## process the links so are absolute urls
            self.link_list = process_links(links, self.host_url)
            
            ## process the links so can be output to a file
            link_output = ''
            for link in self.link_list:
                link_output += link + '\n'

            ## save the content information for the page
            outfile_name = "Files/Content/" + doc_name + ".cnt"
            data_out = output.encode('utf-8')
            outfile = open(outfile_name, "w")
            outfile.write(data_out)

            ## update the file list
            self.file_list += [outfile_name]

            ## save the link information for the page
            linkfile_name = "Files/Links/" + doc_name + ".lk"
            linkfile = open(linkfile_name, "w")
            linkfile.write(link_output)

        except IOError:

            ## error opening the file
            print("Problem opening page file: " + file_name)

        except:

            ## another error occured
            print("Problem Parsing the Data")

        finally:

            ## release the files
            outfile.close()
            linkfile.close()

    """ Return Links
            Arguments 	-
            Returns	- Link file
    """
    def get_links(self):

        return self.link_list

    """ Return File List
            Arguments 	-
            Returns	- File list
    """
    def get_file_list(self):

        return self.file_list

""" Return Links
        Arguments - host name, link list
        Returns	- link list with absolute urls
"""
def process_links(links, host):

    ## list to hold the new links
    link_list = []

    ## determine the site name from the host
    ## remove www, https://, http://, .com, .org
    temp1 = host.replace("www.", "")
    temp2 = temp1.replace("https://", "")
    temp3 = temp2.replace("http://", "")
    temp4 = temp3.replace(".com", "")
    site = temp4.replace(".org", "")

    ## split the output into a list
    list = links.split();

    ## process all the links
    for link in list:
        
        ## if absolute url
        if link[0:3] == "http":

            ## with site name add to list
            if site in link:

                link_list += [link]

            ## if absolute without site name skip

        ## if relative add host
        if (link[0] == '/' and len(link) > 1):

            link_abs = host + link
            link_list += [link_abs]

        ## else skip, junk

    return link_list

""" Simple HTML Parser
        Arguments 	-
        Returns	- None: stops (Procedure: side effect)
"""
# NOT CURRENTLY USING - HTMLParser in Python 2.7.2 is too strict
#
#class SimpleHTMLParser(HTMLParser):
#
#    ## only read if certain requirements are met
#    read_data = False
#
#    ## a list to hold the relevent data
#    output_list = []
#
#    # if a particular tag, start reading in data afterwards
#    def handle_starttag(self, tag, attrs):
#        print("start")
#        if (tag.lower() == ('p')) or (tag.lower() == ('h1')) \
#            or (tag.lower() == ('h2')) or (tag.lower() == ('h3')) \
#            or (tag.lower() == ('h4')) or (tag.lower() == ('h5')) \
#            or (tag.lower() == ('h6')):
#
#               read_data = True
#
#    def handle_endtag(self, tag):
#        print("end")
#        if (tag.lower() == ('p')) or (tag.lower() == ('h1')) \
#            or (tag.lower() == ('h2')) or (tag.lower() == ('h3')) \
#            or (tag.lower() == ('h4')) or (tag.lower() == ('h5')) \
#            or (tag.lower() == ('h6')):
#
#               read_data = False
#
#    def handle_data(self, data):
#        print(data)
#        if self.read_data:
#            print(data)
#            output_list += data
#
#    def get_output(self):
#
#        return output_list


""" Return Links
        Arguments 	- A Queue of Links (Global)
        Returns	- Links
"""

""" Return Content
        Arguments 	- Content Word List and Document Pointer (Global)
        Returns	- Word List and Document ID
"""

""" Return Meta Data
        Arguments 	- List of Meta Data
        Returns	- Meta Data
"""
""" Stop Parser
        Arguments 	- A Parser (self)
        Returns	- None: stops (Procedure: side effect)
"""
############################
# HELPER METHODS
##############################
