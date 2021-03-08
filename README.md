About:
======
WynncraftCrate is a small script built on [Selenium](https://www.selenium.dev/selenium/docs/api/py/) that facilitates easy automation of free crate collection from the [Wynncraft Store](https://store.wynncraft.com).

This project uses Firefox's geckodriver, you can find the source code [here](https://github.com/mozilla/geckodriver/releases).

>**By using or modifying this application, you agree to the license found in [LICENSE](./LICENSE.txt) (MIT Licence)**

_Requirements can be found in [requirements.txt](requirements.txt)._

How to use:
-----------
There are three ways you can use this script:

1. Launch it directly for manual crate collection.
2. Automate the program using ONE command-line argument. (it will automatically close the browser when done)
    1. Usage: wynncrate.py "username1,user name2, username 3" (Separate usernames with commas)
3. Import the "Client" class in [wynncrate.py](wynncrate.py) for use in your own Python projects.

Documentation:
--------------
    class Client: Handles Selenium logic for the Wynncraft store, uses the Firefox geckodriver for website interaction.
        param log_filepath: Where to store the Selenium log file. By default it generates one log per object initialized.
        param print_messages: Whether to print messages to stdout or not.
        field WIN_DRIVER: Points to Windows geckodriver location.
        field NIX_DRIVER: Points to *nix-like geckodriver location. (Linux, Unix, MacOS, etc.)
        field SITE_URL: Points to the Wynncraft Store homepage.
        field browser: Firefox Selenium browser; starts when a Client object is initialized.
        field print_messages: allows class-level access of param.
        
            Methods that start with "wynn_store" directly interact with the website, others are for convenience sake.
        method _print: Prints message depending on the self.print_messages value
        method get_free_crates: Attempts to checkout free wynncraft crates for a list of usernames.
        method wynn_store_checkout: Attempts to checkout items from the Wynncraft Store.
        method wynn_store_login: Attempts to login to the Wynncraft store from the store homepage.
        method wynn_store_logout: Logout from the Wynncraft store.
        method quit: Logs out of Wynncraft Store and quits the browser.

    func main: called when __name__ == '__main__' and arguments are valid. Houses CLI interaction.
        func clear_screen: Used to reset display text in the CLI.
