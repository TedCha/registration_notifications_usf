import mechanicalsoup
from bs4 import BeautifulSoup
import unicodedata
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import sys

class ApplicationMethods:
    
    # Static method to load text file into variables/list
    @staticmethod
    def load_file():
        file_name = 'crn_text_file.txt'

        with open(file_name, 'r') as file:

            # Set up email and password variables
            email = file.readline().strip()
            password = file.readline().strip()
            
            # Strip line and split by ', ' into array if the value is not blank
            term_crn_list = [line.strip().split(', ') for line in file if line.strip()]

        print('File loaded successfully.')

        # Return variables in dictionary data type
        return {'list': term_crn_list, 'email': email, 'password': password}

    # Static method to return duration and duration counter variables
    @staticmethod
    def set_duration():
        duration_count = 0

        while True:
            
            # Try to get an int input
            try:
                duration_hours = int(input('Duration (in hours): '))
            
            # Try again if not int input
            except:
                print("Please enter a number value between 1 - 4.")
                continue

            else:
                # If duration_hours between 1 and 4, break the loop
                if duration_hours >= 1 and duration_hours <= 4:
                    break

                # If not between 1 and 4, continue loop
                else:
                    print("Please enter a number value between 1 - 4.")
                    continue
        
        # Convert hours to seconds
        duration = int(duration_hours * 3600)

        # Return variables in dictionary data type
        return {'duration': duration, 'count': duration_count}
    
    @staticmethod
    def set_interval():

        while True:

            # Try to get an int input
            try:
                interval_minutes = int(input('Interval (in minutes): '))
            
            # Try again if not int input
            except:
                print("Please enter a number value between 1 - 10.")
                continue

            else:

                # If interval_minutes between 1 and 10, break the loop
                if interval_minutes >= 1 and interval_minutes <= 10:
                    break
                
                # If not between 1 and 10, continue loop
                else:
                    print("Please enter a number value between 1 - 10.")
                    continue
        
        # Convert minutes to seconds
        interval = int(interval_minutes * 60)

        # Return interval variable
        return interval

class CheckSeats():
    
    # Initialize CheckSeats class with term and crn variables
    def __init__(self, term, crn):
        self.term = term
        self.crn = crn
    
    # Method to scrape class data from USF registrar query page
    def check_seats(self):

        # Creates instance of StatefulBrowser
        browser = mechanicalsoup.StatefulBrowser()

        # Sets up term value to correct HTML option value
        if self.term == 'Spring 2021':
            term_value = '202101'
        elif self.term == 'Fall 2020':
            term_value = '202008'
        elif self.term == 'Summer 2020':
            term_value = '202005'

        url = 'http://www.registrar.usf.edu/ssearch/staff/staff.php'

        browser.open(url)

        # Select form with HTML method as post
        browser.select_form('form[method="post"]')

        # Fill in the term value
        browser["P_SEMESTER"] = term_value

        # Fill in the crn value
        browser["P_REF"] = self.crn

        # Submit query
        response = browser.submit_selected()

        # Load query page HTML response into variable
        html_doc = response.text

        # Instance of BeautifulSoup
        soup = BeautifulSoup(html_doc, 'lxml')

        # Keys are the text value of headers
        keys = soup.select('#results tr th')

        # Values are the text values of class data
        values = soup.select('#results tr td')

        # Set up class_dict as dictionary data type
        class_dict = dict()

        # For loop in the length of the values
        for i in range(len(values)):
            key = unicodedata.normalize("NFKC", keys[i].get_text())
            value = unicodedata.normalize("NFKC", values[i].get_text())
            
            # Add a value to our class_dict dictionary
            class_dict[key] = value

        # Print statement to show affected CRN
        print('CRN ' + self.crn + ' - Seats Remaining: ' + class_dict['SEATSREMAIN'])
        
        # Return class_dict dictionary
        return class_dict

class SendEmail():

    # Initialize SendEmail class with email, password, and message_data variables
    def __init__(self, email, password, message_data):
        self.email = email
        self.password = password
        self.message_data = message_data
    
    # Method that creates our email message from scrapped class data
    def create_email_message(self):
        
        # msg euqals instance of MIMEMultipart
        msg = MIMEMultipart()

        # From ourselves
        msg['From'] = self.email

        # To ourselves
        msg['To'] = self.email

        # Subject line
        msg['Subject'] = 'Some of your classes are available!'

        # Set up body variable with empty string
        body = ''

        # Append to body for however many crn's had seats available
        for i in range(len(self.message_data)):
            # Format each string with a row of the message_data array
            body += '{} - CRN {}: {} has {} seats available.\n'.format(*self.message_data[i])

        # Attch the method as plain text
        msg.attach(MIMEText(body, 'plain'))

        # Set the string value of msg to msg_text
        msg_text = msg.as_string()

        print('Message created.')

        # Return msg_text variable
        return msg_text
    
    # Method that sends created message to passed in email
    def send_email(self, message):

        # SMTP is outlook.office365.com (@usf.edu is an instance of office 365)
        smtp = 'outlook.office365.com'

        # Required port for office 365 smtp
        port = 587

        # Set up SMTP server
        server = smtplib.SMTP(smtp, port)

        # Start SMTP server with encryption
        server.starttls()

        # Login in with email in password
        server.login(self.email, self.password)

        # Send email to ourselves with created message
        server.sendmail(self.email, self.email, message)

        # Quit the server
        server.quit()

        print('Email sent successfully.')