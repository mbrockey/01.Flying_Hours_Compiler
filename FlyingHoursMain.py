
from pdfminer.high_level import extract_text, extract_pages
import os 


def main():
    ## Set main py file as dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    ###########################


    PDF1_name = "01. 05DEC19 - 06JUL20 UPT T-6A Aviation Training Jacket Report.pdf"
    file_location = dname + "/Records/" + PDF1_name

    start_page = 158
    end_page = 159

    PDF1_file = load_pdf_text_into_list(file_location)
    
    find_text = "Full Jacket Summary"
    find_text_loc =[]

    for i in range(0,len(PDF1_file)):
        if PDF1_file[i].find(find_text)>0:
            find_text_loc.append(i)
    
    print(find_text_loc)

        



def determine_end_of_PDF(current_page, loc_of_file,page_timeout_counter):
    if current_page[1] != -1:
        if current_page[0] > current_page[1]:
            print(f"\nEnd of selected pages reached.")
            return False
    for i in range(0, page_timeout_counter-1):
        test_text = extract_text(loc_of_file, page_numbers=[current_page[0]+i])    
        if test_text != "":
            return True
    print(f"\nEnd of document reached.")
    return False 


#load pdf into a list
def load_pdf_text_into_list(file_location, page_counter =[0,-1], end_of_document_counter = 5):
    loop_exit_var = True
    PDF_document = []

    print("Loading PDF:\nPage number: ", end ="")
    while determine_end_of_PDF(page_counter,file_location,end_of_document_counter) and loop_exit_var:

        PDF_document.append(extract_text(file_location, page_numbers=[page_counter[0]]))
        print(f"{page_counter[0]} ", end = "")
        page_counter[0] = page_counter[0] +1

    print(F"Loading File:\n {file_location} \nSuccesful!")
    return PDF_document

    
###########
main()   ## Runs main function
###########