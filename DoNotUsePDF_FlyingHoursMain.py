
from pdfminer.high_level import extract_text, extract_pages
import os 
import re

def main():
    ## Set main py file as dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    ###########################
    
    file_number = 3

    dict_name = f"ATJ{file_number}"
    dict_page_loc = f"ATJ{file_number}_FJS"
    PDF_name = dict_of_files[dict_name]
    pages_to_rip = dict_of_section_Locations[dict_page_loc]

    file_location = dname + "/Records/" + PDF_name
    PDF_file = load_pdf_text_into_list(file_location,pages_to_rip)
   

    ATJ_data = []
    dely_input_for_these_names = [ '','Status','Date','NG','U','F','G','E','Instructor']
    target_col_name =  'Flight'
    section_name_to_find = "Full Jacket Summary"
    ATJ_data.append(extract_data_from_FJS_section(PDF_file,section_name_to_find,target_col_name,dely_input_for_these_names))

    dely_input_for_these_names = [ '','Status','Date','NG','U','F','G','E','Instructor']
    target_col_name =  'Type'
    section_name_to_find = "Full Jacket Summary"
    ATJ_data.append(extract_data_from_FJS_section(PDF_file,section_name_to_find,target_col_name,dely_input_for_these_names))
    



    PDF_file = load_pdf_text_into_list(file_location,[5,170])
    section_name_to_find = "Record Of Training"
    target_col_name =  'DUR'
    ATJ_data = extract_data_from_ROT_section(PDF_file,ATJ_data,section_name_to_find,target_col_name)

    for i in range(0, len(ATJ_data[0])):
        print(f"{ATJ_data[0][i]}, {ATJ_data[1][i]}, {ATJ_data[2][i]}, {ATJ_data[3][i]}, {ATJ_data[4][i]}")


def extract_data_from_ROT_section(PDF_file,ATJ_data,section_name_to_find,target_col_name):
    Section_Name_Summary =[]

    
    for i in range(1,len(PDF_file)):
        if PDF_file[i].find(section_name_to_find)>0:
            Section_Name_Summary.append(PDF_file[i].splitlines())

    date_data = ["NA"]*len(ATJ_data[0])
    dur_data = ["NA"]*len(ATJ_data[0])
    inst_data = ["NA"]*len(ATJ_data[0])

    pattern_str = r'^\d{2}-\w{3}-\d{4}$'

    #check every page
    for i in range(0,len(Section_Name_Summary)):
        date_temp = "NA"
        #extract a date with every page
        for j in range(0,len(Section_Name_Summary[i])):
            test_str = Section_Name_Summary[i][j]
            if bool(re.match(pattern_str, test_str)):
                date_temp = test_str
                
        
        #extract a evetn name and time:
        
        try: 
            loc = Section_Name_Summary[i].index(target_col_name)
            event_name = Section_Name_Summary[i][loc-2]
            dur_temp = Section_Name_Summary[i][loc+2]
            loc = Section_Name_Summary[i].index("INSTRUCTOR'S NAME")
            inst_temp = Section_Name_Summary[i][loc+2]
            if inst_temp == "FLIGHT":
                num = len(Section_Name_Summary[i])
                inst_temp = Section_Name_Summary[i][num - 3]
            if inst_temp == "All times unless otherwise specified are reported in (UTC-05:00) Central Time (US & Canada)":
                inst_temp = "NA"  
            loc = ATJ_data[0].index(event_name)
            date_data[loc] = date_temp
            dur_data[loc]  = dur_temp
            inst_data[loc] = inst_temp
        except:
            try:
                loc = Section_Name_Summary[i].index(target_col_name)
                event_name = Section_Name_Summary[i][loc+10]
                dur_temp = Section_Name_Summary[i][loc+8]
                loc = Section_Name_Summary[i].index("INSTRUCTOR'S NAME")
                inst_temp = Section_Name_Summary[i][loc+2]
                
                if inst_temp == "FLIGHT":
                    num = len(Section_Name_Summary[i])
                    inst_temp = Section_Name_Summary[i][num - 3]
                if inst_temp == "All times unless otherwise specified are reported in (UTC-05:00) Central Time (US & Canada)":
                    inst_temp = "NA" 
                
                loc = ATJ_data[0].index(event_name)
                date_data[loc] = date_temp
                dur_data[loc]  = dur_temp
                inst_data[loc] = inst_temp

                #print(f"problem on page {i}")
                #print(Section_Name_Summary[i])
            except:                
                pass

    ATJ_data.append(date_data)
    ATJ_data.append(dur_data)
    ATJ_data.append(inst_data)

    return ATJ_data

     


dict_of_files = {

    "ATJ3": "03. 19FEB21 - 21JUN21 PIT T-6A Aviation Training Jacket Report.pdf"

}

dict_of_section_Locations = {

    "ATJ3_FJS": [165,175],

}

def extract_data_from_FJS_section(PDF_file,section_name_to_find,target_col_name,dely_input_for_these_names):
    
    Section_Name_Summary =[]

    for i in range(1,len(PDF_file)):
        if PDF_file[i].find(section_name_to_find)>0:
            Section_Name_Summary.append(PDF_file[i].splitlines())
    
    #extract event names and put into list
    data_from_col = []
    for i in range(0,len(Section_Name_Summary)):
        loc = Section_Name_Summary[i].index(target_col_name)
        inc = 1
        current_location = loc + inc

        #find first event name, skip all col headers in dely_input_for_these_names
        while Section_Name_Summary[i][current_location] in dely_input_for_these_names:
            current_location = current_location +1

        while (Section_Name_Summary[i][current_location] in dely_input_for_these_names) == False:
            data_from_col.append(Section_Name_Summary[i][current_location])
            current_location = current_location + 1
        
    return data_from_col



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