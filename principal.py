__author__ = 'rafa'

import pygtk

pygtk.require('2.0')
import gtk
import MySQLdb

class Handler():
    def delete_event(self, widget,data=None):
        print( "Call from Glade." )
        # TIP:if you return 0 , destroy, but if you return 1, stop , not kill program
        # TODO: Here create dialog ask if I want exit program

class Principal:
    """
    Contiene toda la funcionalidad principal
    """

    def __init__(self, oLogin=None, glade=None ):

        self.db = oLogin.db
        self.cSql = None
        self.glade = glade
        self.database = oLogin.database

        #Create object gtk.Window , from load window the glade
        self.window = self.glade.get_object('consultas')

        # Example connect manual signal.
        self.window.connect("destroy", self.destroy)
        self.window.connect("key-press-event", self.on_key_press_event )

        # From Glade, signal delete_event the window consultas,  at class Handler.
        # self.glade.connect_signals( Handler() )
        self.glade.connect_signals( self )

        self.status_bar()
        self.status_setText( "Database in use:" + self.database )

        self.view_lista   = self.glade.get_object('treeview_consulta')
        self.textview_sql = self.glade.get_object('textview_ordenes')
        self.textview_sql.grab_focus()

        self.window.show()

    def status_bar(self):
        self.status_bar = self.glade.get_object( "statusbar")
        self.context_id = self.status_bar.get_context_id("database")

    def status_setText(self,cText):
        self.status_bar.pop(self.context_id)
        self.status_bar.push( self.context_id, cText)

    def execute_sql(self, widget, data=None):
        self.setQuery()

    def setQuery(self):
        elements = 0

        self.status_setText( "Database in use:" + self.database )
        textbuffer = self.textview_sql.get_buffer()
        self.cSql = textbuffer.get_text(*textbuffer.get_bounds())

        # remove columns the old view
        nOld_Fields = self.getTotalColumns()
        if nOld_Fields != 0:
            for column in self.view_lista.get_columns():
                self.view_lista.remove_column( column )

        #Clear model data of view
        oModel = self.view_lista.get_model()
        if oModel != None:
            oModel.clear()
        self.view_lista.set_model()

        #Execute Sql
        cursor = self.db.cursor()
        try:
            cursor.execute(self.cSql)
            result = cursor.fetchall()
        except MySQLdb.Error, e:
            self.status_setText( "Error %d: %s" % (e.args[0], e.args[1]) )
            return

        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description] # Name of fields

        #Create Columns from names fields
        i = 0
        for nombre in field_names:
            self.AddListColumn(nombre, i)
            i = i + 1

        #Create model dinamic of types str for view
        ListStore = gtk.ListStore(*([str] * num_fields))
        for value in result:
            ListStore.append(value)
        self.view_lista.set_model(ListStore)

    def AddListColumn(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
        column.set_resizable(True)
        column.set_sort_column_id(columnId)
        self.view_lista.append_column( column )

    def AddColumnPixbuf(self, title, columnId):
        column = gtk.TreeViewColumn(title, gtk.CellRendererPixbuf(), pixbuf=columnId)
        self.view_lista.append_column( column )


    def getTotalColumns(self):
        return len(self.view_lista.get_columns())

    def on_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == "F5":
            self.setQuery()
            return 1

    def delete_event(self, widget,data=None):
        messagedialog = gtk.MessageDialog(self.window, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO)
        messagedialog.set_markup("<b>%s</b>" % "Hi pythoniso!")
        messagedialog.format_secondary_markup("Why Do you exit the program ? Why ??")
        response = messagedialog.run()
        messagedialog.destroy()
        if response == gtk.RESPONSE_YES:
            return 0
        elif response == gtk.RESPONSE_NO:
            return 1

        print( "delete-event from self" )

    # Salimos de la aplicacion
    def destroy(self, widget, data=None):
        print( "Salgo de Aqui")
        gtk.main_quit()


    def main(self):
        gtk.main()
        return 0