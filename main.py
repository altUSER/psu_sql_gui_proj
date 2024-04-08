import notorm
from tkinter import *
from tkinter import ttk

open_windows_flag = 0

root = Tk()
root.title('БД Салон красоты')
root.geometry('1000x250')


notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=BOTH)


f_clients = ttk.Frame(notebook)
f_masters = ttk.Frame(notebook)
f_services = ttk.Frame(notebook)
 
f_clients.pack(fill=BOTH, expand=True)
f_masters.pack(fill=BOTH, expand=True)
f_services.pack(fill=BOTH, expand=True)
 
notebook.add(f_clients, text='Клиенты')
notebook.add(f_masters, text='Мастера')
notebook.add(f_services, text='Услуги')


# --Additionals windows--

def add_client():
    mst_name_list = []
    for master in notorm.Master().getAll():
        mst_name_list.append(master.name)

    srv_name_list = []
    for service in notorm.Service().getAll():
        srv_name_list.append(service.service_name)

    w_add_cl = Toplevel(root)
    w_add_cl.title('Новый клиент')
    #w_add_cl.geometry('300x200')

    l_name = ttk.Label(w_add_cl, text='ФИО')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_add_cl)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_phone = ttk.Label(w_add_cl, text='Телефон')
    l_phone.grid(row=1, column=0, pady=4, padx=2)
    e_phone = ttk.Entry(w_add_cl)
    e_phone.grid(row=1, column=1, pady=4, padx=2, sticky='ew')

    l_master = ttk.Label(w_add_cl, text='Мастер')
    l_master.grid(row=2, column=0, pady=4, padx=2)
    cb_master = ttk.Combobox(w_add_cl, values=mst_name_list)
    cb_master.grid(row=2, column=1, pady=4, padx=2, sticky='ew')

    l_service = ttk.Label(w_add_cl, text='Услуга')
    l_service.grid(row=3, column=0, pady=4, padx=2)
    cb_service = ttk.Combobox(w_add_cl, values=srv_name_list)
    cb_service.grid(row=3, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_add_cl)

    b_exit = ttk.Button(button_frame, text='Закрыть')
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Добавить')
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)
    



# --Main Window--

# Clients
btn = ttk.Button(master=f_clients, text='Добавить', command=add_client)
btn.pack(anchor='nw')

columns = ('id', 'master', 'name', 'phone_number', 'service', 'price')

clients = []
for cl in notorm.Client().getAll():
    clients.append((
            cl.id,
            cl.master.name,
            cl.name,
            cl.phone_number,
            cl.service.service_name,
            cl.service.price))

t_cl = ttk.Treeview(master=f_clients, columns=columns, show='headings')
t_cl.pack(fill=BOTH, expand=1)
 
t_cl.heading('id', text='#')
t_cl.heading('master', text='Мастер')
t_cl.heading('name', text='ФИО')
t_cl.heading('phone_number', text='Телефон')
t_cl.heading('service', text='Услуга')
t_cl.heading('price', text='Цена')

t_cl.column('id', stretch=NO, width=20)
t_cl.column('price', stretch=NO, width=40)
 
for cl in clients:
    t_cl.insert('', END, values=cl)

# Masters
columns = ('id', 'kind_of_activity', 'name', 'address', 'phone_number')

masters = []
for mst in notorm.Master().getAll():
    masters.append((
            mst.id,
            mst.kind_of_activity,
            mst.name,
            mst.address,
            mst.phone_number))

t_mst = ttk.Treeview(master=f_masters, columns=columns, show='headings')
t_mst.pack(fill=BOTH, expand=1)
 
t_mst.heading('id', text='#')
t_mst.heading('kind_of_activity', text='Деятельность')
t_mst.heading('name', text='ФИО')
t_mst.heading('address', text='Адрес')
t_mst.heading('phone_number', text='Телефон')

t_mst.column('id', stretch=NO, width=20)
 
for mst in masters:
    t_mst.insert('', END, values=mst)

# Services
columns = ('id', 'name', 'price')

services = []
for srv in notorm.Service().getAll():
    services.append((
            srv.id,
            srv.service_name,
            srv.price))

t_srv = ttk.Treeview(master=f_services, columns=columns, show='headings')
t_srv.pack(fill=BOTH, expand=1)
 
t_srv.heading('id', text='#')
t_srv.heading('name', text='Название')
t_srv.heading('price', text='Цена')

t_srv.column('id', stretch=NO, width=20)
t_srv.column('price', stretch=NO, width=40)
 
for srv in services:
    t_srv.insert('', END, values=srv)



 
root.mainloop()