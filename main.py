# Brayden McArthur
# Student ID: 001261746
# DATA STRUCTURES AND ALGORITHMS II — C950
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM


# Import FileHandler to read in the csv files, lookup to add the ability to lookup packages, delivery to start the
# simulation, and truck to pass in the trucks that will be delivering packages
from FileHandler import *
from Lookup import *
from Delivery import *
from Truck import *


# A program that reads in packages and distances from csv files and puts the packages into a hash table for quick
# retrieval and processing. A simulation is run to delivery the packages as quickly and efficiently as possible while
# honoring the criteria in the package notes.
def main():

    # Create a package FileHandler variable to handle importing package
    # data as well as generating the hash table.
    package_handler = FileHandler('WGUPS Package File.csv')

    # A distance handler holds the data from the distance csv file
    distance_handler = FileHandler('WGUPS Distance Table.csv')

    # Using the package FileHandler object to generate a hash table from the package csv file
    hasher = package_handler.import_package_file()
    # The distance table provides methods and attributes for finding the most optimal routes
    distances_table = distance_handler.import_distance_file()

    # The 2 trucks that will be delivering packages
    truck_1 = Truck(1)
    truck_2 = Truck(2)

    # A list of trucks to be passed into the delivery for the simulation
    trucks = [truck_1, truck_2]

    # A delivery object contains several methods that work together to run a simulation based on the criteria in this
    # assignment.
    delivery = Delivery(hasher, trucks, distances_table)

    # Starts the simulation and collects information along the way so that a user can use the interface to track
    # packages, deliveries, times, and mileage
    delivery.start_simulation()

    # The interface is held in place by a while loop with error handling to keep the interface intact if a user provides
    # invalid input
    quit_app = False
    while not quit_app:

        # A lookup object uses the information from a hash table containing packages and a distances table containing
        # distances between addresses
        lookup = Lookup(hasher, distances_table)
        choice = 0
        # Information to guide the user through the interface
        print("[MAIN MENU]")
        print("\nSelect from the below options by typing the corresponding number and hit enter:")
        print("1 View package information")
        print("2 View package delivery status and truck mileage at any time")
        print("3 Quit")

        # Interface navigation is done primarily through numbers corresponding to options displayed in the menus
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
            lookup.Options()

        if choice == 2:
            lookup.time_and_mileage(trucks)

        if choice == 3:
            quit_app = True


if __name__ == '__main__':
    main()
