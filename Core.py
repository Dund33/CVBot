import pandas as pd
from Tools import fix_email_list
from Tools import aggregate_offers
from Tools import interested
from Tools import Offer
from Tools import generate_mail
import weasyprint
import smtplib
import base64


# authorize email
smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp.login('my_email', 'my_key')

subject = 'ZPR PWr-W8-Staż'
body = '''Dzień Dobry!
Piszę w związku z programem stażowym ZPR PWr

Załączam moje CV
Wiadomość wysyłam za pomocą mojego BOTa. Jeżeli otrzymali ją Państwo przez pomyłkę, to przepraszam :)

Pozdrawiam
Łukasz Dróżdż'''

msg = f'Subject: {subject}\n\n{body}'

# technical mumbo-jumbo
employers_file = pd.read_excel('base.xlsx', sheet_name=u'BAZA PRACODAWCÓW', usecols='G:H')
employers_lst = employers_file[10::]

emails = employers_lst[u'Unnamed: 6'].to_list()[1::]
positions = employers_lst[u'JAK ZWIĘKSZĘ SWPOJĄ SZANSĘ?'].to_list()[1::]

# fixing nans
emails_fixed = fix_email_list(emails)
offers = aggregate_offers(emails_fixed, positions)

# tried those already
done = ['aiut', 'micro-solutions', 'titian', 'rgb-elektronika', 'sente', 'big-xyt']

# can't do those
not_interested = ['javascript', 'sap', 'ruby']

# filtering the offers
offers_programmer = filter(lambda x: x.contains('developer') or x.contains('programista'), offers)
offers_filtered = filter(lambda x: interested(x, not_interested), offers_programmer)
offers_final = filter(lambda x: x.company() not in done, offers_filtered)

# load the template
cv_template = open('CV.htm', 'r').read()

# generate and send the CVs
for offer in offers_final:
    print('generating ' + offer.company() + ' for ' + offer.position)
    filename = 'cvs/' + offer.company() + '.pdf'
    cv = cv_template.replace('{POSITION}', offer.position)
    weasyprint.HTML(string=cv).write_pdf(filename)
    email = generate_mail('my_email', offer.email, subject, body, filename)
    smtp.sendmail('my_email', offer.email, email)
