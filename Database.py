import sqlite3

from ToDo import ToDo

"""
 Classe que implementa um Banco de Dados, realizando
 a conexão e toda a manipulação de forma simples.
 @author Herik Silva

 obs: Os métodos insert, select eupdate estão funcionando apenas na tabela de
 tarefas por enquanto, pois utilizam apenas os campos da mesma.
"""

class Database:
    __databaseName: str

    def __init__(self, databaseName: str):        
        self.__databaseName = databaseName

    def __prepareFields(self, stringSql: str,fields: list[any], useSymbols: bool) -> str:
        """
        Prepara uma string com todos os campos do banco de dados e a retorna.
        @param str stringSql: string inicial da consulta SQL sem os campos
        @param list[any] fields: lista de campos da tabela.
        @param bool useSymbols: define se usara o simbolo ? na posição onde ficara o valor do campo
        @return retorna uma string com a consulta SQL completa.
        """
        numberOfFields = fields.__len__()
        if(useSymbols):
            while(numberOfFields > 1):
                stringSql += "?,"
                numberOfFields -= 1
        
            stringSql += "?)"
        else:
            index = 0
            while(numberOfFields > 1):
                stringSql += fields[index] + ","
                numberOfFields -= 1
                index += 1

            stringSql += fields[index] + ")"

        return stringSql

    def getConnection(self):
        """
        Retorna uma conexão com banco de dados
        """
        return sqlite3.connect(self.__databaseName)

    
    def createTable(self, tableName: str, fields: list[str]):
        """
        Cria uma tabela no banco de dados.
        """
        stringSql = "CREATE TABLE " + tableName + " ("
        connection = self.getConnection()
        cursor = connection.cursor()

        stringSql = self.__prepareFields(stringSql, fields, False)
        
        cursor.execute(stringSql)
        cursor.close()
        connection.commit()
        connection.close()

    def insert(self, tableName: str, values: list[any]):
        """
        Insere valores em uma tabela
        @param str tableName: nome da tabela
        @param list values: valores que serão inseridos
        @parm retorna o id do ultimo item inserido.
        """
        stringSql = "INSERT INTO " + tableName + "(description, checked) VALUES(?,?)"
        connection = self.getConnection()
        cursor = connection.cursor()

        lastId = cursor.execute(stringSql, values).lastrowid

        cursor.close()
        connection.commit()
        connection.close()

        return lastId

    def select(self, tableName: str, value: str) -> list[ToDo]:
        """
        Recupera tarefas do banco de dados.
        @param str tableName: nome da tabela
        @param str value: nome da tarefa
        @return lista contendo todas as tarefas encontradas.
        """
        toDo: list
        stringSql = "SELECT * FROM " + tableName + " WHERE description LIKE ?"
        connection = self.getConnection()
        cursor = connection.cursor()
        
        cursor.execute(stringSql, [value])
        
        toDo = cursor.fetchall()
        cursor.close()
        connection.close()

        return toDo

    def remove(self, tableName: str, id: int):
        """
        Remove uma item do banco de dados.
        @param str tableName: nome da tabela
        @param int id: indêntificador do item.
        """
        stringSql = "DELETE FROM " + tableName + " WHERE id = ?"
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(stringSql, [id])
        
        connection.commit()
        cursor.close()
        connection.close()

    def update(self, tableName, toDo: ToDo):
        """
        Atualiza um item do banco de dados.
        @param str tableName: nome da tabela
        @param ToDo toDo: tarefa que será atualizada
        """
        stringSql = "UPDATE " + tableName + " SET checked = ? WHERE id = ?"
        connection = self.getConnection()
        cursor = connection.cursor()

        cursor.execute(stringSql, [toDo.getChecked(), toDo.getId()])
        connection.commit()

        cursor.close()
        connection.close()