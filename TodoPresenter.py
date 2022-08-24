import platform
import os
from numbers import Number
from TodoController import ToDoController

"""
 Classe que manipula a interface que será apresentada ao usuário.
 
 @author Herik Silva
"""
class TodoPresenter:
    __messageAlert: str
    __todoController: ToDoController
    __commands: list
    __isRunning: bool

    def __init__(self):
        self.__todoController = ToDoController("ToDo.db")
        self.__commands = [self.closeProgram, self.checkToDo, self.newTodo, self.removeToDo]
        self.__messageAlert = "Sem Avisos"
        self.__isRunning = True

    def __clear(self):
        """
        Limpa a interface CLI.
        """
        if(platform.system() == "Windows"):
            os.system("cls")
        else:
            os.system("clear")

    def selectCommand(self, commandNumber: Number):
        """
        Seleciona o comando que será executado e o executa.
        @param int commandNumber: número do comando.
        """
        if(commandNumber < self.__commands.__len__()):
            self.__commands[commandNumber]()
        else:
            self.__messageAlert = "Opção inválida!"

    def menu(self):
        """
        Exibe o menu de opções juntamente com a lista de tarefas e uma mensagem
        de alerta.
        """
        while(self.__isRunning):
            commandNumber: Number

            self.__clear()
            print(self.__messageAlert)

            print("\n| Lista de Tarefas")
            self.__todoController.showToDo()

            print("\n| Lista de Comandos")
            print("1 - Marcar/Desmarcar como Feito")
            print("2 - Nova Tarefa")
            print("3 - Remover Tarefa")
            print("0 - Fechar Programa")

            commandNumber = int(input("Escolha um dos comandos acima: "))
            self.__clear()
            self.selectCommand(commandNumber)
    
    def closeProgram(self):
        """
        Finaliza a execução do programa.
        """
        self.__isRunning = False

    def checkToDo(self):
        """
        Interface que exibe as tarefas para marcar/desmarcar como feitas.
        """
        goToMain = False
        while(not goToMain):
            if(not self.__todoController.isEmpty()):
                todoId: Number

                self.__todoController.showToDo()

                print("\n0 - Voltar ao Menu")

                todoId = int(input("\n| Selecione uma das tarefas acima para marcar/desmarcar como feita: "))

                if(todoId > 0 and todoId <= self.__todoController.numberOfToDos()):
                    todoDescription = self.__todoController.checkToDo(todoId-1)
                    self.__messageAlert = "A Tarefa " + todoDescription + " foi marcada/desmarcada como feita!"                
                elif(todoId == 0):
                    goToMain = True
                else:
                    self.__messageAlert = "Opção inválida!"
            else:
                goToMain = True
                self.__messageAlert = "Sem Tarefas.\nExperimente criar uma nova tarefa."
            
            self.__clear()

    def newTodo(self):
        """
        Interface de criação de uma nova tarefa.
        """
        description = input("Descreva a tarefa: ")

        if(description.__len__() > 0):
            self.__todoController.insert(description)
            self.__messageAlert = "A Tarefa " + description + " foi criada!"

    def removeToDo(self):
        """
        Interface que exibe as tarefas cadastradas no sistema, permitindo que o usuário
        as remova.
        """
        if(not self.__todoController.isEmpty()):
            print("| Remover Tarefa")
            self.__todoController.showToDo()
            print("0 - Voltar ao Menu")

            index = int(input("\nSelecione uma das tarefas acima para remover: "))
            if(index > 0 and index <= self.__todoController.numberOfToDos()):
                removedTodo = self.__todoController.removeToDo(index)
                self.__messageAlert = "A Tarefa " + removedTodo.getDescription() + " foi removida!"
            elif(index > self.__todoController.numberOfToDos()):
                self.__messageAlert = "Opção inválida!\nA remoção foi cancelada"

        else:
            self.__messageAlert = "Sem Tarefas para remover"