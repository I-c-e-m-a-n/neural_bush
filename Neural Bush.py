#Neural Bush development
import everything as ev
import bush_helper as bh
import bush_interpreter as bi

class Node:
    def __init__(self, value):
        #setting up neuron
        self.parents = []
        self.parentsStrength = []
        self.children = []
        self.childrenStrength = []
        
        #giving it values to hold
        self.value = value
        return
        
    #getters 
    def getParents(self):
        retTup = []
        for i in range(len(self.parents)):
            retTup.append([self.parents[i], self.parentsStrength[i]])
        return retTup
    
    def getChildren(self):
        retTup = []
        for i in range(len(self.children)):
            retTup.append([self.children[i], self.childrenStrength[i]])
        return retTup
    
    def getId(self):
        return hex(id(self))
    
    def getValue(self):
        return self.value
    
    #setters 
    def addParents(self, parent, parentStrength):
        self.parents.append(parent)
        self.parentsStrength.append(parentStrength)
        
    def addChildren(self, child, childStrength):
        self.children.append(child)
        child.addParents(self, childStrength)
        self.childrenStrength.append(childStrength)
        
    def changeParVal(self, ind, strength):
        self.parentsStrength[ind] = strength
    
    def changeChiVal(self, ind, strength):
        self.childrenStrength[ind] = strength
        
#adds child to node with a value from domain
def addChild(node, domain):
    value = ev.randel(domain)
    node.addChildren(Node(value), ev.sigmoid(ev.random(0, 1000)/1000))
    domain.remove(value)
    return ev.deep(node), domain

#backend training for the bush
def bushTraining(roots, inputs, outputs, domain, iterations):
    iters = 0
    rest = []
    while iters < iterations:
        cur = None
        inp = ev.randel(inputs)
        ind3 = 0
        for i in roots:
            if i.getValue() == inp:
                cur = i
                ind3 = roots.index(cur)
        if not cur:
            raise Exception("invalid input")
        
        if not roots[ind3].getChildren() and len(domain):
            roots[ind3], domain = addChild(cur, domain)
        

        saved = None
        strong = 0
        ind2 = 0
        while not saved:
            children = roots[ind3].getChildren()
            for child in children:
                if child[1] > strong:
                    strong = child[1]
                    saved = child[0]
                    ind2 = roots[ind3].getChildren().index(child)
            if not saved and len(domain):
                roots[ind3], domain = addChild(cur, domain)
            elif not len(domain) and not saved:
                child = ev.randel(ev.randel(roots).getChildren())
                temp = ev.sigmoid(ev.random(0, 1000)/1000)
                roots[ind3].addChildren(child[0], temp)
                ind2 = roots[ind3].getChildren().index([child[0], temp])
                for child in children:
                    if child[1] > strong:
                        strong = temp
                        saved = child[0]

        cor = saved.getValue() == roots[ind3].getValue() ** 2
        if cor:
            parents = child[0].getParents()
            parInd = parents.index([roots[ind3], strong])
            children2 = roots[ind3].getChildren()
            chiInd = children2.index([child[0], strong])
            
            child[0].changeParVal(parInd, strong + 0.5)
            roots[ind3].changeChiVal(chiInd, strong + 0.5)
        else:
            parents = child[0].getParents()
            parInd = parents.index([roots[ind3], strong])
            children2 = roots[ind3].getChildren()
            chiInd = children2.index([child[0], strong])
            
            child[0].changeParVal(parInd, strong - 0.5)
            roots[ind3].changeChiVal(chiInd, strong - 0.5)
        iters+= 1
    print("iter = " + str(iters))
    return roots, iters

#user testing for the bush
def bushTesting(roots, inputs, outputs, domain, iters):
    while True:
        cur = None
        inp = int(input("Enter Number"))
        print(inp)
        ind3 = 0
        for i in roots:
            if i.getValue() == inp:
                cur = i
                ind3 = roots.index(cur)
        if not cur:
            raise Exception("invalid input")
        
        if not roots[ind3].getChildren() and len(domain):
            roots[ind3], domain = addChild(cur, domain)
        

        saved = None
        strong = 0
        ind2 = 0
        while not saved:
            children = roots[ind3].getChildren()
            for child in children:
                if child[1] > strong:
                    strong = child[1]
                    saved = child[0]
                    ind2 = roots[ind3].getChildren().index(child)
            if not saved and len(domain):
                roots[ind3], domain = addChild(cur, domain)
            elif not len(domain) and not saved:
                child = ev.randel(ev.randel(roots).getChildren())
                temp = ev.sigmoid(ev.random(0, 1000)/1000)
                roots[ind3].addChildren(child[0], temp)
                ind2 = roots[ind3].getChildren().index([child[0], temp])
                for child in children:
                    if child[1] > strong:
                        strong = temp
                        saved = child[0]
        print(saved.getValue())
            
        cor = saved.getValue() == roots[ind3].getValue() ** 2
        if cor:
            parents = child[0].getParents()
            parInd = parents.index([roots[ind3], strong])
            children2 = roots[ind3].getChildren()
            chiInd = children2.index([child[0], strong])
            
            child[0].changeParVal(parInd, strong + 0.5)
            roots[ind3].changeChiVal(chiInd, strong + 0.5)
            print("updated conn++\n")
        else:
            parents = child[0].getParents()
            parInd = parents.index([roots[ind3], strong])
            children2 = roots[ind3].getChildren()
            chiInd = children2.index([child[0], strong])
            
            child[0].changeParVal(parInd, strong - 0.5)
            roots[ind3].changeChiVal(chiInd, strong - 0.5)
            print("updated conn--\n")
        
        iters+= 1
        print("iter = " + str(iters))

def main():
    functions = {"add":bh.add,
                 "multiply": bh.multiply,
                 "divide": bh.divide,
                 "exponent": bh.exponent,
                 "root": bh.root}
    inputs = ['0^2', '1^2', '2^2', '3^2', '4^2', '5^2', '6^2',
              '7^2', '8^2', '9^2']
    outputs = [0, 1, 4, 9, 16, 25, 36, 49, 64, 72, 81]
    domain = []
    for key in functions.keys():
        domain.append(key)
    iterations = 4750


    roots = []
    
    for j in inputs:
        roots.append(Node(j))
    
    print(domain)
    for func in domain:
        print(func)
        print(functions[func](3, 3))
#     roots, iters = bushTraining(roots, inputs, outputs, domain, iterations)
#     bushTesting(roots, inputs, outputs, domain, iterations)

if __name__ == '__main__':
    main()