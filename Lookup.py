from datetime import datetime
from Truck import *


# Provides methods and attributes for obtaining information about the simulation
class Lookup:

    # Takes a hash table and a distance table to provide information about the simulation
    def __init__(self, hasher, distance_table):

        self.hasher = hasher
        self.distance_table = distance_table
        self.address_dict = dict()

        # Prepares the address table with empty lists to hold associated package ID's
        for address in distance_table.addresses:
            self.address_dict[address[1]] = []

        # Add ID's to the address table for quick lookup of packages by ID
        for bucket in range(1, len(self.hasher.bucket_table)):

            # If empty, continue
            if not self.hasher.bucket_table[bucket]:
                continue

            # shorten the call to the package's address
            address = self.hasher.bucket_table[bucket][0].get_package_address()

            # If the package address matches an address in the address dictionary, append the ID of that package to that
            # address
            if address in self.address_dict:
                self.address_dict[address].append(self.hasher.bucket_table[bucket][0].get_package_id())

    # Provides a menu to lookup package information
    def Options(self):

        # A while loops keeps the menu intact with error checking to prevent the program from failing
        quit_lookup = False
        while not quit_lookup:

            print("\n[INFO MENU]")
            print("\nEnter the requested package info to lookup package information")

            # A single package can be looked up by ID and information is displayed based on the simulation having
            # already finished (e.g. packages are all delivered at this time). If the user searches by address, it will
            # return all packages that are to be delivered to that address, if any
            print("How would you like to lookup a package or packages?\n")

            print("1 Search package by ID")
            print("2 Search by package delivery address")
            print("3 Back to Main Menu")

            choice = 0

            # Try to make an integer out of the users' input. If ValueError, retry. If choice out of range, retry.
            try:
                choice = int(input("\nOption #: "))

            except ValueError:

                print('Please use a number that corresponds to the menu items and press enter')
                input('Press [ENTER] to try again')

                continue

            except choice < 1 or choice > 3:

                print('Please use a number that corresponds to the menu items and press enter')
                input('Press [Enter] to try again')

            if choice == 1:

                # Takes the user's input and makes an integer
                input_id = ''

                try:

                    input_id = int(input("Package ID: "))

                except ValueError:

                    print('Package ID must be a positive number')
                    input('Press [ENTER] to try again')

                    continue

                # Uses the provided integer to locate a package and display its contents by calling the find by ID
                # method of the hash table
                print(self.hasher.find_by_id(input_id))

                input("Press [ENTER] to continue")

            if choice == 2:

                address = input("Package delivery address: ")

                try:

                    for i in self.address_dict[address]:
                        # If the provided address does not exactly match a string in the address dictionary,
                        # catch the key error and allow the user to try again
                        print(self.hasher.find_by_id(i))

                    input("Press [ENTER] to continue")

                except KeyError:

                    print('Invalid address. Check the spelling and case, then try again')
                    input('Press [ENTER] to continue')

                    continue

            # Return control to the Main Menu in the Main.py file
            if choice == 3:
                quit_lookup = True

    # An interface where package status can be viewed in a specific time as well as truck mileage at that time
    def time_and_mileage(self, trucks):

        quit_loop = False
        while not quit_loop:

            print('\n[TIME INFO MENU]\n')
            print('Enter corresponding number to view information')

            print('1 View package info/status at a specific time')
            print('2 View all package info/status at a specific time')
            print('3 Return to Main Menu')

            choice = 0

            # Try to make an integer out of the users' input. If ValueError, retry. If choice out of range, retry.
            try:
                choice = int(input("\nOption #: "))

            except ValueError:

                print('\nPlease use a number that corresponds to the menu items and press enter')
                input('Press [ENTER] to try again')

                continue

            except choice < 1 or choice > 3:

                print('Please use a number that corresponds to the menu items and press enter')
                input('Press [Enter] to try again')

            if choice == 1:

                # Takes the user's input and makes an integer
                input_id = ''

                try:

                    input_id = int(input("Package ID: "))

                    if self.hasher.find_by_id(input_id) is None:
                        print('Package not found')

                        continue

                except ValueError:

                    print('\nPackage ID must be a positive number')
                    input('Press [ENTER] to try again')

                    continue

                try:

                    # Get desired time from user and split it into a list at the colon
                    time_string = input("Enter time in 24-hour format with no spaces ex: '14:34' for 2:34pm: ")
                    time_string = time_string.split(':')

                    # Index 0 will be the hour and index 1 will be the minutes
                    time_hour = int(time_string[0])
                    time_minute = int(time_string[1])

                    # Create a datetime out of the provided user time
                    input_date_time = datetime(year=2000, month=1, day=1, hour=time_hour, minute=time_minute, second=0)

                    # Obtain the package and create datetimes from its load time and delivery time to compare with the
                    # user time provided
                    package = self.hasher.bucket_table[input_id][0]
                    package_load_time = self.get_time_from_string(package.get_package_loaded())
                    package_deliver_time = self.get_time_from_string(package.get_package_delivered())

                    if input_date_time < package_load_time:

                        # By the time the user interface is loaded, all packages have been delivered and the status is
                        # already showing that. However, when presenting the information to the user at a specific time

                        print(package.get_hub_status())
                        input('Press [ENTER] to continue')

                        continue

                    elif package_deliver_time > input_date_time >= package_load_time:

                        print(package.get_loaded_status())
                        input('Press [ENTER] to continue')

                        continue

                    elif input_date_time >= package_deliver_time:

                        print(package.get_delivered_status())
                        input('Press [ENTER to continue')

                        continue

                except IndexError:

                    print('\nHour and minute must be separated by a colon')
                    input('Press [ENTER] to continue')

                    continue

                except ValueError:

                    print('\nHour and minute must be separated by a colon. Ex: 14:56 for 2:56pm')
                    input('Press [ENTER] to continue')

                    continue

            # Loop through the entire list of packages and compare against the user provided time to display the
            # appropriate status
            elif choice == 2:

                try:

                    # Get desired time from user and split it into a list at the colon
                    time_string = input("Enter time in 24-hour format with no spaces ex: '14:34' for 2:34pm: ")
                    time_string = time_string.split(':')

                    # Index 0 will be the hour and index 1 will be the minutes
                    time_hour = int(time_string[0])
                    time_minute = int(time_string[1])

                    # Create a datetime out of the provided user time
                    input_date_time = datetime(year=2000, month=1, day=1, hour=time_hour, minute=time_minute, second=0)

                    # Obtain the package and create datetimes from its load time and delivery time to compare with the
                    # user time provided

                    for bucket in self.hasher.bucket_table:

                        if bucket:

                            package = bucket[0]
                            package_load_time = self.get_time_from_string(package.get_package_loaded())
                            package_deliver_time = self.get_time_from_string(package.get_package_delivered())

                            if input_date_time < package_load_time:

                                # By the time the user interface is loaded, all packages have been delivered and the
                                # status is already showing that. However, when presenting the information to the
                                # user at a specific time

                                print(package.get_hub_status())

                                continue

                            elif package_deliver_time > input_date_time >= package_load_time:

                                print(package.get_loaded_status())

                                continue

                            elif input_date_time >= package_deliver_time:

                                print(package.get_delivered_status())

                                continue

                except IndexError:

                    print('\nHour and minute must be separated by a colon')
                    input('Press [ENTER] to continue')

                    continue

                except ValueError:

                    print('\nHour and minute must be separated by a colon. Ex: 14:56 for 2:56pm')
                    input('Press [ENTER] to continue')

                    continue

                total_mileage = trucks[0].get_time_mileage_from_time(input_date_time) + \
                                trucks[1].get_time_mileage_from_time(input_date_time)

                print('Total combined mileage:', total_mileage)

            elif choice == 3:

                quit_loop = True

    # Converts a package's time string to a datetime
    def get_time_from_string(self, time_string):

        split_string = time_string.split(':')

        hour = int(split_string[0])
        minute = int(split_string[1])
        second = int(split_string[2])

        date_time = datetime(year=2000, month=1, day=1, hour=hour, minute=minute, second=second)

        return date_time
