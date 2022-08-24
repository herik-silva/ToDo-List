from numbers import Number
from pydoc import describe
from tabnanny import check
from xmlrpc.client import Boolean

"""
 Classe que implementa uma tarefa(ToDo).

 @author Herik Silva
"""
class ToDo:
    __id: int
    __description: str
    __checked: bool

    def __init__(self, description: str):
        self.__description = description
        self.__checked = False

    @classmethod
    def initWithDB(self, id: int, description: str, checked: bool):
        """
        Cria um objeto ToDo que veio do banco de dados.
        @param int id: idêntificador da tarefa.
        @param str description: descrição da tarefa.
        @param bool checked: booleano que representa se a tarefa está ou não marcada como feita.
        @return retorna uma instância de um ToDo.
        """
        toDo = ToDo(description)
        toDo.setId(id)
        toDo.setChecked(checked)

        return toDo

    def checkToDo(self):
        """
        Marca/Desmarca a tarefa como feita.
        """
        self.__checked = not self.__checked
        print(self.__description, "Foi marcado: ",self.__checked)

    def setDescription(self, newDescription: str):
        self.__description = newDescription
    
    def getDescription(self) -> str:
        return self.__description

    def getId(self) -> int:
        return self.__id

    def setId(self, newId: int):
        self.__id = newId

    def setChecked(self, checked: bool):
        self.__checked = checked

    def getChecked(self) -> bool:
        return self.__checked