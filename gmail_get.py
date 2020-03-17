import email
import imaplib
import credentials


def open_session(imap_url, username, password):
    """
    Function creates and returns an object of the connection with specified credentials and imap_url
    """
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(username, password)
    return con


def get_body_of_a_message(message):
    """
    Take a message
    Function helps to figure out if message is multipart.
    If it's so it joins them and return to one output
    !!!decode('KOI8-R', errors='ignore')!!! make a message human-readable
    """
    if message.is_multipart():
        return get_body_of_a_message(message.get_payload(0))
    else:
        return (message.get_payload(None, True)).decode('KOI8-R', errors='ignore')


def search(key, value, connection):
    """
    Function provides to find some messages by parameters and keys
    For example
    search('FROM', 'Y.Shutko@creatio.com', con)
    Where con is an object of connection to the mailbox
    """
    result, data = connection.search(None, key, '"{}"'.format(value))
    return data


def get_bodies():
    """
    Function returns several messages and convert them to human-readable format by defined filter"
    """
    connection = open_session(credentials.imap_url, credentials.user, credentials.password)
    msgs_arr = []
    connection.select('INBOX')
    messages = get_emails(search('FROM', 'Y.Shutko@creatio.com', connection), connection)
    for message in messages:
        msgs_arr.append(get_body_of_a_message(email.message_from_bytes(message[0][1])))
    return msgs_arr


def get_emails(result_bytes, connection):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = connection.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

