import re
import sys
import time
import random
import os.path
import getpass
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

body = ''
mode = ''
email_subject = "YOUR SUBJECT HERE" #ENTER THE EMAIL'S SUBJECT
email_address = "" # ENTER YOUR EMAIL ADDRESS ON LINE NUMBER 79

# YOUR ATTACHMENT LOCATION
FILE_LOCATION = ""
# YOUR ATTACHMENT FILE NAME
FILE_NAME = ""

files = [
    "body_agent.txt",
    "body_company.txt",
    "raw_data.txt",
    "raw_data2.txt",
]


def get_body():
    var = input("please enter the mode of email \n for email to Agents, please enter A or Agent \n for email to Company, please Enter C or Company  \n")
    if var == "a" or "A" or "agent" or "AGENT":
        body_agent = open('body_agent.txt', 'r')
        body = body_agent.read()
        body_agent.close()
        mode = 'Agent'
        return body
    if var == "c" or "C" or "Company" or "COMPANY":
        body_company = open('body_company.txt', 'r')
        body = body_company.read()
        body_company.close()
        mode = 'Company'
        return body
    else:
        get_body()

def get_emails():
    old = 0
    repeated = 0
    email_list = []
    file = open('raw_data.txt','r')
    line = file.read()
    new_list = re.findall(r'[\w\.-]+@[\w\.-]+', line)
    print("Searching emails...")
    #checking in current list for no repetition
    old_emails_file = open('emails_sent.txt', 'r')
    old_emails = old_emails_file.read()
    for i in new_list:
        # CROSS VERIFY WITH PREVIOUS EMAILS
        if i not in email_list:
            if i not in old_emails:
                    email_list.append(i)
            elif i in old_emails:
                # print(i + "\t\t was already send email")
                old = old + 1
        elif i in email_list:
            #print(i + "\t\t have appeared more than once")
            repeated = repeated + 1
        # TO SEND EMAILS ANYWAYS UNCOMMENT THE LINE BELOW
        # email_list.append(i)

    print("Unique new emails found :"+str(len(email_list)))
    print("Repeated Emails Addresses in NEW list : " + str(repeated))
    print("Repeated Emails Addresses in OLD list : " + str(old))
    old_emails_file.close()
    send_emails(email_list)

def start_server():
    email_address = "" # YOUR EMAIL ADDRESS HERE
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("Logging in as : " + str(email_address))
    server.login(str(email_address), str(email_password))
    time.sleep(6)
    print("Logged in!")
    return server

def send_emails(list):
    new_entry = open('emails_sent.txt', 'a')
    new_entry.write(
        "\n====================================" + time.strftime("%d/%m/%Y") + "====================================\n")

    print("Preparing Your emails...")
    total_to = len(list)
    print("total emails: " + str(total_to))
    print("Starting the Server...")
    server = start_server()
    sno = 0
    for current_to in range(0, int(total_to)):
        toaddr = list[current_to]
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = toaddr
        msg['Subject'] = email_subject

        msg.attach(MIMEText(body, 'plain'))
        filename = FILE_NAME
        attachment = open(FILE_LOCATION, "rb")

        part = MIMEBase('application', "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        text = msg.as_string()
        server.sendmail(email_address, toaddr, text)
        sno = sno + 1
        print(str(sno) + "\t" + mode + " Email sent!" + " @ " + time.strftime(
            "%I:%M:%S %p") + " From: " + email_address + " To " + toaddr)
        new_entry.write(str(sno) + ":\t" + mode + " Email sent!" + " @ " + time.strftime(
            "%I:%M:%S %p") + " From: " + email_address + " To " + toaddr + "\n")
        waiting = random.randint(0,9)
        print("please wait " + str(waiting) + " seconds")
        time.sleep(10)

    print("sent " + str(total_to) + " email(s)")
    # END PROGRAM PROTOCOL
    end_program(total_to, new_entry)
    quit_server(server)


def end_program(total_to, new_entry):
    new_entry.write("\nsent " + str(total_to) + " email(s)")
    new_entry.write("\n==================================================================================\n")
    new_entry.close()


def quit_server(server):
    server.quit()
    exit()

to_create = []
def check_files():
    for file in files:
        if os.path.exists(file):
            pass
        else:
            to_create.append(file)

    if len(to_create) is 0:
        print("to_create is empty")
        return True
    else:
        print(to_create)
        return False

def create_files():
    print("will create files ")
    for file in files:
        if file in to_create:
            print(file)
            write_file(file, "")

def write_file(path, data):
    f = open(path, 'a')
    f.write(data)
    f.close()

def print_instructions():
    line_1 = "_ _ . . : :  I N S T R U C T I O N S  : : . . _ _\n this is how you have to write the files. Make sure you follow these instructions carefully\n" \
             "==============================================......=============================================\n" \
             "WHAT TO WRITE IN THE emailer_V3.py FILE\n" \
             "\nWrite your email address.\n" \
             "\twhat it looks like before email address :(ON LINE NUMBER 79) email_address = '' # YOUR EMAIL ADDRESS HERE\n" \
             "\twhat it looks like after  email address :(ON LINE NUMBER 79) email_address = 'your_email@address.com' # YOUR EMAIL ADDRESS HERE\n" \
             "DO NOT WRITE YOUR PASSWORD IN emailer_V3.py FILE. \nYOU WILL BE PROMTED TO WRITE THE PASSWORD ONCE THE PROGRAM RUNS THE SCRIPT\n" \
             "\nWrite your Email subject. ON LINE NUMBER 15" \
             "\nWrite your attachment file Location. ON LINE NUMBER 19" \
             "\nWrite your attachment file name. ON LINE NUMBER 21" \
             "\n===================......========================================================================\n" \
             "FILE NAME \t\t\t\t\t\t\t\t\t\t\t\t WHAT TO WRITE\n"
    print(line_1)
    write_file("instructions.txt", line_1)

    line_2 = "raw_data.txt\t\t\t\t write the email addresses in this file. each email address should be in a new line\n"
    print(line_2)
    write_file("instructions.txt", line_2)

    line_3 = "body_agent.txt\t\t\t\t write the body of email you want to send to the Agents.\n"
    print(line_3)
    write_file("instructions.txt", line_3)

    line_4 = "body_company.txt\t\t\t write the body of email you want to send to the Companies.\n"
    print(line_4)
    write_file("instructions.txt", line_4)

    print("These instructions can also be found in instructions.txt\n"
          "Please fill the text files and rerun the script")



def first_checkpoint():
    yesChoice = ['yes', 'y', ' yes', ' y']
    noChoice = ['no', 'n', ' no', ' n']
    if check_files():
        print("You have all the necessary files")
        return True
    else:
        permission = input(
            "You Do not seem to have the required files necessary to continue with this script. Would you like to auto-create the necessary files: (y/n)\n>>")
        if permission in yesChoice:
            create_files()
            print_instructions()
            exit()
        elif permission in noChoice:
            exit()
        else:
            print("Invalid input.\nExiting.")
            exit()


if __name__ == "__main__":
    if first_checkpoint():
        pass
    # get password
    email_password = getpass.getpass('password: ')
    # get body
    list = []
    body = get_body()
    email_address, email_password = email_address, email_password
    get_emails()