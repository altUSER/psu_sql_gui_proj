from .dbConnection import cursor, conn

class Master():

    def __init__(self, kind_of_activity:str = None, name: str = None, address: str = None, phone_number: str = None):
        self.__id = self.__getMaxId() + 1
        self.kind_of_activity = kind_of_activity
        self.name = name
        self.address = address
        self.phone_number = phone_number

    

    def getById(self, id):
        result =  cursor.execute(f'SELECT * FROM masters WHERE (id={id});').fetchone()
        
        if not result == None:
            self.__id = result[0]
            self.kind_of_activity = result[1]
            self.name = result[2]
            self.address = result[3]
            self.phone_number = result[4]
            return self
        else:
            return None
    
    @classmethod
    def getAll(cls):
        mstr_arr = []

        result = cursor.execute(f'SELECT id FROM masters;').fetchall()

        for mstr_id in result:
            instance = cls()
            mstr_arr.append(instance.getById(mstr_id[0]))
        
        return mstr_arr
    
    def delete(self):
        cursor.execute(f'DELETE FROM masters WHERE id={self.id}')
        conn.commit()
        return self
    
    def getClients(self):
        from .clients import Client

        cl_arr = []

        result =  cursor.execute(f'SELECT id FROM clients WHERE (id_master={self.id});').fetchall()
        
        if not result == None:
            for cl_id in result:
                cl_arr.append(Client().getById(cl_id[0]))
            
            return cl_arr
        else:
            return None

    
    def write(self):
        if self.__inDatabase():
            cursor.execute(f"UPDATE masters SET kind_of_activity = '{self.kind_of_activity}', name = '{self.name}', address = '{self.address}', phone_number = '{self.phone_number}' WHERE id={self.id}")
            conn.commit()
            return self
        else:
            cursor.execute(f"INSERT INTO masters VALUES ('{self.__id}', '{self.kind_of_activity}', '{self.name}', '{self.address}', '{self.phone_number}')")
            conn.commit()
            return self


    def __getMaxId(self):
        return cursor.execute('SELECT MAX(id) FROM masters;').fetchone()[0]
    
    def __inDatabase(self):
        result =  cursor.execute(f'SELECT * FROM masters WHERE (id={self.id});').fetchone()

        if result == None:
            return False
        else:
            return True

    @property
    def id(self):
        return self.__id

    def __str__(self) -> str:
        return str((self.__id, self.kind_of_activity, self.name, self.address, self.phone_number))