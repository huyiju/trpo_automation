class FirstClass:

    def chet(self,a,b):
        
        print('Func1')
        res=a/b
        print('result',res)

    """a_1=int(input('param A: '))
    b_1=int(input('param B: '))

    chet(a_1, b_1)"""

    def FRead_Clone(self):
        print('Func2')
        file = open('Proba.txt', 'r')
        ST=file.read()
        
           
        file_2 = open('NEW_file.txt', 'w')
        i=0
        while i<10:
             file_2.write(ST+"\n")
             i=i+1

    #FRead_Clone()

    def Pars(self):
        import requests
        from bs4 import BeautifulSoup

        base_url = "https://litnet.com"

        space = "/ru/reader/nevesta-snezhnogo-demona-zimnii-bal-v-akademii-b193123"

        response = requests.get(base_url + space)

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        conteiner = soup.find("div", {"class":"reader-text font-size-medium"})

        images = conteiner.findAll("p")

        print(len(images))

        for image in images:
                value = image.text
                print (value)
                
                file_3 = open('TEXT.txt', 'w')
                file_3.write(value+"\n")
                
                
             
    #Pars()
    #print("Успешно отработано")


    



   
    
