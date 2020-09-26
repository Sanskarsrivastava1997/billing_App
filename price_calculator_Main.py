import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang.builder import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import pickle
from kivy.uix.pagelayout import PageLayout
from kivy.config import Config
Builder.load_file("object_tray.kv")
Builder.load_file("label_tray.kv")
Builder.load_file("data_base.kv")
Builder.load_file("welcome_scr.kv")

Config.set('graphics', 'resizable', True)

class label_tray(BoxLayout):
    orientation = "vertical"
    cols = 1
    label_tray=ObjectProperty(None)




    Total_price = 0

    def __init__(self, **kwargs):

        super(label_tray, self).__init__(**kwargs)

        self.list_PN=[]
        self.list_p=[]
        self.dict={}
        self.count=0


    def b1_press(self):
        if len(self.t1.text)<12 and len(self.t2.text)<9:
            text1 = self.t1.text
            text2 = self.t2.text
        else:
            text1 =""
            text2 =""
            print("limit exceed")


        #------------------------
        #for pop_up

        self.layout = GridLayout(cols=1, padding=10)
        self.layout.add_widget(Label(text="Repeated Entry"))
        #------------------------

        if text1 != "" and text2 != "" and text1 not in self.list_PN:

            self.bx.add_widget(object_tray(text1, text2,self.dict))
            self.list_PN.append(text1)
            self.list_p.append(text2)
        else:
            if text1 in self.list_PN:
                self.pop_up=Popup(title="Error",content= self.layout,size_hint=(None,None),size=(200,100))
                self.pop_up.open()
                print(self.list_PN)


        self.auto_update()



        if self.list_PN==[]:
            try:
                self.list_PN=data1[:]
                self.list_p=data2[:]

                for i in range(len(data1)):
                    self.bx.add_widget(object_tray(data1[i], data2[i], self.dict))
                data1.clear()
                data2.clear()
                self.auto_update()


            except:
                print("load")




    def total_price(self, total, so,dict):

        self.count=dict

        if so == True:
            self.Total_price += total
        else:
            self.Total_price -= int(total)


    def auto_update(self):
        self.t1.text = ""
        self.t2.text = ""
        self.l1.text = "total -->" + str(self.Total_price)

        if self.t4.text:

            if int(self.t4.text) < self.Total_price:
                self.l3.text = "limit exceed"
                self.l2.text = "loss  -->  " + str(int(self.t4.text) - self.Total_price)
                try:
                    lk=(int(self.t4.text) - self.Total_price)+((int(self.t3.text) * self.Total_price) / 100)
                except:
                    return
                if self.t3.text and self.Total_price != 0 and lk<0:
                    self.l2.text = "loss  -->  " + str(int(lk))
                else:
                    self.l2.text = "BL  -->  " + str(int(lk))

            else:
                self.l3.text = "Status"
                self.l2.text = "BL  -->  " + str(int(self.t4.text) - self.Total_price)
                if self.t3.text and self.Total_price != 0:
                    self.l2.text = "BL  -->  " + str(int(int(self.t4.text) - self.Total_price)+((int(self.t3.text) * self.Total_price) / 100))
        else:
            self.l2.text = "Budget Left"
            self.l3.text = "Status"

        if self.t3.text and self.Total_price != 0:
            self.l4.text = "AD  -->  " + str(int((self.Total_price - ((int(self.t3.text) * self.Total_price) / 100))))
        else:
            self.l4.text = "After Discount"

    def rem_press(self):
        label_tray.clear_widgets(self.bx)
        label_tray.Total_price=0
        self.l1.text = "total -->0"
        self.list_PN = []
        self.list_p = []
        self.dict.clear()


    def Load(self):

        global pop_up1
        self.layout_load = data_base(True)

        pop_up1 = Popup(title="Saved Files", content=self.layout_load, size_hint=(1, .8))
        pop_up1.open()
        self.rem_press()






    def select(self,*args):
        global data1
        global data2

        data2=[]
        data1=[]
        data=args[0]

        pop_up1.dismiss()
        for i in range(len(data[0])):
            data1.append(str(data[0][i]))
            data2.append(str(data[1][i]))






    def save(self):
        #-------------------------------------------------------------------------------------------------------
        self.layout1 = GridLayout(cols=1, padding=10)
        self.TI= (TextInput(hint_text="File Name", multiline=False))
        self.layout1.add_widget(self.TI)
        text = Label(text="")
        text.size_hint_y = .5
        self.layout1.add_widget(text)
        BT=Button(text="Save")
        BT.bind(on_press=self.save_pop)
        self.layout1.add_widget(BT)
        text2 = Label(text="")
        text2.size_hint_y = .5
        self.layout1.add_widget(text2)
        self.pop_up = Popup(title="Save File", content=self.layout1, size_hint=(None, None), size=(200, 170))
        self.pop_up.open()

        #pop up
        #-------------------------------------------------------------------------------------------------------




    def save_pop(self,instance):
        list_all = [self.list_PN, self.list_p, self.count]
        self.file_name = "saved_files/"+self.TI.text+".pkl"
        self.file_obj = open(self.file_name, "wb")
        pickle.dump(list_all, self.file_obj)
        self.file_obj.close()
        self.pop_up.dismiss()

    def del_file(self):

        global pop_up1
        self.layout_load = data_base(False)

        pop_up1 = Popup(title="Saved Files", content=self.layout_load, size_hint=(1, .8))
        pop_up1.open()
        self.rem_press()

    def delete(self,*args):

        os.remove(*args)
        pop_up1.dismiss()











class object_tray(GridLayout):
    count = 1
    total_amount = 0
    so = True

    def __init__(self, data, price,dict, **kwargs):
        self.dict=dict
        self.data=data
        self.dict[self.data]=self.count
        self.so = True
        super(object_tray, self).__init__(**kwargs)
        self.total_tx2 = int(price)

        self.price = price
        self.tx1.text = data

        self.tx2.text = str(self.count) + "pack:  " + str(self.total_tx2)
        label_tray.total_price(label_tray, self.total_tx2, self.so, self.dict)

    def incr(self):

        self.so = True
        self.count += 1
        self.dict[self.data] = self.count

        self.total_tx2 += int(self.price)
        self.tx2.text = str(self.count) + "pack:  " + str(self.total_tx2)
        label_tray.total_price(label_tray, int(self.price), self.so,self.dict)

    def decr(self):
        if self.count > 0:
            self.so = False
            self.count -= 1
            self.dict[self.data] = self.count
            self.total_tx2 -= int(self.price)
            self.tx2.text = str(self.count) + "pack:  " + str(self.total_tx2)
            label_tray.total_price(label_tray, int(self.price), self.so,self.dict)

    def rem(self):

        object_tray.clear_widgets()
        print("jf")


class main_page(PageLayout):
    border = 5

    def __init__(self, **kwargs):
        super(main_page, self).__init__(**kwargs)

        self.add_widget(welcome_scr())
        self.add_widget(label_tray())




class data_base(GridLayout):
    cols = 1

    def __init__(self,status, **kwargs):
        super(data_base, self).__init__(**kwargs)
        self.status=status

    def select(self, *args):

        self.k = args[1][0]

        if self.status==True:

            try:
                file_obj = open(self.k, "rb")




                data = pickle.load(file_obj)
                file_obj.close()
                label_tray().select(data)
                self.pop()
            except:
                print("invalid")
        else:
            try:

                label_tray().delete(self.k)

            except:
                print("invalid")


    def pop(self):
        self.layout = GridLayout(cols=1, padding=10)
        self.layout.add_widget(Label(text="      Click On \n Add and Update"))
        self.pop_up = Popup(title="", content=self.layout, size_hint=(None, None), size=(200, 100))
        self.pop_up.open()



class welcome_scr(GridLayout):
    cols = 1

    def __init__(self, **kwargs):
        super(welcome_scr, self).__init__(**kwargs)








class main(App):
    def build(self):
        return main_page()


if __name__ == "__main__":
    k = main()
    k.run()






