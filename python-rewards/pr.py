#!/usr/bin/python

# https://www.zeekrewards.com/backoffice/back_office.asp

# post username
# post password

import logging
import re
import sys

from BeautifulSoup import BeautifulSoup
import requests

login_host = 'secure.bidambassadors.com'


my_config = {'verbose': sys.stderr}

s = requests.session()


def full_url(path):
    return "https://{0}/{1}".format(login_host, path)

def backoffice_url(path):
    return full_url("{0}/{1}".format("backoffice", path))

def parse_command_line():
    import getpass

    import argparse

    parser = argparse.ArgumentParser(description='Post zeek ad url')

    parser.add_argument("--zuser", help='Zeek Rewards username')
    parser.add_argument("--zpass", help='Zeek Rewards password')
    parser.add_argument("adurl", help='The URL of the ad you posted today')
    parser.add_argument("notifyemail", help='The email to send confirmation results to')

    args = parser.parse_args()
    opts = dict()
    if not args.zuser:
        args.zuser = raw_input("Zeek Username: ")
    if not args.zpass:
        args.zpass = getpass.getpass()
    return parser, args

def log_response(r):
    logging.warn("""
                 Status code - {0},
                 Headers - {1}
                 Encoding - {2}
                 URL - {3}
                 Cookies - {4}
                 """.format(
        r.status_code, r.headers, r.encoding, r.url, r.cookies
        ))

def login(args):
    post = {
        'username': args.zuser,
        'password': args.zpass,
        'agree' : 0,
        'submit' : 'Login'
    }

    login_url = full_url('office')
    query = { 'action' : 'accountAccess' }

    logging.debug("post parms: {0}".format(post))

    r = s.get(login_url, config=my_config, data=post, params=query)
    log_response(r)
    html = r.text.encode("utf-8")
    return html

def click_place_ad(html):
    soup = BeautifulSoup(html)
    elem = soup.find(href=re.compile("ad_options.asp"))
    href = elem['href']

    place_ad_url = backoffice_url(elem["href"])
    #raise Exception(place_ad_url)
    r = s.get(place_ad_url, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def click_register_ad(html):
    soup = BeautifulSoup(html)
    # elem = soup.find(href=re.compile("ad_submit.asp"))
    # print elem
    register_ad_url = 'https://secure.bidambassadors.com/office/marketing/ads/report-it/'
    r = s.get(register_ad_url, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def submit_ad(html, args):
    url = full_url('office/marketing/ads/report-it/index.asp')
    query = { 'pass' : 'Add' }
    post = {
        'placead' : "http://freebidsforpennyauction.blogspot.com/",
        'adtype': "Ezine",
        'url': args.adurl,
        'MAX_FILE_SIZE' : 50000,
        'memo': '',
        'Submit' : 'Confirm Your Ad',
        'approvedtext' : ""
    }

    soup = BeautifulSoup(html)


    r = s.post(url, data=post, config=my_config, params=query)

    log_response(r)
    html = r.text.encode("utf-8")
    return html

def email_confirmation(email, html, user):
    # Import smtplib for the actual sending function
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart('alternative')

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'BTG posting for {0}'.format(user)
    msg['To'] = email
    msg['From'] = 'thequietcenter@gmail.com'

    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.set_debuglevel(1)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.quit()


if __name__ == '__main__':
    parser, args = parse_command_line()

    html = login(args)
    #logging.warn("login html: {0}".format(html))
    #raise Exception(html)
#    html = click_place_ad(html) # simulate clicking on "PLACE YOUR AD"
#    html = click_register_ad(html) # click on Register your Ad to Qualify for Today's Cash Rewards
#    print "*** submitting ad ***"
    html = submit_ad(html,args)
    logging.warn("result of submit: {0}".format(html))
    email_confirmation(args.notifyemail, html, args.zuser)
