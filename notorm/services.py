from .dbConnection import cursor, conn

class Service():

    def __init__(self, service_name: str = None, price:int = None):
        self.__id = self.__getMaxId() + 1
        self.service_name = service_name
        self.price = price
    

    def getById(self, id):
        result =  cursor.execute(f'SELECT * FROM types_of_services WHERE (id={id});').fetchone()
        
        if not result == None:
            self.__id = result[0]
            self.service_name = result[1]
            self.price = result[2]
            return self
        else:
            return None
    
    @classmethod
    def getAll(cls):
        srv_arr = []

        result = cursor.execute(f'SELECT id FROM types_of_services;').fetchall()

        for srv_id in result:
            instance = cls()
            srv_arr.append(instance.getById(srv_id[0]))
        
        return srv_arr
    
    def getClients(self):
        from .clients import Client

        cl_arr = []

        result =  cursor.execute(f'SELECT id FROM clients WHERE (id_service={self.id});').fetchall()
        
        if not result == None:
            for cl_id in result:
                cl_arr.append(Client().getById(cl_id[0]))
            
            return cl_arr
        else:
            return None

    
    def write(self):
        if self.__inDatabase():
            cursor.execute(f"UPDATE types_of_services SET service_name = '{self.service_name}', price = '{self.price}' WHERE id={self.id}")
            conn.commit()
            return self
        else:
            cursor.execute(f"INSERT INTO types_of_services VALUES ('{self.__id}', '{self.service_name}', '{self.price}')")
            conn.commit()
            return self
    

    def __getMaxId(self):
        return cursor.execute('SELECT MAX(id) FROM types_of_services;').fetchone()[0]
    
    def __inDatabase(self):
        result =  cursor.execute(f'SELECT * FROM types_of_services WHERE (id={self.id});').fetchone()

        if result == None:
            return False
        else:
            return True

    
    @property
    def id(self):
        return self.__id

    def __str__(self) -> str:
        return str((self.__id, self.service_name, self.price))