__author__ = 'rafa'

import pygtk

pygtk.require('2.0')
import gtk

class Handler():
    def delete_event(self, widget,data=None):
        print( "Call from Glade." )
        # TIP:if you return 0 , destroy, but if you return 1, stop , not kill program
        # TODO: Here create dialog ask if I want exit program

        return 0

class Principal:
    """
    Contiene toda la funcionalidad principal
    """

    def __init__(self, db=None, glade=None):

        self.db = db
        self.cSql = None
        self.glade = glade

        #Create object gtk.Window , from load window the glade
        self.window = self.glade.get_object('consultas')

        # Example connect manual signal.
        self.window.connect("destroy", self.destroy)

        # From Glade, signal delete_event the window consultas,  at class Handler.
        self.glade.connect_signals( Handler() )

        self.window.show()

    # Salimos de la aplicacion
    def destroy(self, widget, data=None):
        print( "Salgo de Aqui")
        gtk.main_quit()

    def main(self):
        gtk.main()
        return 0