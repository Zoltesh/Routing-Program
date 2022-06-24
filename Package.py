class Package:

    def __init__(self, p_id, address, city, state, zip_code, deadline, mass, note='', status='', loaded='', delivered=''):

        self.package_id = int(p_id)
        self.package_address = address
        self.package_city = city
        self.package_state = state
        self.package_zip = zip_code
        self.package_deadline = deadline
        self.package_mass = mass
        self.package_note = note
        self.package_status = status
        self.package_loaded = loaded
        self.package_delivered = delivered
        self.package_hub_status = 'At Hub'
        self.package_loaded_status = 'Loaded'
        self.package_delivered_status = 'Delivered'

        # This keeps the package note information because the Delivery object will overwrite the note if it had
        # 'Delayed' or 'Wrong address' in the note
        self.retain_package_note = note

    def set_package_id(self, p_id):

        self.package_id = int(p_id)

    def get_package_id(self):

        return self.package_id

    def set_package_address(self, address):

        self.package_address = address

    def get_package_address(self):

        return self.package_address

    def set_package_city(self, city):

        self.package_city = city

    def get_package_city(self):

        return self.package_city

    def set_package_state(self, state):

        self.package_state = state

    def get_package_state(self):

        return self.package_state

    def set_package_zip(self, zip_code):

        self.package_zip = zip_code

    def get_package_zip(self):

        return self.package_zip

    def set_package_deadline(self, deadline):

        self.package_deadline = deadline

    def get_package_deadline(self):

        return self.package_deadline

    def set_package_mass(self, mass):

        self.package_mass = mass

    def get_package_mass(self):

        return self.package_mass

    def set_package_note(self, note):

        self.package_note = note

    def get_package_note(self):

        return self.package_note

    def set_package_status(self, status):

        self.package_status = status

    def get_package_status(self):

        return self.package_status

    def set_package_loaded(self, time_loaded):

        self.package_loaded = time_loaded

    def get_package_loaded(self):

        return self.package_loaded

    def set_package_delivered(self, time_delivered):

        self.package_delivered = time_delivered

    def get_package_delivered(self):

        return self.package_delivered

    # Get this list to display information for a package that is still at the hub
    def get_hub_status(self):

        if 'Delayed' in self.retain_package_note:
            return [self.get_package_id(), self.get_package_address(), self.get_package_deadline(),
                    self.get_package_city(), self.get_package_zip(), self.get_package_mass(), self.retain_package_note]

        else:

            return [self.get_package_id(), self.get_package_address(), self.get_package_deadline(),
                    self.get_package_city(), self.get_package_zip(), self.get_package_mass(), self.package_hub_status]

    # Get this list to display information for a package that has been loaded
    def get_loaded_status(self):

        return [self.get_package_id(), self.get_package_address(), self.get_package_deadline(), self.get_package_city(),
                self.get_package_zip(), self.get_package_mass(), self.package_loaded_status,
                self.get_package_loaded()]

    # Get this list to display information for a package that has been delivered
    def get_delivered_status(self):

        return [self.get_package_id(), self.get_package_address(), self.get_package_deadline(), self.get_package_city(),
                self.get_package_zip(), self.get_package_mass(), self.package_delivered_status,
                self.get_package_delivered()]

    # This is used when a new package is inserted into the hash table from user inputs or hardcoded values
    def set_package_all(self, package):

        self.package_id = package.get_package_id()
        self.package_address = package.get_package_address()
        self.package_city = package.get_package_city()
        self.package_state = package.get_package_state()
        self.package_zip = package.get_package_zip()
        self.package_deadline = package.get_package_deadline()
        self.package_mass = package.get_package_mass()
        self.package_note = package.get_package_note()
        self.package_status = package.get_package_status()
        self.package_delivered = package.get_package_delivered()

    # This returns package information in a single list of strings
    def get_package_value(self):

        return [self.get_package_id(), self.get_package_address(), self.get_package_city(), self.get_package_state(),
                self.get_package_zip(), self.get_package_deadline(), self.get_package_mass(), self.get_package_note(),
                self.get_package_status(), self.get_package_delivered()]
