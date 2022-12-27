#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hashlib
import PySimpleGUI as sg


# In[2]:


print ("The available algorithms are : ", end ="")
print (hashlib.algorithms_guaranteed)


# In[3]:


charset = {
    'numeric': '0123456789',
    'alpha': 'ABC',
    'alpha-numeric': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    'loweralpha':'abcdefghijklmnopqrstuvwxyz',
    'loweralpha-numeric':'abcdefghijklmnopqrstuvwxyz0123456789'
}


# In[4]:


p_dict = {}


# In[5]:


class RainbowTableGenerator:
    def __init__(self,hashing_algo,cset,minlen,maxlen,chainlen):
        self.hashing_algo = hashing_algo
        self.PT = charset[cset]
        self.charset = cset
        self.minlen = int(minlen)
        self.maxlen = int(maxlen)
        self.chainlen = chainlen
        self.permutations = []
        self.Permutations_of_charset = []
    def __init__(self):
        self.permutations = []
        self.Permutations_of_charset= []
        pass
    
    def getPermutations (self):
        return self.permutations
    def getPermutations_of_charset(self):
        return self.Permutations_of_charset
    def findPermutations_of_charset (self,p,i,length):
        if i == length:
            if (''.join(p) not in self.Permutations_of_charset):
                self.Permutations_of_charset.append(''.join(p) )
        else:
            for j in range(i, length):
                # swap
                p[i], p[j] = p[j], p[i]
                self.findPermutations_of_charset(p, i + 1, length)
                p[i], p[j] = p[j], p[i] 
    def findPermutations(self,p, i, length):
        if i == length:
            if (''.join(p) not in self.permutations):
                self.permutations.append(''.join(p) )
        else:
            for j in range(i, length):
                # swap
                p[i], p[j] = p[j], p[i]
                self.findPermutations(p, i + 1, length)
                p[i], p[j] = p[j], p[i] 
    def setValues(self,hashing_algo,cset,minlen,maxlen,chainlen):
        self.hashing_algo = hashing_algo
        self.charset = cset
        self.minlen = int(minlen)
        self.maxlen = int(maxlen)
        self.chainlen = int(chainlen)
    def Hash(self,val):
        if(self.hashing_algo == "sha1"):
            return (hashlib.sha1(str.encode(val)).hexdigest())
        elif (self.hashing_algo == "sha256"):
            return (hashlib.sha256(str.encode(val)).hexdigest())
        elif(self.hashing_algo == "md5"):
            return (hashlib.md5(str.encode(val)).hexdigest())
        
    def reduction_function(self,hashed,size):
        return (hashed[0:size])
    def Generator(self):
        
        self.findPermutations_of_charset (list(charset[self.charset]),0,len(charset[self.charset]))
        
        #checking all the possible combinations of the the selected Charset of provided Min & Max length
        
        for out in range (self.minlen,self.maxlen+1):

            
            for i in range (len(self.Permutations_of_charset)):
            
                self.permutations.clear()

                PT = self.Permutations_of_charset[i][0:out]

                self.findPermutations (list(PT),0,len(PT))
#                 print("SLEF PERMUTATIONs---->",self.permutations)

                for p in range(len(self.permutations)):

#                     print("SLEF PERMUTATIONs---->",self.permutations[p])
                    hashed = self.Hash (self.permutations[p])
                    
#                     print ("SLEF.per---->",self.permutations[p])    
                    if p_dict.get(hashed)== False:
                        p_dict[hashed]  = self.permutations[p]

                    for j in range (int(self.chainlen)):

                        red = self.reduction_function(hashed,out)

                        rehashed = self.Hash (red)
#                         print ("AFTER REDUCTION ---->",red)    
                        if not p_dict.get(rehashed) == False:
                            p_dict[rehashed] = red

                        hashed = rehashed
        f = open("D:/Semester#7/Information Security/rainbowtable.txt", "w")
       
        for key, value in p_dict.items(): 
            f.write('%s:%s\n' % (key, value))
        f.close()
        return p_dict      
        
    def write_to_table():
        pass
    def UI(self):
        
#         sg.theme_previewer()

        sg.theme('DarkBlue15')   # Add a touch of color
        # All the stuff inside your window.
        layout = [  
                    [sg.Text('        Rainbow Table Generator',size=(100,1),font=("Arial",30))],
                    [sg.Text('Hash                    '),sg.Combo(['sha1','md5','sha256'],default_value='md5',key='hash')],
                    [sg.Text('Charset                '),sg.Combo(['numeric','alpha','alpha-numeric','loweralpha','loweralpha-numeric'],default_value='numeric',key='charset')],
                    [sg.Text('Min Len                '), sg.InputText()],
                    [sg.Text('Max Len               '), sg.InputText()],
                    [sg.Text('Chain Count          '), sg.InputText()],
                    [sg.Button('Add Table'), sg.Button('Cancel')],
                    [sg.Text("LINK                     "), sg.Input(key='OUTPUT')], 
                    [sg.Text('----------------------------------------------------------------------------------',size=(50,3))],
                    [sg.Text("PASSWORD TO FIND HASH        "), sg.Input(key='password')] ,
                    [sg.Button('Hash')],
                    [sg.Text("ENTER HASH to FIND PLAINTEXT"), sg.Input(key='Plaintext')] ,
                    [sg.Button('Search')],
                ]
        
                    
        
                    

        # Create the Window
        window = sg.Window('RainBowTableGenerator', layout,size=(800, 600))
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == 'Add Table':
                self.hashing_algo = values['hash']
                self.minlen = int(values[0])
                self.maxlen = int(values[1])
                self.chainlen = int(values[2])
                self.cset = values['charset']
                self.setValues(self.hashing_algo,self.cset,self.minlen,self.maxlen,self.chainlen)
    
                self.Generator()
    
                window['OUTPUT'].update(value="D:/Semester#7/Information Security/rainbowtable.txt")
            if event == 'Hash':
                temp = self.Hash(values['password'])
                window['password'].update(value=str(temp))
            if event == 'Search':
                temp = values['Plaintext']
                
                window['Plaintext'].update(value=str(p_dict[temp]))
        window.close()


# In[6]:


def main():
    
    RBTG = RainbowTableGenerator()
    
    RBTG.UI()

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




