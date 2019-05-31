import pandas as pd 
import os 
import csv
import json

path = './csvfiles'
files = []

#createing CSV comparision result to display on the web page
def data_set_creator():
    #json objet to store pass fail result and additional information
    result ={}
    create_file_list()
    #Reading the files recived from the directory. Can be improved later
    A = pd.read_csv(files[0], header=[0]).drop_duplicates()
    B = pd.read_csv(files[1], header=[0]).drop_duplicates()
    #getting number of rows and columns in dataframe shape -> (#row, #column)
    count_file1 = A.shape
    count_file2 = B.shape
    #getting the row difference between the two CSV
    count_difference = count_file1[0] - count_file2[0]
    #IMPLEMENT THE COLUMN DIFFERENCE BETWEEN CSV
    #creating response for which file has more rows 
    if(count_difference > 0):
        result['line1'] = '('+files[0]+') has '+str(count_difference)+' more rows then ('+files[1]+')'
    elif(count_difference < 0):
        result['line1'] = files[1]+' has '+str(count_difference)+' more rows then '+files[0]
    else:
        result['line1'] = "NO MISMATCH"
    #Need to add a condition to check the columns
    #finding the difference between file1 and file2 [list(A.columns) gives list of colums]
    # A - B 
    only_in_file1 = pd.merge(A, B, on=list(A.columns), how='left', indicator=True).query("_merge == 'left_only'")
    only_in_file1_count = only_in_file1.shape
    #finding percentage difference between the two CSV based on rows
    matched_in_file1_percent = round(((count_file1[0] - only_in_file1_count[0])/count_file1[0])*100)
    result['line2'] = matched_in_file1_percent
    #adding additional attribute to json for the HTML page
    if matched_in_file1_percent != 100:
        result['line3'] = "Incomplete match"
        result['line3C'] = "red"
    else:
        result['line3'] = "Complete match"
        result['line3C'] = "green"
    #creating data.csv file to get the difference between the two csv in new csv
    f= open("./output/data.csv","w")
    f.write(files[0] + " --> Questionable Rows \n")   
    #writing merge output to the new CSV 
    only_in_file1.to_csv (f, mode='a', index = None, header=True)
    f.close()
    #finding difference between file2 and file1
    # B - A
    only_in_file2 = pd.merge(A, B, on=list(A.columns), how='right', indicator=True).query("_merge == 'right_only'")
    print(only_in_file2)
    only_in_file2_count = only_in_file2.shape
    #finding percentage difference between the two CSV based on rows
    matched_in_file2_percent = round(((count_file2[0] - only_in_file2_count[0])/count_file2[0])*100)
    f= open("./output/data.csv","a")
    f.write(files[1] + " --> Questionable Rows \n")
    only_in_file2.to_csv (f, mode='a', index = None, header=True)
    print(matched_in_file2_percent)
    result['line4'] = matched_in_file2_percent
    if matched_in_file2_percent != 100:
        result['line5'] = "Incomplete match"
        result['line5C'] = "red"
    else:
        result['line5'] = "Complete match"
        result['line5C'] = "green"
    f.close()
    #creating the final data csv whiching going to be used to display in HTML
    f= open("./output/data.csv","r")
    f1= open("./output/data_fin.csv","w")
    for line in f.readlines():
        if line.strip() == '':
            continue
        f1.write(line)
    #creating the json file for he HTML page
    outputdetails = open("./output/file.json",'w')
    outputdetails.write(json.dumps(result))
    outputdetails.close

#Function is being used to go through a complete folder and add CSV file path to the file global variable
def create_file_list():
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file))

#main function
if __name__ == "__main__":
    data_set_creator()