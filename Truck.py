from datetime import datetime, timedelta


class Truck:

    def __init__(self, id_number):

        self.id = id_number

        self.date = datetime(year=2000, month=1, day=1, hour=8, minute=0, second=0)
        self.time = self.date.strftime('%H:%M:%S')
        self.SPEED = 18
        self.distance_travelled = float(0)
        self.packages = []
        self.package_ids = []
        self.addresses_loaded = []
        self.current_location = '4001 South 700 East'

        # Each time the truck makes a delivery stop or loads packages, a time is stamped here with the total mileage
        # so that a user could see the mileage at any time.
        self.time_mileage = []

    # If the truck has less than 16 packages, updates the package status to loaded, gets the time it was loaded/en route
    # , appends the package to the truck's list of packages, and also the truck's list of addresses that it has to visit
    def load_package(self, package):

        if len(self.packages) < 16:
            package.set_package_status('Loaded')
            package.set_package_loaded(self.get_time())
            self.packages.append(package)
            self.addresses_loaded.append(package.get_package_address())

            return True

        elif len(self.packages) >= 16:

            return False

    def get_packages(self):

        return self.packages

    # Checks if a truck is full
    def is_full(self):

        if len(self.packages) >= 16:
            return True

        elif len(self.packages) < 16:
            return False

    # If the key/Package ID matches a key/Package ID in the truck's list of packages, changes the status to delivered,
    # sets the delivered time, and removes the package from the truck.
    def unload_package(self, package):

        for i in self.packages:

            if i.get_package_id() == package.get_package_id():
                i.set_package_status('Delivered')
                i.set_package_delivered(self.get_time())
                self.packages.remove(i)

    # Adds to a list where each index contains a list that contains time passed and distance travelled
    def update_time_mileage(self):

        self.time_mileage.append([self.get_date_time(), self.get_distance_travelled()])

    def get_time_mileage(self):

        return self.time_mileage

    # Returns the total mileage this truck has travelled up to the provided time
    def get_time_mileage_from_time(self, date_time):

        # Hold all times earlier than the time_string
        earlier_times = []
        later_times = []
        for i in self.get_time_mileage():

            if i[0] <= date_time:

                earlier_times.append(i)

            elif i[0] > date_time:

                later_times.append(i)

        if not earlier_times and date_time > datetime(year=2000, month=1, day=1, hour=8, minute=0):

            total_mileage = self.get_time_mileage()[-1][1]

            return total_mileage

        try:

            closest_time_index = earlier_times.index(max(earlier_times))

        except ValueError:

            total_mileage = 0

        else:

            total_mileage = earlier_times[closest_time_index][1]

        return total_mileage

    # Given a sorted version of the list already loaded, removes the unsorted list and fills it with the sorted list.
    def sort_packages(self, package_list):

        self.packages.clear()
        self.packages = package_list

    def set_package_ids(self):

        for package in self.get_packages():
            self.package_ids.append(package.get_package_id())

    def get_package_ids(self):

        return self.package_ids

    def set_current_location(self, address):

        self.current_location = address

    def get_current_location(self):

        return self.current_location

    # Using the truck's constant speed of 18mph, advances the truck's time based on the time passed to make a delivery.
    # Also sets the 'time friendly' string to the hour/minute/second
    def update_time(self, distance):

        time = float(distance / 18)

        self.date += timedelta(hours=time)
        self.time = self.date.strftime('%H:%M:%S')

    def get_time(self):

        return self.time

    def get_date_time(self):

        return self.date

    def set_id_number(self, id_number):

        self.id = id_number

    def get_id_number(self):

        return self.id

    def update_distance_travelled(self, distance):

        self.distance_travelled += distance

    def get_distance_travelled(self):

        return self.distance_travelled

    def update_addresses_loaded(self, address):

        self.addresses_loaded.append(address)

    def get_addresses_loaded(self):

        return self.addresses_loaded
