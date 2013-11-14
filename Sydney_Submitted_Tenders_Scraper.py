import os
import csv
import urllib2
import urllib
import re
from bs4 import BeautifulSoup
import dateutil.parser as dparser

def write_data(data): #This is used for two different writing functions. Make sure to change the file name and fieldnames
    ordered_fieldnames =  ["type", "number", "name", "title", "bidder", "date", "committee_mem1", "committee_mem2", "committee_mem3"]

    if os.path.exists("/Users/sunlight/Documents/Sydney Contracts Project/Sydney_Bidders_Bulk.csv"):
        with open("/Users/sunlight/Documents/Sydney Contracts Project/Sydney_Bidders_Bulk.csv", "a") as datatest:
    #csv.register_dialect("custom", delimiter="", skipinitialspace=True)
            writer = csv.writer(datatest, dialect="excel")
            try:
                writer.writerow([s.encode("utf-8") for s in data])
            except UnicodeEncodeError:
                print userdataset
                pass
    else:
        with open("/Users/sunlight/Documents/Sydney Contracts Project/Sydney_Bidders_Bulk.csv", "w") as datatest:
        #csv.register_dialect("custom", delimiter="", skipinitialspace=True)
            csv.DictWriter(datatest, dialect="excel", fieldnames=ordered_fieldnames).writeheader()
            writer = csv.writer(datatest, dialect="excel")
            try:
                writer.writerow([s.encode("utf-8") for s in data])
            except UnicodeEncodeError:
                print i
                pass

def get_html( path):
    try:
        fp = urllib2.urlopen(path)
        return fp.read()
    except urllib2.HTTPError, e:
        if e.code == 404:
            raise Http404
        else:
            #retry once
            try:
                fp = urllib2.urlopen(path)
                return json.loads(fp.read())
            except urllib2.HTTPError, e:
                raise e
if __name__=='__main__':
    url =  "http://www.cityofsydney.nsw.gov.au/business/tenders/submitted-tenders"
    
    page = get_html(url)

    soup = BeautifulSoup(page)
    pretty =soup.prettify()

    tender_data = soup.find_all(attrs={"id": "content_div_65007"})[0]
    tender_nums = tender_data.find_all('h3')
    for tender in tender_nums:
        tender_num = tender.text
        tender_chunks = tender_num.split()
        ttype = tender_chunks[0]
        t_id = tender_chunks[1]
        loc = soup.find('h3', text =tender_num)
        if loc == None:
            loc = soup.find('strong', text= "1312").parent
        else:
            pass
        if loc.find_next_sibling('h4') != None:        
            description = loc.find_next_sibling('h4').text
            add_info = loc.find_next_sibling('p').text
            submission_ul = loc.find_next_sibling('ul')
        else:
            desc = loc.find_next_sibling('p')
            description = desc.text
            add_info = desc.find_next_sibling('p').text
            submission_ul = loc.find_next_sibling('ul')
        info_chunk = add_info.split(":")
        date = dparser.parse(info_chunk[0], fuzzy=True).strftime("%m/%d/%Y")
        name_string = info_chunk[1]
        names = re.split(", | and", name_string)
        childrenz = []
        for child in submission_ul.children:
            if child != "\n":
                childrenz.append(child.text)
            else:
                pass
        for child in childrenz:
            try:
                data = (tender_num, ttype,t_id, child, description, date, names[0], names[1], names[2])
            except:
                data = (tender_num, ttype,t_id, child, description, date, name_string)
            write_data(data)
        
