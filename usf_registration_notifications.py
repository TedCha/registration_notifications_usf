import sys
import time
from application import ApplicationMethods 
from application import CheckSeats, SendEmail

def main():

    # Sets up email data list (the message data that will be sent to us)
    email_data = []

    sent_email_data = []

    # Instance variable of ApplicationMethods Class
    load = ApplicationMethods()

    # Sets variable to return value of load file method
    file_load = load.load_file()
    
    # Sets email variable
    email = file_load['email']

    # Sets password variable
    password = file_load['password']

    # For loop for the number of CRNs passed in
    for i in range(len(file_load['list'])):
        
        # Set up term and crn variables
        term = file_load['list'][i][0]
        crn = file_load['list'][i][1]

        # Instance variable of CheckSeats Class
        run = CheckSeats(term, crn)

        # Set class_dict to returned value of check_seats method (class data dictionary)
        class_dict = run.check_seats()

        # If iteration equals 10, break the loop (max of 10 crn's allowed to be checked)
        if i == 10:
            break

        # If the seats available in the class > 0, append to email_data
        elif int(class_dict['SEATSREMAIN']) > 0:
            
            valid_class_data = [term,
            class_dict['CRN'], 
            class_dict['SUBJ CRS#'],
            class_dict['SEATSREMAIN']]

            email_data.append(valid_class_data)

        # If the seats available < 0, continue loop
        else:
            continue

    # If email_data variable is populated create and send a message
    if email_data:
        email = SendEmail(email, password, email_data)

        message = email.create_email_message()

        email.send_email(message)

    # If email_data variable is not populated, quit program
    else:
        print('No seats available.')
        pass

if __name__ == "__main__":

    # Create variable instances of the ApplicationMethods class for set duration method
    event = ApplicationMethods.set_duration()

    # Create variable instances of the ApplicationMethods class for set interval method
    interval = ApplicationMethods.set_interval()

    # While the event counter is less than or equal to the set duration
    while event['count'] <= event['duration']:
        try:
            # Print output 
            print('-----------------------------')
            print('Running script...')
            main()
            print('Waiting for next run...')
            
            # Add the interval to the counter
            event['count'] += interval

            # Sleep for that interval
            time.sleep(interval)
        except:
            # If any failure takes place, the while loop will break
            print('Script failure, closing program.')
            break
    
    # Print number of times the class data was scraped. 
    print('Class data scraped ' + str(int(event['count']/interval)) + ' times.')