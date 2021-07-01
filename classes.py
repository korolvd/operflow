class User:
    def __init__(self, id, name, upload, create):
        self.__id = id
        self.__name = name
        self.__upload = upload
        self.__create = create

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_upload(self):
        return self.__upload

    def set_upload(self, upload):
        self.__upload = upload

    def get_create(self):
        return self.__create

    def set_create(self, create):
        self.__create = create


class Unit:
    def __init__(self, id, type, name, number, status, images):
        self.__id = id
        self.__name = name
        self.__number = number
        self.__status = status
        self.__type = type
        self.__images = images

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_number(self):
        return self.__number

    def set_number(self, number):
        self.__number = number

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def get_images(self):
        return self.__images

    def set_images(self, images):
        self.__images = images

    def add_image(self, image):
        self.__images.append(image)

    def __str__(self) -> str:
        return f'{self.__name} №{self.__number}'


class Flow:
    __units = list()
    __users = list()
    __ids = 1

    def add_user(self, user):
        self.__users.append(user)

    def find_user(self, id):
        rsl = None
        for user in self.__users:
            if user.get_id() == id:
                rsl = user
                break
        return rsl

    def add_unit(self, unit):
        unit.set_id(self.__ids)
        self.__units.append(unit)
        self.__ids += 1

    def index_of(self, id):
        rsl = -1
        for i in range(len(self.__units)):
            if self.__units[i].get_id() == id:
                rsl = i
                break
        return rsl

    def find_by_id(self, id):
        rsl = None
        index = self.index_of(id)
        if index != -1:
            rsl = self.__units[index]
        return rsl

    def find_all(self):
        return self.__units

    def delete(self, id):
        index = self.index_of(id)
        rsl = index != -1
        if rsl:
            self.__units.pop(index)
        return rsl