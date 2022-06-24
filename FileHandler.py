from Package import *
from Distances import *
from Hasher import *
import csv

class FileHandler:

    def __init__(self, file_name):

        self.file_name = file_name


    def import_package_file(self):

        # Open the csv file containing the packages and assign a name to the open file object
        with open(self.file_name, 'r') as package_data:
            # Create an an object to allow reading through the file object
            package_file = csv.reader(package_data)

            # Get the total number of packages by summing each line in the reader object
            number_of_packages = sum(1 for i in package_file)

        # Close the file so that the pointer can be reset
        package_data.close()

        # Open the file again
        with open('WGUPS Package File.csv', 'r') as package_data:
            package_file = csv.reader(package_data)

            # Instantiate a hash table with length equal to the number of packages
            hash_table = Hasher()

            # Create a new package object for each item in the reader object by reading through, line by line,
            # and use each line's indices as the package attributes. Then insert each iteration into the hash
            # table.
            for lines in package_file:
                new_package = Package(lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6], lines[7])
                hash_table.insert(new_package.get_package_id(), new_package)

        # Close the file object as it is no longer needed
        package_data.close()

        return hash_table

    def import_distance_file(self):

        distance_file_list = []
        with open('WGUPS Distance Table.csv', 'r') as distance_data:
            distance_file = csv.reader(distance_data)

            i = 0
            for lines in distance_file:
                i += 1
                distance_file_list.append([])

                for columns in range(i):
                    distance_file_list[i - 1].append(lines[columns])

                distance_file_list[i - 1].append(lines[columns + 1])

        distance_data.close()

        distance_list = Distances(distance_file_list)

        return distance_list
