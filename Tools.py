from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

import pandas as pd


def fix_email_list(email_lst):
    last_email = ''
    output = []
    for email in email_lst:
        if pd.isnull(email):
            output.append(last_email)
        else:
            output.append(email)
            last_email = email
    return output


def aggregate_offers(emails, positions):
    output = []
    size_emails = len(emails)
    size_positions = len(positions)

    if size_emails != size_positions:
        raise Exception('Unmatched data')

    for i in range(size_emails):
        if not pd.isnull(positions[i]):
            output.append(Offer(emails[i], positions[i]))

    return output


def interested(offer, not_interested):
    tokens = offer.position.lower().split(' ')
    for token in tokens:
        if token in not_interested:
            return False
    return True

def generate_mail(send_from, send_to, subject, text, file=None):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open(file, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
                Name=basename(file)
        )
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)

    return msg.as_string()


class Offer:
    def __init__(self, email, position):
        self.email = email
        self.position = position

    def contains(self, text):
        return text.lower() in self.position.lower()

    def company(self):
        at = self.email.find('@')
        dot = self.email.find('.', at)
        domain = self.email[at+1:dot:]
        return domain

    def __str__(self):
        return '{}, {}'.format(self.email, self.position)



