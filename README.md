# USF Registration Notifications
USF Registration Notifications is a python application that scrapes USF class data in order to send notifications regarding seat availability.

The data is scraped from:

[USF Registrar Schedule Search](http://www.registrar.usf.edu/ssearch/staff/staff.php)

## Installation

Clone this repository using the "Clone or download" button in the top right corner of the repository or by typing the git clone command:

```bash
git clone https://github.com/tcharts-boop/usf_registration_notifications.git
```
or for a specific directory:

```bash
git clone https://github.com/tcharts-boop/usf_registration_notifications.git /specific/directory/
```

After the repository is cloned, navigate to the directory of the cloned repository and install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

First edit the crn_text_file.txt file to reflect your specific information. The formatting is as such:

```text
example@usf.edu
password
semester year, crn
```

For example:

```text
johndoe45@usf.edu
mypasswordisbad
Fall 2020, 82520
Fall 2020, 94806
Spring 2021, 15020
Summer 2020, 52757
```

To run from the command prompt, you must be in the directory of the cloned repository.

From there you can run by typing:
```bash
python usf_registration_notifications
```

The script will ask for a duration (in hours) and an interval (in minutes).

After the duration and interval is set, the script will run for the total duration.

To exit the script early, press CTRL + C.

### Limitations

There are some user limitations that were implemented.

1. Only 10 CRNs can be scraped every execution (e.g. only 10 CRNs will be read from the text file.)
2. Only the Outlook USF email can be utilised at this time:
    - example@usf.edu --- GOOD
    - example@mail.usf.edu --- BAD
    - example@gmail.com --- BAD
    - example@yahoo.com --- BAD
    
    If you want to implement other emails, I reccomend using Outlook rules to create a rule that will forward emails from       yourself to your preferred email.
3. Duration of script runtime is limited to a max of 4 hours.
4. Interval of script run frequency is limited to every 1 to 10 minutes.

    

## Author

[Theodore Charts](https://www.linkedin.com/in/tedcharts/)

## License
[MIT](https://choosealicense.com/licenses/mit/)

