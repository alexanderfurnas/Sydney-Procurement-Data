import os
import csv
import urllib2
import urllib
import json
import subprocess
from time import sleep
import glob

def write_data(data, outputpath): #This is used for two different writing functions. Make sure to change the file name and fieldnames
    ordered_fieldnames =  ["Title",	"Contract Type","Tender Number","Winning Bidder","Winning Bidder Address",	"Related affiliate corp","Date Effective","Duration",	"Contract Description",	"Estimated Value",	"Payment Variation Provisions",	"Renegotiation Provisions",	"Proccess/ Assessment Description"]

    if os.path.exists(outputpath):
        with open(outputpath, "a") as datatest:
    #csv.register_dialect("custom", delimiter="", skipinitialspace=True)
            writer = csv.writer(datatest, dialect="excel")
            try:
                writer.writerow(data)
            except UnicodeEncodeError:
                print userdataset
                pass
    else:
        with open(outputpath, "w") as datatest:
        #csv.register_dialect("custom", delimiter="", skipinitialspace=True)
            csv.DictWriter(datatest, dialect="excel", fieldnames=ordered_fieldnames).writeheader()
            writer = csv.writer(datatest, dialect="excel")
            try:
                writer.writerow(data)
            except UnicodeEncodeError:
                print i
                pass
   
if __name__=='__main__':
    input_dir = "/Users/sunlight/Documents/Sydney-proc/Sydney Contract PDFs"
    output_path = "/Users/sunlight/Documents/Sydney-proc/Sydney_Contracts_2013_Bulk.csv"
    
    for filename in os.listdir(input_dir):
        filepath = input_dir + "/" + filename
        subprocess.call(['pdftotext','-nopgbrk',"-layout", filepath]) 
    os.chdir(input_dir)
    for files in glob.glob("*.txt"):
        pdf_filepath = input_dir + "/" + files
        f = open(pdf_filepath, 'rU')
        content = f.readlines()
        contract_type = content[0]
        if "2" in contract_type:
            contract_type_dum = 2
        elif "1" in contract_type:
            contract_type_dum = 1
        else:
            contract_type_dum = "N/A"
        useless = ["2","","1"]
        all_lines = []
        for line in content:
            all_lines.append(line.strip())
    
        lines = [line for line in all_lines if line not in useless]
        doc_length=len(lines)
        field_dict = {"one":{"begin":0, "end":0}, "two":{"begin":0, "end":0}, "three":{"begin":0, "end":0}, "four":{"begin":0, "end":0}, "five":{"begin":0, "end":0},"six":{"begin":0, "end":0},"seven":{"begin":0, "end":0},"eight":{"begin":0, "end":0},"nine":{"begin":0, "end":0},"ten":{"begin":0, "end":0},"eleven":{"begin":0, "end":0},"twelve":{"begin":0, "end":0},"thirteen":{"begin":0, "end":0},"fourteen":{"begin":0, "end":0},"fifteen":{"begin":0, "end":0},"sixteen": {"begin":0, "end":0}, "seventeen":{"begin":0, "end":0}, "eighteen":{"begin":0, "end":0}}
        line_num=0
        print lines
        for line in lines:
            if "1. Tender Number:" in line:
                field_dict["one"]["begin"]=line_num
            elif "Name and business address" in line:
                field_dict["one"]["end"]=line_num
                field_dict["two"]["begin"]=line_num
            elif "3. Particulars of any related" in line:    
                field_dict["two"]["end"]=line_num
            elif "benefit under the contract" in line:    
                field_dict["three"]["begin"]=line_num
            elif "4. Date on which the contract" in line:    
                field_dict["three"]["end"]=line_num
                field_dict["four"]["begin"]=line_num
            elif "5. Particulars of the project" in line:
                field_dict["four"]["end"]=line_num
            elif "leased under the contract:" in line:    
                field_dict["five"]["begin"]=line_num
            elif "6. Estimated amount payable" in line:    
                field_dict["five"]["end"]=line_num
                field_dict["six"]["begin"]=line_num
            elif "7. Description of any provisions" in line:    
                field_dict["six"]["end"]=line_num
            elif "may be varied:" in line:    
                field_dict["seven"]["begin"]=line_num
            elif "8. Description of any provision" in line:    
                field_dict["seven"]["end"]=line_num
                field_dict["eight"]["begin"]=line_num
            elif "9. In the case of a contract" in line:    
                field_dict["eight"]["end"]=line_num
            elif "assessed:" in line:    
                field_dict["nine"]["begin"]=line_num
            elif "10. Description of any provision under which" in line:    
                field_dict["nine"]["end"]=line_num
            elif "or maintenance services:" in line:    
                field_dict["ten"]["begin"]=line_num
            elif "11. Particulars of future" in line:    
                field_dict["ten"]["end"]=line_num
            elif "their proposed transfer:" in line:    
                field_dict["eleven"]["begin"]=line_num
            elif "12. Particulars of future transfers" in line:    
                field_dict["eleven"]["end"]=line_num
            elif "of the proposed transfer:" in line:    
                field_dict["twelve"]["begin"]=line_num
            elif "13. The results of any" in line:
                field_dict["twelve"]["end"]=line_num
            elif "of Sydney:" in line:    
                field_dict["thirteen"]["begin"]=line_num
            elif "14. The components and quantum" in line:    
                field_dict["thirteen"]["end"]=line_num
                field_dict["fourteen"]["begin"]=line_num
            elif "15. If relevant," in line:    
                field_dict["fourteen"]["end"]=line_num
            elif "sage charges):" in line:    
                field_dict["fifteen"]["begin"]=line_num
            elif "16. If relevant," in line:    
                field_dict["fifteen"]["end"]=line_num
            elif "assumptions involved:" in line:    
                field_dict["sixteen"]["begin"]=line_num
            elif "17. Particulars as to any " in line:    
                field_dict["sixteen"]["end"]=line_num
            elif "be entered into:" in line:    
                field_dict["seventeen"]["begin"]=line_num
            elif "18. Particulars of any other" in line:    
                field_dict["seventeen"]["end"]=line_num  
                field_dict["eighteen"]["begin"]=line_num
                field_dict["eighteen"]["end"]=doc_length
            else:
                pass
            line_num += 1

        field_loc_dict = {}
        for field in field_dict:
            locations = [i for i in range(field_dict[field]["begin"]+1,field_dict[field]["end"] )]
            field_loc_dict[field] = locations
        results_dict = {}
        for field in field_loc_dict:
            line_indices = field_loc_dict[field]
            print line_indices
            ln = len(line_indices)
            if ln == 0:
                results = "Not found"

            elif field == "two":
                if ln == 2:
                    name = lines[line_indices[0]].replace("Name:", "")
                    address = lines[line_indices[1]].replace("Address:", "")
                    results_dict["name"] = name
                    results_dict["address"] = address
                elif ln < 2:
                    name = lines[line_indices[0]].replace("Name:", "")
                    results_dict["name"] = name
                    results_dict["address"] = "Not Found"
                else:
                    name = lines[line_indices[0]].replace("Name:", "")
                    multiple_line_field= []
                    line_indices.pop(0)
                    for l in line_indices:
                        multiple_line_field.append(lines[l])
                    address = "; ".join(multiple_line_field).replace("Address:", "")
                    results_dict["address"] = address
                    results_dict["name"] = name
            elif field == "four":
                if ln == 2:
                    date = lines[line_indices[0]].replace("Effective Date:", "")
                    duration = lines[line_indices[1]].replace("Duration:", "")
                    results_dict["date"] = date
                    results_dict["duration"] = duration
                elif ln < 2:
                    date = lines[line_indices[0]].replace("Effective Date:", "")
                    print date
                    results_dict["date"] = date
                    results_dict["duration"] = "Not Found"
                else:
                    date = lines[line_indices[0]].replace("Effective Date:", "")
                    multiple_line_field= []
                    line_indices.pop(0)
                    for l in line_indices:
                        multiple_line_field.append(lines[l])
                    duration = "; ".join(multiple_line_field).replace("Duration: ", "")
                    results_dict["date"] = date
                    results_dict["duration"] = duration

            elif ln <2:
                results = lines[line_indices[0]]
            else:
                multiple_line_field= []
                for l in line_indices:
                    multiple_line_field.append(lines[l])
                results = "; ".join(multiple_line_field)
            results_dict[field] = results
        data = (contract_type,contract_type_dum,results_dict["one"],results_dict["name"],results_dict["address"],results_dict["three"],results_dict["date"],results_dict["duration"],results_dict["five"],results_dict["six"],results_dict["seven"],results_dict["eight"],results_dict["nine"],results_dict["ten"],results_dict["eleven"],results_dict["twelve"],results_dict["thirteen"],results_dict["fourteen"],results_dict["fifteen"],results_dict["sixteen"],results_dict["seventeen"],results_dict["eighteen"])
        write_data(data, output_path)