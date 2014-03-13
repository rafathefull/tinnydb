__author__ = 'rafa'

import pygtk

pygtk.require('2.0')
import gtk


class Principal:
    """
    Contiene toda la funcionalidad principal
    """

    def __init__(self, db=None, glade=None):

        self.db = db
        self.cSql = None
        self.glade = glade

        #accediendo a los controles
        self.window = self.glade.get_object('consultas')
        self.window.connect("destroy", self.destroy)

        self.window.show()

    # Salimos de la aplicacion
    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()
        return 0