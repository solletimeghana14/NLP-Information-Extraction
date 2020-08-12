# NLP-Information-Extraction
Information Extraction application using NLP features and techniques
Implemented in Python


Set of information templates
Template #1:
BUY(Buyer, Item, Price, Quantity, Source)

Template #2:
WORK(Person, Organization, Position, Location)

Template #3:
PART(Location, Location)

Input:
• Text Document 
Output:
• All instances of the above three templates found in the input text document

Example #1:
Document: Amazon_com.txt
Sentence(s): In 2017, Amazon acquired Whole Foods Market for US$13.4 billion, which vastly increased Amazon's presence as a brick- and-mortar retailer.
Extracted Template: BUY(“Amazon”, “Whole Foods Market”, “US$13.7 billion”, “”, “”)

Example #2: 
Document: AppleInc.txt
Sentence(s): Steven Paul Jobs (; February 24, 1955 – October 5, 2011) was an American business magnate and investor. He was the chairman, chief executive officer (CEO), and co-founder of Apple Inc.; chairman and majority shareholder of Pixar; a member of The Walt Disney Company's board of directors following its acquisition of Pixar; and the founder, chairman, and CEO of NeXT.
Extracted Template: WORK(“Steven Paul Jobs”, “Apple Inc.”, “chairman ; chief executive officer (CEO); co-founder”, “”)
Extracted Template: WORK(“Steven Paul Jobs”, “Pixar”, “chairman”, “”)
Extracted Template: WORK(“Steven Paul Jobs”, “The Walt Disney Company”, “board member”, “”)
Extracted Template: WORK(“Steven Paul Jobs”, “NeXT”, “founder; chairman ; CEO”, “”)

Example #3:
Document: Richardson_Texas.txt
Sentence(s): Richardson is a principal city in Dallas and Collin counties in the U.S. state of Texas.
Extracted Template: PART(“Richardson”, “Dallas”) Extracted Template: PART(“Richardson”, “Collin counties”)
Extracted Template: PART(“Richardson”, “U.S. state of Texas | Texas”)
Extracted Template: PART(“Texas”, “U.S.”)

Steps to execute Python Files:

for BUY_template(additonal optional argument for neuralcoref)
python BUY_template.py <text_file_name>
with coref
python BUY_template.py <text_file_name> c

for WORK_template(additonal optional argument for neuralcoref)
python WORK_template.py <text_file_name>
with coref
python WORK_template.py <text_file_name> c

for PART_template(this uses networkx library)
(takes directory path of all wikipedia articles and generates results in JSON directory which needs to be created)
python PART_template <directory_folder>

