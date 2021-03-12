###################################################################################################
#                              MIT Licence (C) 2021 Cubicpath@Github                              #
###################################################################################################
"""A small script built on Selenium that facilitates easy automation of free
crate collection from the Wynncraft Store."""

import atexit
from datetime import datetime
from os import path, mkdir
from random import randint
from sys import platform, argv
from subprocess import run
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Client:
    """Handles Selenium logic for the Wynncraft store"""
    WIN_DRIVER = './bin/geckodriver.exe'
    NIX_DRIVER = './bin/geckodriver'
    SITE_URL = 'https://store.wynncraft.com'

    def __init__(self, log_name=f'log_{datetime.now().strftime("%Y-%m-%d_%H;%M;%S")}_{randint(1000, 9999)}.log', print_messages=True):
        log_name = f'./logs/{log_name}'
        mkdir('./logs/') if (log_name.startswith('./logs/') and not path.isdir('./logs/')) else None
        self.print_messages = print_messages
        self.browser = webdriver.Firefox(executable_path=self.WIN_DRIVER if platform == 'win32' else self.NIX_DRIVER, service_log_path=log_name, timeout=10)
        self.browser.get(self.SITE_URL)

    def _print(self, message: str):
        print(message) if self.print_messages else None

    def get_free_crates(self, usernames: list[str]):
        """Attempts to checkout free wynncraft crates for a list of usernames."""
        self.wynn_store_logout()
        duplicate_ready = []
        for username in usernames:
            if username and username not in duplicate_ready:
                self.wynn_store_login(username)
                if self.wynn_store_checkout():
                    self._print(f"Got free crate for '{username}' successfully.")
                else:
                    self._print(f"Couldn't get free crate for '{username}'.")
                duplicate_ready.append(username)
                self.wynn_store_logout()

    def wynn_store_checkout(self, attempt_times=2) -> bool:
        """Attempts to checkout items from the Wynncraft Store."""
        for attempts in range(attempt_times):
            if attempts >= 1:
                self.browser.get(f'{self.SITE_URL}/checkout/basket')
            try:
                self.browser.find_element_by_id('privacyConsent').click()
                self.browser.find_element_by_name('agreement').click()
                self.browser.find_element_by_class_name('btn-success').click()
                return True
            except NoSuchElementException:
                pass
        return False

    def wynn_store_login(self, name: str, attempt_times=2) -> bool:
        """Attempts to login to the Wynncraft store from the store homepage."""
        for attempts in range(attempt_times):
            if attempts >= 1:
                self.browser.get(self.SITE_URL)
            try:
                self.browser.find_element_by_class_name('free-crate-container').click()
                self.browser.find_element_by_class_name('input-lg').send_keys(name)
                self.browser.find_element_by_class_name('input-group-btn').click()
                return True
            except NoSuchElementException:
                pass
        return False

    def wynn_store_logout(self, attempt_times=2) -> bool:
        """Logout from the Wynncraft store."""
        for attempts in range(attempt_times):
            if attempts >= 1:
                self.browser.get(self.SITE_URL)
            try:
                self.browser.find_element_by_class_name('changeUsername').click()
                return True
            except NoSuchElementException:
                pass
        return False

    def quit(self):
        """Logs out of Wynncraft Store and quits the browser."""
        if self.browser:
            self.wynn_store_logout()
            self.browser.quit()
            self.browser = None


def main(*args):
    """if __name__ == '__main__':"""

    def clear_screen():
        """Clears the terminal."""
        if platform == 'win32':
            run('cls', shell=True, check=True)
        elif platform.startswith('linux') or platform == 'darwin':
            run('clear', shell=True, check=True)
        else:
            raise ValueError(f"OS PLATFORM NAME IS NOT AN EXPECTED VALUE: {platform}")

    client = Client()
    atexit.register(client.quit)

    while True:
        usernames = []
        for username in args[0].strip().split(',' if args else input("Enter usernames to get crates for, separate usernames with ','\n").strip().split(',')):
            usernames.append(username.strip())
        print(usernames)

        client.get_free_crates(usernames)
        if not args and input("Enter 'again' to run again:\n|").lower() == 'again':
            clear_screen()
        else:
            break


if __name__ == '__main__':
    if len(argv) <= 2:
        main(argv[1]) if len(argv) == 2 else main()
    else:
        raise ValueError(f'Please only use one argument ex: [{argv[0]} "username1,user name2, username 3"]')
