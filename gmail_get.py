import imaplib
import email
import credentials


def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


# def get_decoded_message(message):


con = imaplib.IMAP4_SSL(credentials.imap_url)
con.login(credentials.user, credentials.password)
con.select('INBOX')

result, data = con.fetch(b'1', '(RFC822)')
rav = email.message_from_bytes(data[0][1])

# decoded_message = quopri.decodestring(get_body(rav)).decode('KOI8-R', errors="ignore")
print(get_body(rav).decode('KOI8-R', errors="ignore"))

