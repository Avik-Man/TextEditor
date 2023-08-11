from tkinter import *
from tkinter import filedialog

characters = 0
words = 0
class Rope(object):                                                    #Rope ADT
    def __int__(self,value ="",parent = None):
        if isinstance(value,str):
            if parent == None and value == "":
                self.right=None
                self.left = None
                self.weight =0
                self.parent = None

            elif parent== None:
                self.right = Rope(value[self.weight:],self)
                self.left = Rope(value[:self.weight],self)
                self.weight = len(value)//2
                self.parent = None

            else:
                self.right = None
                self.left = None
                self.weight = 0
                self.value = value
                self.parent = parent
        else:
            raise TypeError("Enter only strings please")

    def search_node(self,index):                                                    #function to search string
                if self.weight <=index and self.right != None:
                    return self.right.search_node(index -self.weight)
                elif self.left!=None:
                    return self.left.search_node(index);

                return [self,index]
    def concatenation(self,node1,node2):                                          #function to concatenate 2 strings
            self.right = node2
            self.left = node1
            self.weight = self.weights(self.left)
            node1.parent = self
            node2.parent = self
            return self

    def Indexing(self,index):                                                     #Function to find index of a character
            if self.weight <=index and self.right != None:
                return self.right.Indexing(index - self.weight)

            elif self.left != None:
                return self.left.Indexing(index)

            else:
                return self.value[index]

    def weights(self,node):                                                       #Function to find value at parent node, ie sum of elements of leaf nodes
            if node.right!=None:
                return node.weight + node.right.weights(node.right)
            else:
            	return len(node.value)
    def split(self,index):                              
            node, ind = self.search_node(index)
            node1 = Rope(node.value[:ind],node)
            node2 = Rope(node.value[ind:],node)
            node.value = ""
            node.weight = len(node1.value)
            node.right = node2
            node.left = node1
            return node
    def check_balancing(self,node,char):
            if node.weight<=(0.45*char) or (node.left==None and node.right==None):
                return (True,None)
            else:
                char = char-node.weight
                check,empty_node = node.right.check_balancing(node.right,char)
                return (False,node)

    def insertion(self,s,characters):
            characters += len(s)
            check,node = self.check_balancing(self,characters)
            new_self = Rope()
            string_to_connect = Rope(s,new_self)
            if (check==True):
                new_self = new_self.concatenation(self,string_to_connect)
                return new_self,characters
            elif (check==False):
                new_self = new_self.concatenation(node.right,string_to_connect)
                new_self.parent=node
                node.right = new_self
                return self, characters

    def deletion(self,index_i,index_j,characters):                          #function to delete a string
            for char in range(index_i,index_j):
                node,i = self.search_node(char)
                print(i)
                if node is not None:
                    print(node.value)
                    characters -= len(node.value)
                    node.value = ""
                    node = None
            return self,characters

    def split_node(self,node, s_index):      
            value = node.value
            node1 = Rope(value[:s_index])
            node2 = Rope(value[s_index:])
            return node1,node2

    def edit(self,index,str1,characters):                         #Funcion to modify a string
            node,i = self.search_node(index)
            node1 = Rope(node.value[:i],node)
            node2 = Rope(str1 + node.value[i:],node)
            node.value = ""
            node.weight = len(node1.value)
            node.left = node1
            node.right = node2
            characters += len(str1)
            return self,characters

    def print_rope(self,characters):                           #Function to print the string
            result = ""
            for i in range(characters):
                node,ind = self.search_node(i)
                result += node.value[ind]
            return result


def add_first(starting_string):
    document_rope = Rope(starting_string)
    characters = len(starting_string)
    return document_rope,characters


