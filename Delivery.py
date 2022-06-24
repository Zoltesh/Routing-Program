from datetime import datetime


class Delivery:

    def __init__(self, hash_table, truck_list, distance_table):

        # Where the trucks start and end
        self.hub = '4001 South 700 East'

        # Package correction that will take place at 10:20am
        self.package_correction = ['410 S State St', '84111']
        self.package_correction_time = datetime(year=2000, month=1, day=1, hour=10, minute=20, second=0)

        # The hash table containing the packages from the supporting files
        self.hasher = hash_table
        self.bucket_table = hash_table.bucket_table

        # A copy of the bucket table without any empty buckets
        self.all_packages_no_gaps = []
        self.no_restraints = []

        # A list of trucks that will be delivering packages
        self.truck_list = truck_list

        # The individual trucks
        self.truck_1 = self.truck_list[0]
        self.truck_2 = self.truck_list[1]

        # A table containing all distances from one address to another address and methods for routing
        self.distance_table = distance_table

        # The list of packages that have a note saying they must be delivered together
        self.deliver_together_final = []
        self.deliver_together_final_addresses = []

        # A list of packages that need to be delivered
        self.packages_to_deliver = []

        # A list of delivery addresses of packages at the hub
        self.package_addresses_hub = []

        self.try_to_load_addresses = []
        # A list of addresses that are associated with a delayed package and need to wait for the delayed package to be
        # ready before delivering to this address.
        self.delayed_addresses = []
        self.delayed_packages = []
        self.try_to_load = []
        self.set_deliver_together_final()
        self.set_deliver_together_final_addresses()

    # As the algorithm is running in a while loop until all the packages are delivered, their statuses need to be
    # updated or refreshed before starting a new iteration
    def refresh_package_status(self):

        self.packages_to_deliver.clear()

        for bucket in self.bucket_table:

            if bucket:

                status = bucket[0].get_package_status()
                if 'Loaded' not in status and 'Delivered' not in status:
                    self.packages_to_deliver.append(bucket[0])

    # Method to ensure delayed packages/wrong address packages and their associated packages (by address) will not be
    # checked for loading
    def set_delayed_package_lists(self):

        for package in self.get_all_packages_no_gaps():

            note = package.get_package_note()
            address = package.get_package_address()

            # If a package has a delay or wrong address in the note, add it to the list of delayed packages and add
            # its address to the list of delayed addresses
            if 'Delayed' in note:

                self.delayed_packages.append(package)
                self.delayed_addresses.append(address)

            elif 'Wrong address' in note:

                self.delayed_packages.append(package)

            # If the current package has the same address and any package in the delayed lists, add the current
            # package to the lists as well
            elif address in self.get_delayed_address():

                self.delayed_packages.append(package)
                self.delayed_addresses.append(address)

            # If it does not have delayed/wrong address in its note and its address does not match any package in
            # the delayed package list, let it try to be loaded.
            else:

                for i in self.get_try_to_load():

                    if i.get_package_address() in self.get_delayed_address():

                        if i.get_package_address() not in self.get_try_to_load_addresses():
                            self.set_try_to_load_addresses(i.get_package_address())

                if package not in self.get_try_to_load():
                    self.set_try_to_load(package)

                if address not in self.get_try_to_load_addresses():
                    self.set_try_to_load_addresses(address)

    # Removes any packages from the delayed list if their note condition time is at or before an eligible truck's
    # current time AND any packages with the same address don't also have a conflicting note.
    def remove_delay(self, truck):

        for bucket in self.bucket_table:

            if bucket:

                note = bucket[0].get_package_note()
                address = bucket[0].get_package_address()

                # Skip packages that don't mention a delay or wrong address in the note
                if 'Delayed' not in note and 'Wrong address listed' not in note:
                    continue

                # If the wrong address is listed and it is 10:20 or later, correct the package address info, set the
                # note to blank and then continue to the next package
                elif 'Wrong address listed' in note and truck.get_date_time() >= self.package_correction_time:
                    bucket[0].set_package_address(self.package_correction[0])
                    bucket[0].set_package_zip(self.package_correction[1])
                    bucket[0].set_package_note('')

                    self.delayed_packages.remove(bucket[0])

                    if bucket[0] not in self.get_try_to_load():

                        self.set_try_to_load(bucket[0])

                    if bucket[0].get_package_address() not in self.get_try_to_load_addresses():
                        self.set_try_to_load_addresses(bucket[0].get_package_address())

                    continue

                # If any of the available trucks' current time is at or after the current package's time correction,
                # clear the delayed note from the package
                elif 'Delayed' in note and self.get_package_time(note) <= truck.get_date_time():

                    bucket[0].set_package_note('')

                    for package in self.delayed_packages:

                        sub_package_note = package.get_package_note()
                        sub_package_address = package.get_package_address()

                        # If any other package in the delayed lists has the same address as the current package, keep it
                        # in the delayed list until all packages of the same address can be delivered together
                        if 'Delayed' not in sub_package_note:

                            if sub_package_address == address:

                                if bucket[0] in self.delayed_packages:
                                    self.delayed_packages.remove(bucket[0])
                                    self.delayed_addresses.remove(address)

                                    self.set_try_to_load(bucket[0])
                                    self.set_try_to_load_addresses(address)

                                self.delayed_packages.remove(package)
                                self.delayed_addresses.remove(sub_package_address)

                                self.set_try_to_load(package)
                                self.set_try_to_load_addresses(sub_package_address)

                        else:

                            continue

                else:

                    continue

            else:

                continue

    def get_delayed_packaged_list(self):

        return self.delayed_packages

    def get_packages_to_deliver(self):

        return self.packages_to_deliver

    def get_delayed_address(self):

        return self.delayed_addresses

    # Given a package id and package note, adds the package id to a list of packages that need to be delivered together
    def set_deliver_together_final(self):

        deliver_together = []
        deliver_together_integer = []

        for bucket in self.bucket_table:

            if bucket:

                package_note = bucket[0].get_package_note()
                package_id = bucket[0].get_package_id()

                if 'Must be delivered with' in package_note:

                    # String methods to remove everything except for the package ID's that go with the current package
                    deliver_together.append(package_note.split('Must be delivered with '))
                    deliver_together[-1].remove('')

                    deliver_together[-1][0] = deliver_together[-1][0].replace(',', '')
                    deliver_together[-1][0] = deliver_together[-1][0].split(' ')

                    temp_list = []
                    for i in deliver_together[-1][0]:

                        if i not in temp_list:
                            temp_list.append(int(i))

                    for i in temp_list:

                        if i not in deliver_together_integer:
                            deliver_together_integer.append(int(i))

                    # Add the ID of the current package if not already in list
                    if package_id not in deliver_together_integer:
                        deliver_together_integer.append(package_id)

        for i in deliver_together_integer:

            if self.bucket_table[i][0].get_package_id() == i:
                index = deliver_together_integer.index(i)
                deliver_together_integer[index] = [self.bucket_table[i][0]]

        for i in deliver_together_integer:

            for j in i:

                if j not in self.deliver_together_final:
                    self.deliver_together_final.append(j)

        # Sort the list by package ID using a lambda expression with the package's get_package_id() function
        self.deliver_together_final.sort(key=lambda x: x.get_package_id())

        for package in self.deliver_together_final:
            self.package_addresses_hub.append(package.get_package_address())

    def get_deliver_together_final(self):

        return self.deliver_together_final

    # A list of the addresses associated with the packages that have to go together
    def set_deliver_together_final_addresses(self):

        for i in self.get_deliver_together_final():
            self.deliver_together_final_addresses.append(i.get_package_address())

    def get_deliver_together_final_addresses(self):

        return self.deliver_together_final_addresses

    # Used primarily to extract the time in packages that have a note where it says it will be delayed and will arrive
    # at x time.
    def get_package_time(self, time_string):

        date_time = datetime(year=2000, month=1, day=1, hour=8, minute=0, second=0)
        time_hour = 0
        time_minute = 0
        hour_minute = []
        if 'PM' not in time_string and 'Delayed' in time_string:

            time_string = time_string.strip(' amAM')

            time_string = time_string.split(':')

            if ' ' in time_string[0]:
                time_hour = int(time_string[0].split(' ')[-1])
                time_minute = int(time_string[1])

            # hour_minute = [time_hour, time_minute]

            if time_hour < 8:
                time_hour = 23

            date_time = datetime(year=2000, month=1, day=1, hour=time_hour, minute=time_minute, second=0)

        else:

            if type(time_hour) != int:
                time_string = time_string.strip(' pmPM')
                time_string = time_string.split(':')
                time_hour = int(time_string[0]) + 12
                time_minute = int(time_string[1])

            # hour_minute = [time_hour, time_minute]

            if time_hour < 8:
                time_hour = 23
            date_time = datetime(year=2000, month=1, day=1, hour=time_hour, minute=time_minute, second=0)

        return date_time

    # Handles the unloading of a truckload of packages
    def deliver_packages(self, truck):

        # Loop until the truck is empty
        while truck.get_packages():

            # Sets the truck's current location so the distance and time can be calculated
            current_location = truck.get_current_location()

            package_distance = self.distance_table.get_min_distance(current_location, truck.get_packages())
            next_package = package_distance[0]
            distance = package_distance[1]

            # Keep track of time passed, distance travelled, and then unload the package and update it's status to
            # delivered and set the delivery time in the package object
            truck.update_time(distance)
            truck.update_distance_travelled(distance)
            truck.unload_package(next_package)

            # Append log of the time and total mileage to the truck's time_mileage list
            truck.update_time_mileage()

            # Set the location to currently delivered package's delivery address so that the next iteration can
            # calculate the distance travelled/time passed based on the new directions
            truck.set_current_location(next_package.get_package_address())

        if not truck.get_packages():

            # If there are no more packages at the hub, do not count mileage back to the hub
            self.refresh_package_status()
            if self.get_packages_to_deliver():

                # If more packages need to be loaded at the hub, return the truck to the hub and add the time to get
                # there and add the distance travelled back to the hub
                back_to_hub = self.distance_table.get_distance_between_two_points(truck.get_current_location(), self.hub)
                truck.update_distance_travelled(back_to_hub)
                truck.update_time(back_to_hub)
                truck.set_current_location(self.hub)

    def set_all_packages_no_gaps(self):

        # The hash table could have empty buckets if there isn't a package ID associated with a bucket index. This
        # strips the hash table's list to only a list of packages with no empty buckets.
        for bucket in self.bucket_table:

            if bucket:
                self.all_packages_no_gaps.append(bucket[0])

    def all_packages_no_gaps_remove(self, package):

        self.all_packages_no_gaps.remove(package)

    def get_all_packages_no_gaps(self):

        return self.all_packages_no_gaps

    def set_try_to_load(self, package):

        self.try_to_load.append(package)

    def get_try_to_load(self):

        return self.try_to_load

    def set_try_to_load_addresses(self, package):

        self.try_to_load_addresses.append(package)

    def get_try_to_load_addresses(self):

        return self.try_to_load_addresses

    # Given a list of packages, takes their addresses and sorts the addresses in the most optimal delivery order
    def next_delivery_address(self, package_list, truck_number):

        # Orders the list of addresses by the next closest address starting with the hub
        next_address = []
        point_one = self.hub
        next_address.append(point_one)
        for i in package_list:

            # Excludes packages that can only be on truck 2 if truck 1 is the truck being evaluated.
            if truck_number == 1 and 'Can only be on truck 2' in i.get_package_note():

                continue

            status = i.get_package_status()
            address = i.get_package_address()
            if 'Loaded' not in status and 'Delivered' not in status:

                shortest_distance = 999999

                if address in next_address:
                    continue

                distance = self.distance_table.get_distance_between_two_points(point_one, address)

                if distance < shortest_distance:

                    if address not in next_address:
                        shortest_distance = distance
                        next_address.append(address)

                point_one = address

        return next_address

    # Given an order list of addresses, load them onto a truck if there is room left
    def best_load(self, address_list, truck):

        # Loop through each delivery address
        for i in address_list:

            # If the current truck is not yet full
            if len(truck.get_packages()) < 16:

                # If the address is found in the list of packages' addresses
                if i in self.get_try_to_load_addresses():

                    # Loop through all packages that could be loaded
                    for j in self.get_try_to_load():

                        # If the address matches the address of a package
                        if i in j.get_package_address():

                            # If that package is not already loaded onto the truck and isn't loaded anywhere else and
                            # wasn't already delivered
                            if j not in truck.get_packages() and 'Loaded' not in j.get_package_status() and \
                                    'Delivered' not in j.get_package_status():

                                # Load the package
                                truck.load_package(j)

    def start_simulation(self):

        self.set_all_packages_no_gaps()
        self.refresh_package_status()

        while self.packages_to_deliver and not self.truck_1.packages and not self.truck_2.packages:

            self.nearest_neighbor()
            self.refresh_package_status()

    # Self-Adjusting Algorithm.
    def nearest_neighbor(self):

        # Algorithm to determine the most efficient truck loading at the hub

        # Refresh list of delayed packages and other packages that have the same address
        # Runs twice so that it can account for packages that weren't marked as delayed until the end and reevaluates
        # earlier packages in the list
        for i in range(2):
            self.set_delayed_package_lists()

        # 1. Are there any trucks at the hub? If so, do they have any room left?
        if (self.truck_1.get_current_location() == self.hub and not self.truck_1.is_full()) \
                or (self.truck_2.get_current_location() == self.hub and not self.truck_2.is_full()):

            # If Truck 1 is at the hub and not full, remove any delays if the time condition is met
            if self.truck_1.get_current_location() == self.hub:
                self.remove_delay(self.truck_1)

            # If Truck 2 is at the hub and not full, remove any delays if the condition is met
            if self.truck_2.get_current_location() == self.hub:
                self.remove_delay(self.truck_2)

        # If there are no trucks at the hub or all trucks at the hub are full, stop further checking
        else:

            return False

        # Now comes the checking process for packages to load

        # Does the package have a deadline? If so try to load it first. If any other eligible packages have the same
        # address, add those packages too. If the note says it has to be delivered with other packages, add all of those
        # to the truck too. If there's not enough room on the current truck for all of the same address and/or delivered
        # together packages, try putting them on the other truck.

        # Temporary list to hold a load of packages that may be added to one of the trucks
        new_load = []
        for package in self.get_try_to_load():

            if 'Loaded' in package.get_package_status() or 'Delivered' in package.get_package_status():
                continue
            note = package.get_package_note()

            deadline = package.get_package_deadline()
            address = package.get_package_address()

            # Keep track of all unique addresses in try to load
            if address not in self.get_try_to_load_addresses():
                self.set_try_to_load_addresses(address)

            # Start with packages that have a deadline to meet
            if 'EOD' not in deadline:

                # Gather the packages that have to go together first
                if 'Must be delivered with' in note:

                    for i in self.get_deliver_together_final():

                        if i not in new_load:

                            new_load.append(i)

                            if i in self.get_all_packages_no_gaps():
                                self.all_packages_no_gaps_remove(i)

                        else:

                            continue

            # If any package in the try to load list has the same address as a package on the load, add it to the load
            # to keep them grouped together.
            if address in self.get_deliver_together_final_addresses() and package not in new_load:

                new_load.append(package)

                if package in self.get_all_packages_no_gaps():
                    self.all_packages_no_gaps_remove(package)

        # Determines which truck to use for the initial set of packages that have to be delivered together. This is
        # based on how much room is left on the truck
        if not self.truck_1.is_full() and (len(self.truck_1.get_packages()) - 16) <= len(new_load):

            for i in new_load:

                if i not in self.truck_1.get_packages():
                    self.truck_1.load_package(i)

        elif not self.truck_2.is_full() and (len(self.truck_2.get_packages()) - 16) <= len(new_load):

            for i in new_load:

                if i not in self.truck_2.get_packages():
                    self.truck_2.load_package(i)

        # Calls the next_delivery_address function to find the Nearest Neighbor, by always going to the closest location
        # first
        delivery_order_1 = self.next_delivery_address(self.get_try_to_load(), 1)
        delivery_order_2 = self.next_delivery_address(self.get_try_to_load(), 2)

        self.best_load(delivery_order_1, self.truck_1)
        self.best_load(delivery_order_2, self.truck_2)

        self.deliver_packages(self.truck_1)
        self.deliver_packages(self.truck_2)
