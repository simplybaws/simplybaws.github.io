#AutoRenamer.py
#Created by Cade Muntz for the use of the College of Business at Oregon State University.


import os 
import docx2txt # Extracts text from docx files
import PyPDF2 # extracts text from PDF files
import re 
import shutil


#Function to extract information from specifically docx files
def extract_from_docx(filename):
    text = docx2txt.process(filename) #turns doc into text
    lines = text.split("\n") #splits text into individual lines

    #establishes both as None to start, only replaces if something is found to replace with
    course_number = None
    instructor = None
 
    # Look for course number using "Course Number:" and alternative pattern
    pattern = r"(BA|BIS|MRKT|MGMT|ECON)[\s_]*(\d{3})" #establishes the pattern to look for
  
    #Loop to iterate through the lines
    for line in lines:
            if course_number is None:
                match = re.search(pattern, line) #Otherwise, we look for the pattern and the 3 digits after the pattern
                if match:
                    course_number = match.group(0) #if the pattern matches me match the pattern with the 3 digits
                    line = line.replace(course_number, "").strip() #and replace
                    course_number = course_number.replace("_", "")

            # Extract instructor email
            if instructor is None and re.search(r"([\w.-]+)[\s]?@(oregonstate\.edu|bus\.oregonstate\.edu)", line): #search for either @oregonstate or @bus.oregonstate
                email = re.search(r"([\w.-]+)[\s]?@(oregonstate\.edu|bus\.oregonstate\.edu)", line).group(1) #find only the first occurence
                instructor = email.split('@')[0] #split first half from the email half

    return course_number, instructor #return the values :)


#Same thing but for PDF files 
def extract_from_pdf(filename):
    course_number = None
    instructor = None
    
    with open(filename, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            lines = text.split("\n")
            pattern = r"(BA|BIS|MRKT|MGMT|ECON)[\s_]*(\d{3})"
            for line in lines:
                if course_number is None:
                    match = re.search(pattern, line) #Otherwise, we look for the pattern and the 3 digits after the pattern
                    if match:
                        course_number = match.group(0) #if the pattern matches me match the pattern with the 3 digits
                        line = line.replace(course_number, "").strip() #and replace
                        course_number = course_number.replace("_", "")

                    # Extract instructor email
                if instructor is None and re.search(r"([\w.-]+)[\s]?@(oregonstate\.edu|bus\.oregonstate\.edu)", line): #search for either @oregonstate or @bus.oregonstate
                    email = re.search(r"([\w.-]+)[\s]?@(oregonstate\.edu|bus\.oregonstate\.edu)", line).group(1) #find only the first occurence
                    instructor = email.split('@')[0] #split first half from the email half

    return course_number, instructor #return the values :)


#Same thing for DOC files
def extract_from_doc(filename):
    text = docx2txt.process(filename)  # Extract text from DOC file
    lines = text.split("\n")
    course_number = None
    instructor = None

    # Look for course number using "Course Number:" and alternative pattern
    pattern = r"(BA|BIS|MRKT|MGMT|ECON)[\s_]*(\d{3})"
    for line in lines:
        if course_number is None:
            match = re.search(pattern, line)
            if match:
                course_number = match.group(0)
                line = line.replace(course_number, "").strip()
                course_number = course_number.replace("_", "")

        # Extract instructor email
        if instructor is None and re.search(r"([\w.-]+)[\s]?@(oregonstate\.edu|bus\.oregonstate\.edu)", line):
            email = re.search(r"([\w.-]+)[\s]?@(oregonstate\.edu|bus\.oregonstate\.edu)", line).group(1)
            instructor = email.split('@')[0]

    return course_number, instructor



#Calls the individual functions to extract from the file itself
def extract_from_file(filename):
    _, extension = os.path.splitext(filename) #splits the filename from the extension (mysyllabus.pdf becomes .pdf i.e., extension = .pdf)

    if extension == ".docx": #if docx use docx function
        return extract_from_docx(filename)
    
    elif extension == ".pdf": # if pdf use pdf function
        return extract_from_pdf(filename)
    
    elif extension == ".doc": #if doc use doc function
        return extract_from_doc(filename)
    
    else: #otherwise, return nothing
        return None, None




# Path to the folder containing the files
#... While loop to ensure that the path is correct and repeatedly asks for a new path if the path is not a real path on their system
while True:
    folder_path = input("Enter the folder path: ")
    
# Verify if the provided folder path exists
    if os.path.isdir(folder_path):
        break
        
    print("Invalid folder path:", folder_path)
    print("Please ensure that you are entering a correct folder path where the files you would like to be re-named are kept")
    
   

print(" ")
print("File changes noted below!")
print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ ")
print("--------------------")

incomplete_folder_path = os.path.join(folder_path, "Incomplete")

movedcount = 0
renamedcount = 0

# Create the "Incomplete" folder if it doesn't exist
if not os.path.exists(incomplete_folder_path):
    os.makedirs(incomplete_folder_path)


# Iterate over files in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name) #gets the folder path and filename


    if os.path.isfile(file_path):
        _, extension = os.path.splitext(file_name) #splits the extension
        if extension in ['.doc', '.docx', '.pdf']: #makes sure the extension is one of these three

            course_number, instructor = extract_from_file(file_path) #assigns the variables

            if course_number is not None and instructor is not None: #if the file has the correct information then the file will be renamed with said information
                new_file_name = f"{course_number.replace(' ', '')}{instructor}{extension}"
                new_file_path = os.path.join(folder_path, new_file_name)

                os.rename(file_path, new_file_path) #Renames the file :)

                #useful little print statement so the user knows which file got renamed to what
                print("Renamed file:", file_name)
                print("New file name:", new_file_name)
                print("--------------------")
                renamedcount+=1
                #if the information is not valid then it will let the user know the program couldnt find the course number or instructor information from said file    
            else:
                new_file_path = os.path.join(incomplete_folder_path, file_name)
                shutil.move(file_path, new_file_path) 
                print("Skipping file:", file_name)
                print("Reason: Course number or instructor information not found.")
                print("--------------------")
                movedcount+=1
          #if the extension isnt one of the three used then the program will skip the file      
        else: 
            print("Skipping file:", file_name)
            print("Reason: File format not supported.")
            print("--------------------")
print("Number of files renamed = ",renamedcount,"!!")            
print("Number of files that were unable to be renamed= ",movedcount)            

