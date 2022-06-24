import itertools
from itertools import combinations, permutations


# Creates a refined list of distance lists.

# Each address is assigned an id and contains
# a list of all distances between itself and
# all other locations.

# The id of an address directly correlates
# to the index of another address' list to
# view the distance between the two.
class Distances:

    # Distance object requires a list of lists
    # that is obtained from the distances csv
    def __init__(self, list_of_lists):

        # Create a local list variable to hold
        # the raw distance data.
        self.lists = list_of_lists

        # Initialize a local variable that
        # will hold the refined/preferred
        # data based on the data found in
        # the previous list variable.
        self.addresses = []

        # Initialize a dictionary that will
        # store the address string as the
        # key and it's generated id as the
        # value.
        self.key = []
        self.value = []
        self.new_dict = dict

        # Index variable to keep track of
        # the first index in the 2D list.
        index = 0

        # Loop through each address in the
        # raw address format.
        for i in self.lists:
            # Each address contains a leading
            # space that needs to be stripped
            # for convenience.
            self.lists[index][0] = self.lists[index][0].lstrip()

            # Expand refined list to accept
            # a new entry.
            self.addresses.append([])

            # At the current index, append the
            # address id number (based on index)
            # and append the address string.
            self.addresses[index].append(index)
            self.addresses[index].append(i[0])

            # Increment the index variable to
            # move on to the next address in the
            # list.
            index += 1

        # Create variable to keep track of the
        # index in the raw list since it doesn't
        # have id's to use.
        index = 0

        # Loop through and add the first distance
        # to each address list.
        for i in self.addresses:

            for j in range(len(self.lists[i[0]]) - 1):
                # Append the missing distance data
                # to the current address in the
                # refined list.

                # It was previously omitted in the
                # provided raw list so as to prevent
                # duplicate data.
                i.append(self.lists[index][j + 1])

            # Increment the index to prepare the next
            # address in the list.
            index += 1

        for i in self.addresses:

            # The range is determined by the length
            # of the final address list -1 to omit
            # the address string located at index 0.
            for j in range(i[0] + 1, len(self.lists[-1]) - 1):
                i.append(self.lists[j][i[0] + 1])

        # Populate the dictionary to contain key/value
        # pairs of address name and id. This will allow
        # a function to take two addresses and return
        # the distance between them.
        for i in self.addresses:
            self.key.append(i[1])
            self.value.append(i[0])
        self.new_dict = dict(zip(self.key, self.value))

    # Provided 2 points in string format, obtains the value
    # associated with that string key and then gets the
    # corresponding distance from the addresses table.

    # 2 is added to the second provided index because the
    # addresses table's first two indices are an id and an
    # address string. The actual distances begin at index
    # 2.
    def get_distance_between_two_points(self, point_one, point_two):

        p1 = int(self.new_dict[point_one])
        p2 = int(self.new_dict[point_two])
        distance = float(self.addresses[p1][p2 + 2])

        return distance

    def add_new_location(self, address):

        if address not in self.addresses:
            self.addresses.append([])
            last_address_index = self.addresses[-2][0]
            self.addresses[-1].append(last_address_index)
            self.addresses[-1].append(address)

            self.new_dict[address] = self.addresses[-1][0]

    def get_min_distance(self, location, package_list):

        available_packages = []
        for package in package_list:

            if package:
                available_packages.append([package,
                                           self.get_distance_between_two_points(location,
                                                                                package.get_package_address())])

        min_distance = min(available_packages, key=lambda x: x[1])

        return min_distance

    def sort_nearest_neighbor(self, package_list):

        hub = '4001 South 700 East'
        unsorted_list = package_list

        next_address = []
        point_one = hub
        next_address.append(point_one)
        for i in unsorted_list:

            address = i.get_package_address()

            shortest_distance = 999999

            if address in next_address:
                continue

            distance = self.get_distance_between_two_points(point_one, address)

            if distance < shortest_distance:

                if address not in next_address:
                    shortest_distance = distance
                    next_address.append(address)

            point_one = address

        if hub in next_address:

            next_address.remove(hub)

        return next_address
