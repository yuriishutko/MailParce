import email
import imaplib
import credentials


def open_session(imap_url, username, password):
    """Function creates and returns an object of the connection with specified credentials and imap_url"""
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(username, password)
    return con


def get_body_of_the_message(message):
    """Take a message
    Function helps to figure out if message is multipart.
    If it's so it joins them and return to one output
    !!!decode('KOI8-R', errors='ignore')!!! make a message human-readable"""
    if message.is_multipart():
        return get_body_of_the_message(message.get_payload(0))
    else:
        return (message.get_payload(None, True)).decode('KOI8-R', errors='ignore')


def search_by_keys(key, value, connection):
    """Function provides to find some messages by parameters and keys
    For example
    search('FROM', 'Y.Shutko@creatio.com', connection)
    Where con is an object of connection to the mailbox"""
    result, data = connection.search(None, key, '"{}"'.format(value))
    return data


def get_bodies_of_messages():
    """Function returns several messages and convert them to human-readable format by defined filter"""
    array_of_filtered_messages = []
    connection = open_session(credentials.imap_url, credentials.user, credentials.password)
    connection.select('INBOX')
    messages = get_emails_from_mailbox(connection.search(None, 'unseen')[1], connection)
    # messages = get_emails_from_mailbox(search_by_keys('FROM', credentials.from_email, connection), connection)
    for message in messages:
        array_of_filtered_messages.append(get_body_of_the_message(email.message_from_bytes(message[0][1])))
    return array_of_filtered_messages


def get_emails_from_mailbox(result_of_search_in_bytes, connection):
    """This function receives bytes and forms all the necessary
    service information about the letter, body, head and so on"""
    array_of_messages = []
    for num in result_of_search_in_bytes[0].split():
        typ, data = connection.fetch(num, '(RFC822)')
        array_of_messages.append(data)
    return array_of_messages

