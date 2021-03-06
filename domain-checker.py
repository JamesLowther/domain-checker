# Domain name checker
# James Lowther | 2020/04/30

import smtplib, whois, json, os
from datetime import datetime

CONFIG_FILE = 'config.json'

# currently configured for gmail
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

def main():

    username, password, recipients, domains = read_json()

    server = gmail_login(username, password)
    possible_domains = check_domains(domains)


    # send email if possible domains exist
    if (possible_domains):
        message = "Subject: Domain name(s) may be available\n\n"
        message += "The following domain(s) may be available:\n\n"
        
        for domain in possible_domains:
            message += domain + "\n"

        message += "\nScript run at: " + datetime.now().strftime('%d-%b-%Y (%H:%M:%S)')

        send_message(server, recipients, username, message)

    # close the server connection
    server.close()

# read the configuration file
# sets the global variables
def read_json():

    path = os.path.dirname(os.path.realpath(__file__)) + '/' + CONFIG_FILE

    with open(path) as f:
        data = json.load(f)

        username = data['username']
        password = data['password']
        recipients = data['recipients']
        domains = data['domains']

        f.close()

        return (username, password, recipients, domains)

# create server object
def gmail_login(username, password):

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(username, password)
        
    except Exception as e:
        print(e)

    return server

# returns a list of domains that may be available
def check_domains(domains):

    possible_domains = []

    for domain in domains:
        try:
            whois.whois(domain)

        # PywhoisError is returned when a domain may be available
        except whois.parser.PywhoisError:
            possible_domains.append(domain)

    return possible_domains

# send message to server
def send_message(server, recipients, username, message):

    for rec in recipients:
        server.sendmail(username, rec, message)

main()
