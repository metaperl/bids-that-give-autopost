bids that give autoposter
========================

[Bids That Give](http://www.everybidhelpsakid.com/princepawn) is a
penny auction website. Affiliates of this penny auction are required
to post a classifieds ad somewhere on the internet each day and record
the URL of their post in their back-office.

This free source code addresses both of these requirements.
* It automatically posts an advertisement encouraging people to take
some sample bids in a penny auction ad.
* It automatically records the URL of the advertisement in the advertisers
back-office so that she receives reward points for posting her ad.

# Installation

sudo pip install pygments
sudo pip install docutils
sudo pip install gdata
sudo pip install BeautifulSoup
sudo pip install requests

# Usage

## Create a blogspot.com blog

Mine happens to be [Free Bids for Penny
Auctions](http://freebidsforpennyauction.blogspot.com/)

## Obtain your blog id

    cd python-blogger; ./pb.py --listblogs \
      --username  blogspot_username --password blogspot_password

    running this command will return a number showing you your blog id

## create config.py in the root directory

Create a file config.py in the root directory (the same directory this
README is in) that describes your blog and the zeek affiliates that
will be posting their for advertisement posting credit.

```python
blog = {
    'id' : 486769223931063890,
    'username' : 'thequietcenter@gmail.com',
    'password' : 'magickJack66'
}

users = {

    "thequietcenter" : {                     # my login name
        'website_id' : 'princepawn'          # my replicated BTG websites id
        'zeekpass'   : "bxxxx",              # password for login name
        'email'      : 'schemab@gmail.com' # send results of posting to
    },

}
```
