from .dbConnection import cursor, conn
from .masters import Master
from .services import Service


class Client():

    def __init__(self, master: Master = None, name:str = None, phone_number:str = None, service:Service = None):
        self.__id = self.__getMaxId() + 1
        self.master = master
        self.name = name
        self.phone_number = phone_number
        self.service = service
    

    def getById(self, id):
        result =  cursor.execute(f'SELECT * FROM clients WHERE (id={id});').fetchone()
        
        if not result == None:
            self.__id = result[0]
            self.master = Master().getById(result[1])
            self.name = result[2]
            self.phone_number = result[3]
            self.service = Service().getById(result[4])
            return self
        else:
            return None
    
    @classmethod
    def getAll(cls):
        srv_arr = []

        result = cursor.execute(f'SELECT id FROM clients;').fetchall()

        for srv_id in result:
            instance = cls()
            srv_arr.append(instance.getById(srv_id[0]))
        
        return srv_arr

    
    def write(self):
        if self.__inDatabase():
            cursor.execute(f"UPDATE clients SET id_master = '{self.master.id}', name = '{self.name}', phone_number = '{self.phone_number}', id_service = '{self.service.id}' WHERE id={self.id}")
            conn.commit()
            return self
        else:
            cursor.execute(f"INSERT INTO clients VALUES ('{self.__id}', '{self.master.id}', '{self.name}', '{self.phone_number}', '{self.service.id}')")
            conn.commit()
            return self
    

    def __getMaxId(self):
        return cursor.execute('SELECT MAX(id) FROM clients;').fetchone()[0]
    
    def __inDatabase(self):
        result =  cursor.execute(f'SELECT * FROM clients WHERE (id={self.id});').fetchone()

        if result == None:
            return False
        else:
            return True

    
    @property
    def id(self):
        return self.__id

    def __str__(self) -> str:
        return str((self.__id, self.master, self.name, self.phone_number, self.service))