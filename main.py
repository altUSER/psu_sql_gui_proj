import notorm
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

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

# Add client
def new_client_window():
    mst_name_list = []
    mst_name_dict = {}
    for master in notorm.Master().getAll():
        mst_name_list.append(master.name)
        mst_name_dict.update({master.name: master.id})
    

    srv_name_list = []
    srv_name_dict = {}
    for service in notorm.Service().getAll():
        srv_name_list.append(service.service_name)
        srv_name_dict.update({service.service_name: service.id})

    w_add_cl = Toplevel(root)
    w_add_cl.title('Новый клиент')

    l_name = ttk.Label(w_add_cl, text='ФИО')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_add_cl)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_phone = ttk.Label(w_add_cl, text='Телефон')
    l_phone.grid(row=1, column=0, pady=4, padx=2)
    e_phone = ttk.Entry(w_add_cl)
    e_phone.grid(row=1, column=1, pady=4, padx=2, sticky='ew')


    mst_var = StringVar()

    l_master = ttk.Label(w_add_cl, text='Мастер')
    l_master.grid(row=2, column=0, pady=4, padx=2)
    cb_master = ttk.Combobox(w_add_cl, textvariable=mst_var, values=mst_name_list)
    cb_master.grid(row=2, column=1, pady=4, padx=2, sticky='ew')


    srv_val = StringVar()

    l_service = ttk.Label(w_add_cl, text='Услуга')
    l_service.grid(row=3, column=0, pady=4, padx=2)
    cb_service = ttk.Combobox(w_add_cl, textvariable=srv_val, values=srv_name_list)
    cb_service.grid(row=3, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_add_cl)

    b_exit = ttk.Button(button_frame, text='Закрыть', command=w_add_cl.destroy)
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Добавить', command=lambda: add_client(e_name.get(), e_phone.get(), mst_var.get(), srv_val.get()))
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)

    def add_client(name, phone_number, master_name, service_name):
        try:
            newUser = notorm.Client(
                    name=name,
                    phone_number=phone_number,
                    master=notorm.Master().getById(mst_name_dict[master_name]),
                    service=notorm.Service().getById(srv_name_dict[service_name])
                    )
            newUser.write()

            showinfo('Успешно', f'Пользователь {name} добавлен.')
            w_add_cl.destroy()
        except Exception as e:
            showerror('Ошибка', e)

# Update client
def update_client_window(cl_id):
    client = notorm.Client().getById(cl_id)

    mst_name_list = []
    mst_name_dict = {}
    for master in notorm.Master().getAll():
        mst_name_list.append(master.name)
        mst_name_dict.update({master.name: master.id})
    

    srv_name_list = []
    srv_name_dict = {}
    for service in notorm.Service().getAll():
        srv_name_list.append(service.service_name)
        srv_name_dict.update({service.service_name: service.id})

    w_upd_cl = Toplevel(root)
    w_upd_cl.title(client.name)

    l_name = ttk.Label(w_upd_cl, text='ФИО')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_upd_cl)
    e_name.insert(0, client.name)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_phone = ttk.Label(w_upd_cl, text='Телефон')
    l_phone.grid(row=1, column=0, pady=4, padx=2)
    e_phone = ttk.Entry(w_upd_cl)
    e_phone.insert(0, client.phone_number)
    e_phone.grid(row=1, column=1, pady=4, padx=2, sticky='ew')


    mst_var = StringVar(value=mst_name_list[client.master.id])

    l_master = ttk.Label(w_upd_cl, text='Мастер')
    l_master.grid(row=2, column=0, pady=4, padx=2)
    cb_master = ttk.Combobox(w_upd_cl, textvariable=mst_var, values=mst_name_list)
    cb_master.grid(row=2, column=1, pady=4, padx=2, sticky='ew')


    srv_val = StringVar(value=srv_name_list[client.service.id])

    l_service = ttk.Label(w_upd_cl, text='Услуга')
    l_service.grid(row=3, column=0, pady=4, padx=2)
    cb_service = ttk.Combobox(w_upd_cl, textvariable=srv_val, values=srv_name_list)
    cb_service.grid(row=3, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_upd_cl)

    b_exit = ttk.Button(button_frame, text='Закрыть', command=w_upd_cl.destroy)
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Обновить', command=lambda: update_client())
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    b_delete = ttk.Button(button_frame, text='Удалить', command=lambda: delete_client())
    b_delete.grid(row=0, column=3, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)

    def update_client():
        client.name = e_name.get()
        client.phone_number = e_phone.get()
        client.master = notorm.Master().getById(mst_name_dict[mst_var.get()])
        client.service = notorm.Service().getById(srv_name_dict[srv_val.get()])

        try:
            client.write()
            cl_item_update()
            showinfo('Успешно', f'Пользователь {client.name} обновлен.')
            w_upd_cl.destroy()
        except Exception as e:
            showerror('Ошибка', e)
    
    def delete_client():
        try:
            client.delete()
            cl_item_update()
            showinfo('Успешно', f'Пользователь {client.name} удален.')
            w_upd_cl.destroy()
        except Exception as e:
            showerror('Ошибка', e)
    

# Add Master
def new_master_window():
    w_add_mst = Toplevel(root)
    w_add_mst.title('Новый мастер')

    l_name = ttk.Label(w_add_mst, text='ФИО')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_add_mst)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_phone = ttk.Label(w_add_mst, text='Телефон')
    l_phone.grid(row=1, column=0, pady=4, padx=2)
    e_phone = ttk.Entry(w_add_mst)
    e_phone.grid(row=1, column=1, pady=4, padx=2, sticky='ew')

    l_addr = ttk.Label(w_add_mst, text='Адрес')
    l_addr.grid(row=2, column=0, pady=4, padx=2)
    e_addr = ttk.Entry(w_add_mst)
    e_addr.grid(row=2, column=1, pady=4, padx=2, sticky='ew')

    l_act = ttk.Label(w_add_mst, text='Деятельность')
    l_act.grid(row=3, column=0, pady=4, padx=2)
    e_act = ttk.Entry(w_add_mst)
    e_act.grid(row=3, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_add_mst)

    b_exit = ttk.Button(button_frame, text='Закрыть', command=w_add_mst.destroy)
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Добавить', command=lambda: add_master())
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)

    def add_master():
        new_master = notorm.Master(
            kind_of_activity=e_act.get(),
            name=e_name.get(),
            address=e_addr.get(),
            phone_number=e_phone.get()
            )
        
        try:
            new_master.write()
            mst_item_update()
            showinfo('Успешно', f'Мастер {new_master.name} добавлен.')
            w_add_mst.destroy()
        except Exception as e:
            showerror('Ошибка', e)

# Update Master
def update_master_window(mst_id):
    master = notorm.Master().getById(mst_id)

    w_upd_mst = Toplevel(root)
    w_upd_mst.title(master.name)

    l_name = ttk.Label(w_upd_mst, text='ФИО')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_upd_mst)
    e_name.insert(0, master.name)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_phone = ttk.Label(w_upd_mst, text='Телефон')
    l_phone.grid(row=1, column=0, pady=4, padx=2)
    e_phone = ttk.Entry(w_upd_mst)
    e_phone.insert(0, master.phone_number)
    e_phone.grid(row=1, column=1, pady=4, padx=2, sticky='ew')

    l_addr = ttk.Label(w_upd_mst, text='Адрес')
    l_addr.grid(row=2, column=0, pady=4, padx=2)
    e_addr = ttk.Entry(w_upd_mst)
    e_addr.insert(0, master.address)
    e_addr.grid(row=2, column=1, pady=4, padx=2, sticky='ew')

    l_act = ttk.Label(w_upd_mst, text='Деятельность')
    l_act.grid(row=3, column=0, pady=4, padx=2)
    e_act = ttk.Entry(w_upd_mst)
    e_act.insert(0, master.kind_of_activity)
    e_act.grid(row=3, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_upd_mst)

    b_exit = ttk.Button(button_frame, text='Закрыть', command=w_upd_mst.destroy)
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Обновить', command=lambda: update_master())
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    b_delete = ttk.Button(button_frame, text='Удалить', command=lambda: delete_master())
    b_delete.grid(row=0, column=3, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)

    def update_master():
        master.name = e_name.get()
        master.address = e_addr.get()
        master.phone_number = e_phone.get()
        master.kind_of_activity = e_act.get()
        
        try:
            master.write()
            mst_item_update()
            showinfo('Успешно', f'Мастер {master.name} обновлен.')
            w_upd_mst.destroy()
        except Exception as e:
            showerror('Ошибка', e)


    def delete_master():
        try:
            master.delete()
            mst_item_update()
            showinfo('Успешно', f'Мастер {master.name} удален.')
            w_upd_mst.destroy()
        except Exception as e:
            showerror('Ошибка', e)


# Add Service
def new_service_window():
    w_add_srv = Toplevel(root)
    w_add_srv.title('Новая услуга')

    l_name = ttk.Label(w_add_srv, text='Название')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_add_srv)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_price = ttk.Label(w_add_srv, text='Цена')
    l_price.grid(row=1, column=0, pady=4, padx=2)
    e_price = ttk.Entry(w_add_srv)
    e_price.grid(row=1, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_add_srv)

    b_exit = ttk.Button(button_frame, text='Закрыть', command=w_add_srv.destroy)
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Добавить', command=lambda: add_service())
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)

    def add_service():
        new_service = notorm.Service(
                service_name=e_name.get(),
                price=e_price.get()
                )
        
        try:
            new_service.write()
            srv_item_update()
            showinfo('Успешно', f'Услуга {new_service.service_name} добавлена.')
            w_add_srv.destroy()
        except Exception as e:
            showerror('Ошибка', e)

# Update Service
def update_service_window(srv_id):
    service = notorm.Service().getById(srv_id)

    w_upd_srv = Toplevel(root)
    w_upd_srv.title(service.service_name)

    l_name = ttk.Label(w_upd_srv, text='Название')
    l_name.grid(row=0, column=0, pady=4, padx=2)
    e_name = ttk.Entry(w_upd_srv)
    e_name.insert(0, service.service_name)
    e_name.grid(row=0, column=1, pady=4, padx=2, sticky='ew')

    l_price = ttk.Label(w_upd_srv, text='Цена')
    l_price.grid(row=1, column=0, pady=4, padx=2)
    e_price = ttk.Entry(w_upd_srv)
    e_price.insert(0, service.price)
    e_price.grid(row=1, column=1, pady=4, padx=2, sticky='ew')

    button_frame = ttk.Frame(w_upd_srv)

    b_exit = ttk.Button(button_frame, text='Закрыть', command=w_upd_srv.destroy)
    b_exit.grid(row=0, column=0, pady=4, padx=6)

    b_apply = ttk.Button(button_frame, text='Обновить', command=lambda: update_service())
    b_apply.grid(row=0, column=1, pady=4, padx=6)

    b_delete = ttk.Button(button_frame, text='Удалить', command=lambda: delete_service())
    b_delete.grid(row=0, column=3, pady=4, padx=6)

    button_frame.grid(row=4, column=0, columnspan=2)

    def update_service():
        try:
            service.write()
            srv_item_update()
            showinfo('Успешно', f'Услуга {service.service_name} обновлена.')
            w_upd_srv.destroy()
        except Exception as e:
            showerror('Ошибка', e)

    def delete_service():
        try:
            service.delete()
            srv_item_update()
            showinfo('Успешно', f'Услуга {service.service_name} удалена.')
            w_upd_srv.destroy()
        except Exception as e:
            showerror('Ошибка', e)


# --Main Window--

# Clients
            
def cl_item_update():
    t_cl.delete(*t_cl.get_children(''))

    clients = []
    for cl in notorm.Client().getAll():
        clients.append((
                cl.id,
                cl.master.name,
                cl.name,
                cl.phone_number,
                cl.service.service_name,
                cl.service.price))
    
    for cl in clients:
        t_cl.insert('', END, values=cl)

def cl_item_select(event):
    item = t_cl.item(t_cl.selection()[0])
    cl_id = item['values'][0]

    update_client_window(cl_id)

f_cl_frame = ttk.Frame(f_clients)     
f_cl_frame.pack(side=TOP, anchor='nw')       

b_cl_add = ttk.Button(master=f_cl_frame, text='Добавить', command=new_client_window)
b_cl_add.grid(row=0, column=0, sticky='w')

b_cl_update = ttk.Button(master=f_cl_frame, text='Обновить', command=cl_item_update)
b_cl_update.grid(row=0, column=1, sticky='w')

columns = ('id', 'master', 'name', 'phone_number', 'service', 'price')

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
 
cl_item_update()

t_cl.bind('<<TreeviewSelect>>', cl_item_select)

# Masters

def mst_item_update():
    t_mst.delete(*t_mst.get_children(''))

    masters = []
    for mst in notorm.Master().getAll():
        masters.append((
                mst.id,
                mst.kind_of_activity,
                mst.name,
                mst.address,
                mst.phone_number))
    
    for mst in masters:
        t_mst.insert('', END, values=mst)

def mst_item_select(event):
    item = t_mst.item(t_mst.selection()[0])
    mst_id = item['values'][0]

    update_master_window(mst_id)

f_mst_frame = ttk.Frame(f_masters)     
f_mst_frame.pack(side=TOP, anchor='nw')       

b_mst_add = ttk.Button(master=f_mst_frame, text='Добавить', command=new_master_window)
b_mst_add.grid(row=0, column=0, sticky='w')

b_mst_update = ttk.Button(master=f_mst_frame, text='Обновить', command=mst_item_update)
b_mst_update.grid(row=0, column=1, sticky='w')
    

columns = ('id', 'kind_of_activity', 'name', 'address', 'phone_number')

t_mst = ttk.Treeview(master=f_masters, columns=columns, show='headings')
t_mst.pack(fill=BOTH, expand=1)
 
t_mst.heading('id', text='#')
t_mst.heading('kind_of_activity', text='Деятельность')
t_mst.heading('name', text='ФИО')
t_mst.heading('address', text='Адрес')
t_mst.heading('phone_number', text='Телефон')

t_mst.column('id', stretch=NO, width=20)
 
mst_item_update()

t_mst.bind('<<TreeviewSelect>>', mst_item_select)

# Services
def srv_item_update():
    t_srv.delete(*t_srv.get_children(''))

    services = []
    for srv in notorm.Service().getAll():
        services.append((
                srv.id,
                srv.service_name,
                srv.price))
    
    for srv in services:
        t_srv.insert('', END, values=srv)

def srv_item_select(event):
    item = t_srv.item(t_srv.selection()[0])
    srv_id = item['values'][0]

    update_service_window(srv_id)

f_srv_frame = ttk.Frame(f_services)     
f_srv_frame.pack(side=TOP, anchor='nw')       

b_mst_add = ttk.Button(master=f_srv_frame, text='Добавить', command=new_service_window)
b_mst_add.grid(row=0, column=0, sticky='w')

b_mst_update = ttk.Button(master=f_srv_frame, text='Обновить', command=srv_item_update)
b_mst_update.grid(row=0, column=1, sticky='w')

columns = ('id', 'name', 'price')

t_srv = ttk.Treeview(master=f_services, columns=columns, show='headings')
t_srv.pack(fill=BOTH, expand=1)
 
t_srv.heading('id', text='#')
t_srv.heading('name', text='Название')
t_srv.heading('price', text='Цена')

t_srv.column('id', stretch=NO, width=20)
t_srv.column('price', stretch=NO, width=40)

srv_item_update()

t_srv.bind('<<TreeviewSelect>>', srv_item_select)

 
root.mainloop()