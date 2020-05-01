import smtplib, whois, json

CONFIG_FILE = './config.json'

USERNAME = None
PASSWORD = None
DOMAINS = []
RECIPIENTS = []

def main():

    read_json()

    server = gmail_login()

    for domain in DOMAINS:
        if (whois.query(domain) == None):
            message = "The domain name '" + domain + "' may be available."
            send_message(server, message)

    # close the server connection
    server.close()

# read the configuration file
# sets the global variables
def read_json():

    global USERNAME
    global PASSWORD
    global DOMAINS
    global RECIPIENTS

    with open(CONFIG_FILE) as f:
        data = json.load(f)

        USERNAME = data['username']
        PASSWORD = data['password']
        RECIPIENTS = data['recipients']
        DOMAINS = data['domains']

# create server object
def gmail_login():

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(USERNAME, PASSWORD)
        
    except Exception as e:
        print(e)

    return server

# send message to server
def send_message(server, message):

    for rec in RECIPIENTS:
        server.sendmail(USERNAME, rec, message)

main()