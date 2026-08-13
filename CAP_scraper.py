import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import pandas as pd

url = 'https://chesterfieldauto.com/newest-cars'
tables = pd.read_html(url)

# 1st table - Richmond
table1 = tables[0]
slim_tbl1 = table1[['Store', 'Make', 'Model', 'Year', 'Engine', 'Yard Row', 'Set']]

# 2nd table - Fort Lee
table2 = tables[1]
slim_tbl2 = table2[['Store', 'Make', 'Model', 'Year', 'Engine', 'Yard Row', 'Set']]

# 3rd table - Southside
table3 = tables[2]
slim_tbl3 = table3[['Store', 'Make', 'Model', 'Year', 'Engine', 'Yard Row', 'Set']]

alltbls = pd.concat([slim_tbl1, slim_tbl2, slim_tbl3])
alltbls["Year"] = pd.to_numeric(alltbls["Year"])

result = alltbls.loc[alltbls['Year'] <= 1992]
print(result)


def send_email(df: pd.DataFrame):
    sender = os.environ["EMAIL_SENDER"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["EMAIL_RECIPIENT"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Chesterfield Auto - cars 1992 and older ({len(df)} found)"
    msg["From"] = sender
    msg["To"] = recipient

    if df.empty:
        body_html = "<p>No cars 1992 or older found today.</p>"
        body_text = "No cars 1992 or older found today."
    else:
        body_html = df.to_html(index=False)
        body_text = df.to_string(index=False)

    msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(body_html, "html"))

    # Gmail SMTP settings - adjust host/port if using a different provider
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())


send_email(result)
