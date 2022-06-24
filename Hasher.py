# Creates a hash table
class Hasher:

    def __init__(self):

        self.bucket_table = []

        # This is used later in the Lookup
        # class to find a package by providing
        # the associated address
        self.address_list = []

    # Takes the package ID as the key and the entire package object as the item
    def insert(self, key, item):

        if len(self.bucket_table) <= (key + 1):

            for i in range(1 + key - len(self.bucket_table)):
                self.bucket_table.append([])

        bucket = hash(key) % len(self.bucket_table)
        bucket_list = self.bucket_table[bucket]

        for package in bucket_list:

            if package.get_package_id() == key:
                package.set_package_all(item)

            if item.get_package_address() not in self.address_list:
                self.address_list.append(item.get_package_address())

                return True

        bucket_list.append(item)

        if item.get_package_address() not in self.address_list:
            self.address_list.append(item.get_package_address())

        return True

    # Finds a package by passing in the entire package, rather than taking in the ID/Key
    def find(self, item):

        bucket = hash(item.get_package_id()) % len(self.bucket_table)
        bucket_list = self.bucket_table[bucket]

        for package in bucket_list:

            if package.get_package_id() == item.get_package_id():

                if package.get_package_value() == item.get_package_value():
                    return package.get_package_value()

        return None

    # Given a package ID, finds the bucket where that package is located and returns a list of package values
    def find_by_id(self, id):

        bucket = hash(id) % len(self.bucket_table)
        bucket_list = self.bucket_table[bucket]

        for package in bucket_list:

            if package.get_package_id() == id:
                return package.get_package_value()

        return None

    # Locates the bucket where the package is stored and deletes that package if it is a match
    def delete(self, item_id):

        bucket = hash(item_id) % len(self.bucket_table)
        bucket_list = self.bucket_table[bucket]

        for package in bucket_list:

            if item_id == package.get_package_id():
                bucket_list.remove(package)
                return True

        return False

    def get_address_list(self):

        return self.address_list
