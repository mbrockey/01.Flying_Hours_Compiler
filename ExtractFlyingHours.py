import os 
import csv
import re

def main():
    ## Set main py file as dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    ###########################

    print(f"Working Directory: {dname}")

    #All info will be imported from CSVs
                    #[file number, extraction method]
    files_to_extract = [[dname+ '\\Records\\' + file_names_dict[3],file_decode_method[2]],
                        [dname+ '\\Records\\' + file_names_dict[4],file_decode_method[3]],
                        [dname+ '\\Records\\' + file_names_dict[5],file_decode_method[4]]]


    csv_data, data_dimensions = extract_csv_data_to_list(files_to_extract[0][0])
    print(data_dimensions)
    
    compiled_data = []

    #generate headers
    for i in range(0, len(column_name_data)):
        compiled_data.append([column_name_data[i]])
    

    if files_to_extract[0][1] == file_decode_method[2]: #AF3520
        # 0 = date, 5 = time(z), 9 = device/plane, 12 = serial num, 15 = duty code
        # 20 = prim, 22 = sec, 23 = instruct, 24 = eval, 26 = other, 33 = primary night
        # 36 = pri instrument, 38 = pri sim instrument
        
        start_row_number = 15
        description_phase = 1
        pit_not_complete = True
        t38_phase_start = "16 Jul 2020"
        jump_to_PIT_Rip_data_date = "07 Jul 2021"
        IP_phase_start = "07 Jul 2021"
        pattern_str1 = r'^\d{2} \w{3} \d{4}$'
        pattern_str2 = r'^\d{1} \w{3} \d{4}$'

        #while the string pattern matches above
        while bool(re.match(pattern_str1,csv_data[start_row_number][0])) or bool(re.match(pattern_str2,csv_data[start_row_number][0])) :
            
            temp_date_for_phase = csv_data[start_row_number][0]

            if temp_date_for_phase == t38_phase_start:
                description_phase = 2
            if temp_date_for_phase == IP_phase_start:
                description_phase = 4
            # Check date range for PIT
            if temp_date_for_phase == jump_to_PIT_Rip_data_date and pit_not_complete:
                #import PIT data
                pit_csv_data, pit_data_dim = extract_csv_data_to_list(files_to_extract[2][0])
                
                
                for i in range(1,pit_data_dim[1]):
                    #col 22 = Device
                    temp = pit_csv_data[i][22]
                    temp = device_name_conversion[temp]
                    compiled_data[1].append(temp)
                    temp = sim_or_aircraft[temp]
                    compiled_data[0].append(temp)
                    compiled_data[2].append("NA")
        
                    #col 2 = zulu time
                    temp = pit_csv_data[i][2]
                    temp = list(temp)
                    temp.insert(2,":")
                    temp = "".join(temp)
                    compiled_data[4].append(temp)

                    #col 12 = month
                    temp_month = pit_csv_data[i][12]
                    #col 13 = Day
                    temp_day = pit_csv_data[i][13]
                    pattern_day1 = r'^\d{2}'
                    if bool(re.match(pattern_day1,temp_day)) != True:
                        temp_day = "0" + temp_day
            
                    #col 14 = Year
                    temp_year = pit_csv_data[i][14]
                    temp_date = f"{temp_day} {temp_month} {temp_year}"
                    compiled_data[3].append(temp_date)

                    #col 3 = primary time
                    temp = pit_csv_data[i][3]
                    compiled_data[5].append(temp)

                    #fill out the rest of time as zeros
                    compiled_data[6].append(0)
                    compiled_data[7].append(0)
                    compiled_data[8].append(0)
                    compiled_data[9].append(0)
                    compiled_data[10].append(0)
                    compiled_data[11].append(0)
                    compiled_data[12].append(0)

                     #13 : "Precision Approach",
                     #14 : "Non-Precision Approach",
                     #15 : "Landing",
                     #16 : "Overhead / Pattern",
                    #col 4 = OH
                    temp = pit_csv_data[i][4]
                    
                    if temp != "":
                        compiled_data[16].append(temp)
                    else:
                        compiled_data[16].append(0)
                    #col 5 = LDG
                    temp = pit_csv_data[i][5]
                    if temp !="":
                        compiled_data[15].append(temp)
                    else:
                        compiled_data[15].append(0)

                    #col 6 = LOC
                    temp = pit_csv_data[i][6]
                    temp_sum = 0
                    if temp.isdigit():
                        temp_sum = int(temp)+temp_sum
                        
                    #col 7 = VOR
                    temp = pit_csv_data[i][7]
                    if temp.isdigit():
                        temp_sum = int(temp)+temp_sum
                    
                    #col 9 = GPS
                    temp = pit_csv_data[i][9]
                    if temp.isdigit():
                        temp_sum = int(temp)+temp_sum
                    #col 11 = ASR
                    temp = pit_csv_data[i][11]
                    if temp.isdigit():
                        temp_sum = int(temp)+temp_sum
                    compiled_data[14].append(temp_sum) ####################

                    #col 10 = PAR
                    temp = pit_csv_data[i][10]
                    temp_sum = 0
                    if temp.isdigit():
                        temp_sum = int(temp)+temp_sum
                    # #col 8 = ILS
                    temp = pit_csv_data[i][8]
                    if temp.isdigit():
                        temp_sum = int(temp)+temp_sum
                    compiled_data[13].append(temp_sum) ######################

                    for i in range(17,33):
                        compiled_data[i].append(0)
                    

                    compiled_data[33].append(home_unit_decode[3])
                    

                



                pit_not_complete = False





            #col 0 : simulator / AC
            sim_ac_test = csv_data[start_row_number][9]
            if sim_ac_test == "F37AT11":
                temp = "F37AT11" +str(csv_data[start_row_number+1][9])
            else:
                temp = sim_ac_test

            #col 1 : AC device name
            temp = device_name_conversion[temp]
            compiled_data[1].append(temp)

            #col 0 : simulator / AC
            temp = sim_or_aircraft[temp]
            compiled_data[0].append(temp)

            #col 2 : serial number
            temp = csv_data[start_row_number][12]
            compiled_data[2].append(temp)

            #col 3 : date
            temp = csv_data[start_row_number][0]
            compiled_data[3].append(temp)

            #col 4 : time
            temp = csv_data[start_row_number][5]
            compiled_data[4].append(temp)

            #col 5 : primary time
            temp = csv_data[start_row_number][20]
            if temp == "":
                temp = 0
            compiled_data[5].append(temp)

            #col 6 : secondary time
            temp = csv_data[start_row_number][22]
            if temp == "":
                temp = 0
            compiled_data[6].append(temp)

            #7:"Instructor",
            temp = csv_data[start_row_number][23]
            if temp == "":
                temp = 0
            compiled_data[7].append(temp)
               
            #8:"Evaluator",
            temp = csv_data[start_row_number][24]
            if temp == "":
                temp = 0
            compiled_data[8].append(temp)

            #9:"Other",
            temp = csv_data[start_row_number][26]
            if temp == "":
                temp = 0
            compiled_data[9].append(temp)

            #10:"Primary Night", 33
            temp = csv_data[start_row_number][33]
            if temp == "":
                temp = 0
            compiled_data[10].append(temp)

            #11: "Primary Instrument", 36
            temp = csv_data[start_row_number][36]
            if temp == "":
                temp = 0
            compiled_data[11].append(temp)

            #12: "Primary Simulated Instrument",38
            temp = csv_data[start_row_number][38]
            if temp == "":
                temp = 0
            compiled_data[12].append(temp)

            for i in range(13,33):
                compiled_data[i].append(0)
            #33
            compiled_data[33].append(home_unit_decode[description_phase])

            #increment and check for end of page
            skip_line_list = ["F37AT11","SMT001","CST006"]
            if sim_ac_test in skip_line_list:
                start_row_number = start_row_number+2
            else:
                start_row_number = start_row_number+1

            if csv_data[start_row_number][0] == "":
                start_row_number = start_row_number +23
            if start_row_number >= data_dimensions[1]:
                break
            
    else:
        print("unable to decode")

    #for i in range(0,len(compiled_data[0])):
        #print(f"{compiled_data[0][i]} {compiled_data[1][i]} {compiled_data[2][i]} {compiled_data[3][i]}" +
              #f" {compiled_data[4][i]} {compiled_data[5][i]} {compiled_data[6][i]} {compiled_data[7][i]}"+
              #f" {compiled_data[8][i]} {compiled_data[9][i]} {compiled_data[10][i]} {compiled_data[11][i]}"+
              #f" {compiled_data[12][i]} {compiled_data[13][i]} {compiled_data[14][i]} {compiled_data[15][i]}"+
              #f" {compiled_data[16][i]} {compiled_data[17][i]} {compiled_data[18][i]} {compiled_data[33][i]}")
        
    #Next load in the activity log and convert dates to zulu time
    #####################################

    activity_log_data, activity_log_dim = extract_csv_data_to_list(files_to_extract[1][0])
    
    pattern_date_to_match = r'^\d{2} \w{3} \d{4}$'
    pattern_date_to_match = r'^\d{2}:\d{2}$'
    pattern_datetime_to_match = r'^\d{2}-\w{3}-\d{4} \d{2}:\d{2}$'
    datetime_test = re.compile(pattern_datetime_to_match)
    #generate headers

    reverse_column_name_data = {v:k for k,v in column_name_data.items()} 
    for i in range(0, activity_log_dim[1]):
    
        #col 1 for date and time, col 2 for flight record, col 4 activity, col 7 for number
        activity_list = []

        if bool(datetime_test.match(activity_log_data[i][1])) and activity_log_data[i][2] != "":

            datetime = convert_to_zulu_and_format(activity_log_data[i][1])
            activity = activity_log_data[i][4]
            activity_qty = activity_log_data[i][7]
            is_one_beneath = bool(activity_log_data[i+1][1] == "" and activity_log_data[i+1][4] != "")
            compiled_data_loc = -1
            #print(f"{activity} {activity_qty} found")
            try:
            
                compiled_data_loc = reverse_column_name_data[activity_type_decode[activity_decode[activity]]]
                #print(f"{activity} {activity_qty} found")
            except:
                #print(f"{activity} {activity_qty}  not found")
                compiled_data_loc = -1

            if compiled_data_loc != -1:
                for j in range(0,len(compiled_data[0])):
                
                    c_date = compiled_data[3][j]
                    c_time = compiled_data[4][j]
                    c_datetime = f"{c_date} {c_time}"
                    t_datetime1 = str(datetime[0][0])
                    t_datetime2 = str(datetime[1][0])
                    #print(f"{c_datetime} {t_datetime1} {t_datetime2}")
                    if c_datetime == t_datetime1 or c_datetime == t_datetime2:
                        compiled_data[compiled_data_loc][j] = activity_qty
                        #print(f"Inserted {c_datetime} {activity_type_decode[activity_decode[activity]]} {compiled_data[compiled_data_loc][j]}")
                        break
            
            below_counter = i+1
            is_one_beneath = bool(activity_log_data[below_counter][1] == "" and activity_log_data[below_counter][4] != "")
            
            while is_one_beneath:
                activity = activity_log_data[below_counter][4]
                activity_qty = activity_log_data[below_counter][7]
                compiled_data_loc = -1
                try:
                    compiled_data_loc = reverse_column_name_data[activity_type_decode[activity_decode[activity]]]
                except:
                    compiled_data_loc = -1

                if compiled_data_loc != -1:
                    compiled_data[compiled_data_loc][j] = activity_qty
                below_counter = below_counter+1   
                is_one_beneath = bool(activity_log_data[below_counter][1] == "" and activity_log_data[below_counter][4] != "")
                #print(f"{i} {below_counter} {activity} {activity_qty}")
            #print(f"{i} {activity_log_data[i][1]} {activity_log_data[i][2]} {activity} {activity_qty} {is_one_beneath}")


    
    

    


    compiled_data = [list(i) for i in zip(*compiled_data)]

    out_file_name = "Brockey_Compliled_Flight_Hours.csv"
    with open(out_file_name,"w", newline= "") as f:
       writer = csv.writer(f)
    
       writer.writerows(compiled_data)      


##############################################################################


def convert_to_zulu_and_format(date_time):
    test_datetime =date_time

    #convert to zulu time and format
    test_datetime = test_datetime.split(" ")
    test_date = test_datetime[0].split("-")
    test_time = test_datetime[1].split(":")
    #convert day from str to int
    test_date[0] = int(test_date[0])

    #convert hour marker from str to int
    test_time[0] = int(test_time[0])

    #add 5 hours to convert to zulu

    test_time5 = test_time[0] + 5
    test_day1 = test_date[0]
    if test_time5 >= 24:
        test_time5 = test_time5-24
        test_day1 = test_day1 +1
    

    test_time6 = test_time[0] + 6
    test_day2 = test_date[0]
    if test_time6 >= 24:
        test_time6 = test_time5-24
        test_day2 = test_day1 +1
    
    day_pattern = r'^\d{1}$'
    test_day1 = str(test_day1)
    if bool(re.match(day_pattern,test_day1)):
        test_day1 = "0"+test_day1

    test_day2 = str(test_day2)
    if bool(re.match(day_pattern,test_day2)):
        test_day2 = "0"+test_day2
    
    converted_times = [[f"{test_day1} {test_date[1]} {test_date[2]} {str(test_time5)}:{test_time[1]}"],
                      [f"{test_day2} {test_date[1]} {test_date[2]} {str(test_time6)}:{test_time[1]}"]]
    
    return converted_times


def extract_csv_data_to_list(file_path):
    try:
        with open(file_path,"r") as f:
            csv_data = list(csv.reader(f))
            data_dimensions = [len(csv_data[0]),len(csv_data)]
            return csv_data, data_dimensions
    except:
        print("File not found!!")
        return ["error"], [0,0]
    
file_names_dict = {
    1: "01.UPT T-6 ATJ.csv",
    2: "02.UPT T-38 ATJ.csv",
    3: "04. AF 3520 Brockey Flight and Device Data.csv",
    4: "05.Activity Log.csv",
    5: "06.T-6 PIT PDF Rip.csv",
}

file_decode_method = {
    1: "ATJ",
    2: "AF3520",
    3: "ActivityLog",
    4: "PDF_rip_file"
}

flying_hours_compiled_data = [
    ["Simulator/Aircraft","Aircraft/Device Name","Serial Number","Date","Time",
     "Primary","Secondary","Instructor","Evaluator","Other","Primary Night", "Primary Instrument", "Primary Simulated Instrument"]]

device_name_conversion = {
    "T006A"    : "T-6A",
    "T038C"    : "T-38C",
    "S2C75"    : "T-6A UTD",
    "S2B48"    : "T-6A IFT",
    "S2F188"   : "T-6A OFT",
    "F37AT111" : "T-38C UTD",
    "F37AT112" : "T-38C OFT",
    "F37AT113" : "UNUSED",
    "F37AT114" : "T-38C WST",
    "T-6A"     : "T-6A",
    "UTD"      : "T-6A UTD",
    "IFT"      : "T-6A IFT",
    "OFT"      : "T-6A OFT",
    "SMT001"   : "T-1A OFT",
    "T001A"    : "T-1A",
    "CST006"   : "T-6A OFT"
 
}

sim_or_aircraft = {
    "T-6A"      : "Aircraft",
    "T-38C"     : "Aircraft",
    "T-6A UTD"   : "Simulator",
    "T-6A IFT"   : "Simulator",
    "T-6A OFT"   : "Simulator",
    "T-38C UTD"  : "Simulator",
    "T-38C OFT"  : "Simulator",
    "T-38C WST"  : "Simulator",
    "T-1A OFT"   : "Simulator",
    "T-1A"      : "Aircraft",
    "UNUSED"    : "UNUSED",

}                   

file_flying_time_decode = {
    "ATJ"          : "Primary",
    "AF3520"       : "Variable",
    "ActivityLog"  : "NA",
    "PDF_rip_file" : "Primary",
}
home_unit_decode = {
    1  : "71 FTW, 71 STUS, 8 FTS, VANCE AFB - Student Pilot",
    2  : "71 FTW, 71 STUS, 25 FTS, VANCE AFB - Student Pilot",
    3  : "12 FTW, 12 TRS, 559 FTS, RANDOLPH AFB - Student Pilot - Instructor Upgrade",
    4  : "71 FTW, 8 FTS and 71 STUS, VANCE AFB - Instructor Pilot",
}

activity_decode = {
    "ILS normal" : 1,
    "VOR approach" : 2,
    "GPS Approach" : 2,
    "Localizer approach" : 2,
    "TACAN approach" : 2,
    "VFR Patterns" : 4,
    "Local Counter 1" : 5,
    "EMER LND PATT T611XT" : 6,
    "EMER LND PATT T611" : 6,
    "LANDING T623" : 3,
    "LANDING T623XT" : 3,
    "NORM PAT T617XT" : 4,
    "NO FLAP PAT T616XT" : 7,
    "RCP LANDING T624" : 8,
    "RCP LANDING T624XT" : 8,
    "POWER ON STALLS T615" : 9,
    "POWER ON STALLS T615XT" : 9,
    "TRAFF PAT STALL T619XT" : 9,
    "TRAFF PAT STALL T619" : 9,
    "OCF T614" : 5,
    "OCF RECOVERY T614XT" : 5,
    "CONT AB FLT REC T618" : 10,
    "CONT AB FLT REC T618XT" : 10,
    "EP SIMULATOR T631" : 11,
    "EP SIMULATOR T631XT" : 11,
    "NONPREC APPR T607" : 2,
    "NONPREC APPR T607XT" : 2,
    "PRE APPROACH T608XT" : 1,
    "PREC APPROACH T608" : 1,
    "PUB APP PROC T650" : 12,
    "PUB APP PROC T650XT" : 12,
    "NIGHT RCP LAND T625XT" : 13,
    "LOW LEVEL CURR T627" : 14,
    "LOW LEVEL CURR T627XT" : 14,
    "FORM TAKEOFF T612" : 15,
    "FORM TAKEOFF T612XT" : 15,
    "STUDENT SORTIE T621" : 16,
    "STUDENT SORTIE T621XT" : 16,
    "MILITARY SIM INSTRUCTOR XMSIXT" : 17,
    "CIRCLING APPR T610XT" : 18,
    "FORMATION APPROACH XFARXT" : 19,
    "4SHIP FLIGHT LEAD XT653T" : 20,
    "ILS" : 1,
    "VOR" : 2,
    "LOC" : 2,
    "GPS" : 2,
    "PAR" : 1,
    "ASR" : 2,
    "Landings" : 3,
    "OH" : 4,
    "LDG": 3,

}

activity_type_decode = {
    1 : "Precision Approach",
    2 : "Non-Precision Approach",
    3 : "Landing",
    4 : "Overhead / Pattern",
    5 : "Spin",
    6 : "ELP",
    7 : "No-Flap Pattern",
    8 : "RCP Landing",
    9 : "Stall Series",
    10 : "Abnormal Flight Recoveries",
    11 : "EP Simulator",
    12 : "Full Procedure Approach",
    13 : "Night RCP Landing",
    14 : "Low Level",
    15 : "Formation Takeoff",
    16 : "Student Sortie",
    17 : "Mil Sim Instructor",
    18 : "Circling Approach",
    19 : "Formation Approach",
    20 : "Four Ship Flight Lead",
}

column_name_data = {
    0:"Simulator/Aircraft",
    1:"Aircraft/Device Name",
    2:"Serial Number",
    3:"Date",
    4:"Time",
    5:"Primary",
    6:"Secondary",
    7:"Instructor",
    8:"Evaluator",
    9:"Other",
    10:"Primary Night",
    11: "Primary Instrument",
    12: "Primary Simulated Instrument",
    13 : "Precision Approach",
    14 : "Non-Precision Approach",
    15 : "Landing",
    16 : "Overhead / Pattern",
    17 : "Spin",
    18 : "ELP",
    19 : "No-Flap Pattern",
    20 : "RCP Landing",
    21 : "Stall Series",
    22 : "Abnormal Flight Recoveries",
    23 : "EP Simulator",
    24 : "Full Procedure Approach",
    25 : "Night RCP Landing",
    26 : "Low Level",
    27 : "Formation Takeoff",
    28 : "Student Sortie",
    29 : "Mil Sim Instructor",
    30 : "Circling Approach",
    31 : "Formation Approach",
    32 : "Four Ship Flight Lead",
    33 : "Description"
    

}

###########
main()   ## Runs main function
###########