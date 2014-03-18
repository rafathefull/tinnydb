__author__ = 'rafa'

import pygtk
pygtk.require('2.0')
import gtk
import MySQLdb
import os
import ConfigParser

class Login:
    """
    Ventana de Introduccion al sistema
    """

    def LoadConfig(self):
        """
         Vamos a leer un fichero de configuracion y lo rellenammos
        """
        cfg = ConfigParser.ConfigParser()
        cfg.read(["connect.cfg"])
        self.entry_user.set_text(cfg.get("mysql", "user"))
        self.entry_pass.set_text(cfg.get("mysql", "psw"))
        self.entry_server.set_text(cfg.get("mysql", "host"))
        self.entry_bd.set_text(cfg.get("mysql", "dbname"))
        self.spin_port.set_text(cfg.get("mysql", "port"))

    def __init__(self, glade=None):

        """
        Ventana de acceso a la BD
        """

        self.conectado = False
        self.glade = glade

        #accediendo a los controles
        self.window = self.glade.get_object('inicio')
        self.window.connect("destroy", self.destroy)

        self.btn_access = self.glade.get_object('btn_access')

        # este salta a un method
        self.btn_access.connect("clicked", self.Conectando, None)

        self.btn_cancel = self.glade.get_object('btn_cancel')
        self.btn_cancel.connect("clicked", self.destroy )

        self.label = self.glade.get_object('information')

        self.entry_user   = self.glade.get_object('entry_user')
        self.entry_user.connect("key-press-event", self.on_key_press_event )

        self.entry_pass   = self.glade.get_object('entry_pass')
        self.entry_pass.connect("key-press-event", self.on_key_press_event )

        self.entry_server = self.glade.get_object('entry_server')
        self.entry_bd     = self.glade.get_object('entry_bd')
        self.spin_port    = self.glade.get_object('spin_port')

        self.LoadConfig()
        self.window.show()

    def OpenDB(self):
        self.elhost = self.entry_server.get_text()
        self.database   = self.entry_bd.get_text()
        self.db = MySQLdb.connect( host=self.elhost, user=self.entry_user.get_text(), passwd=self.entry_pass.get_text(), db=self.database )


    def Conectando(self, widget, data=None):
        self.label.set_label( "Informacion" )
        try:
            self.OpenDB()
            self.conectado = True
            self.window.destroy()

        except MySQLdb.Error, e:
               self.label.set_label( "Error %d: %s" % (e.args[0], e.args[1]) )

    def on_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == "Return" or keyname == "KP_Enter":
            widget.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD)

    # Cuando destruimos la pantalla, si no estamos conectado, salimos de la aplicacion.
    def destroy(self, widget, data=None):
        if not self.conectado:
            gtk.main_quit()
            os.sys.exit (1)
        else:
            gtk.main_quit()

    def main(self):
        gtk.main()
        return 0
