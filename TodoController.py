from numbers import Number
from Database import Database
from ToDo import ToDo

"""
 Classe que implementa o controller de ToDo.
 Essa classe é o intermediario entre a camada
 onde apresenta e captura os dados enviados pelo usuário
 e o banco de dados.
 A classe ToDoController recebe os dados da classe ToDoPresenter e 
 realiza suas operações.

 @author Herik Silva.
"""
class ToDoController:
    __toDoList: list[ToDo]
    __database: Database
    __tableName: str

    def __init__(self, dbName: str):
        self.__toDoList = []
        self.__database = Database(dbName)
        self.__tableName = "ToDo"

        try:
            auxList = self.__database.select("ToDo", "%")
            for toDo in auxList:
                newTodo = ToDo.initWithDB(toDo[0],toDo[1], toDo[2])
                self.__toDoList.append(newTodo)

        except:
            self.__database.createTable("ToDo", ["id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, checked BOOL"])

    def numberOfToDos(self) -> int:
        """
        Retorna a quantidade de tarefas na lista.
        @return tamanho da list toDoList.
        """
        return self.__toDoList.__len__()

    def insert(self, description: str):
        """
        Insere uma nova tarefa na lista de tarefa.
        @param str description: descrição da nova tarefa.
        """
        toDo = ToDo(description)
        toDoId = self.__database.insert(self.__tableName, [toDo.getDescription(), toDo.getChecked()])
        toDo.setId(toDoId)

        self.__toDoList.append(toDo)

    def showToDo(self):
        """
        Exibe a lista de tarefa.
        """
        index = 1
        for toDo in self.__toDoList:
            if(not toDo.getChecked()):
                print(index, "- [ ]", toDo.getDescription())
            else:
                print(index, "- [x]", toDo.getDescription())

            index += 1
        

    def removeToDo(self, index: Number) -> ToDo:
        """
        Remove e retorna o item removido.
        @return ToDo
        """
        removedTodo = self.__toDoList.pop(index-1)
        self.__database.remove(self.__tableName, removedTodo.getId())

        return removedTodo

    def checkToDo(self, id: Number) -> str:
        """
        Marca/desmarca a tarefa como feita.
        @param int id: idêntificador da tarefa
        @return retorna a descrição da tarefa.
        """
        selectedToDo = self.__toDoList[id]
        selectedToDo.checkToDo()
        self.__database.update(self.__tableName, selectedToDo)
        self.isEmpty
        return selectedToDo.getDescription()

    def isEmpty(self) -> bool:
        """
        Verifica se a lista de tarefas esta vazia.
        @return true se a lista estiver vazia. Caso contrário, retorna um false.
        """
        return self.__toDoList.__len__() == 0