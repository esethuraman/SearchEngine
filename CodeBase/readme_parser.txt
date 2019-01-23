------------------------------------------------------------------------------------------------------------------
PARSER
-------------------------------------------------------------------------------------------------------------------

PREREQUISITES:
	1) This code uses two modules that has to be installed
       - beautiful soup 
          > pip install beautifulsoup4

    2) Task1 needs a folder called "Source" where all the html documents are present
    3) Another folder called "Destination" is needed where the tokens are stored in file
        names as the document ids

    [Note]: the source and destination path names can be changed by editing lines 10 and 11 of this file

HOW TO RUN?
	- Two command line arguments are needed for punctuation option and casefold option
	  If the entered input is less than 0, then the option is disabled. otherwise enabled

    - TEMPLATE FOR RUNNING:
    	  > python parser.py Integer Integer
    
    - SYNTAX:
    	  > python parser.py $PUNCTUATION_OPTION $CASEFOLD_OPTION

    - EXAMPLE:
    	  > python parser.py 1 0
    	 This would run the code with punctuation option enabled and casefold option disabled

INTERPRETING THE OUTPUT:
   - The parsed documents will be present in the destination folder - "Destination"
   - The file names are the document ids of the original file 
