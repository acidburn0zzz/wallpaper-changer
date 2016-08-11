#!/usr/bin/env python2
# Auto Change wallpapers from wallhaven

from bs4 import BeautifulSoup as bs
from subprocess import Popen
from getpass import getuser
from random import choice
from time import sleep
import requests
import re
import os

MONITORS = 1
DESTINATION = "/home/{0}/.wallpapers".format(getuser())
RESOLUTIONS = "1920x1080"
RATIOS = "16x9"
CATEGORIES = "100"  # General Anime People
PURITY = "100"  # SFW NSFW 0
URL = "https://alpha.wallhaven.cc/random?categories={0}&purity={1}&resolutions={2}&ratios={3}".format(CATEGORIES, PURITY, RESOLUTIONS, RATIOS)

DELAY = 60 * 15


def get_images(html):
    soup = bs(html, "lxml")
    links = soup.findAll('img')[1:]

    if not os.path.isdir(DESTINATION):
        os.makedirs(DESTINATION)

    for i in xrange(MONITORS):
        try:
            link = choice(links)['data-src']
        except IndexError:
            return

        number = re.match(r'^https://alpha.wallhaven.cc/wallpapers/thumb/small/th-(\d+).jpg$', link).group(1)
        response = requests.get('https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{0}.jpg'.format(number))
        if response.status_code == 200:
            with open('{0}/monitor{1}.jpg'.format(DESTINATION, i), 'wb') as fw:
                fw.write(response.content)


def setup_wallpaper():
    while True:
        r = requests.get(URL)
        get_images(r.text)

        command = 'feh'

        for i in xrange(MONITORS):
            command += ' --bg-scale {0}/monitor{1}.jpg'.format(DESTINATION, i)

        Popen(command.split(' '))

        sleep(DELAY)


def main():

    try:
        pid = os.fork()
        if pid > 0:
            exit(0)

    except OSError as e:
        print "{0}".format(e)

    os.setsid()
    os.umask(0)

    setup_wallpaper()

if __name__ == '__main__':
    main()
