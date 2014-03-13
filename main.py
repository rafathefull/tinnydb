__author__ = 'rafa'
import pygtk
pygtk.require('2.0')

import login
import principal
import gtk

if __name__ == "__main__":

    gladefile = "./tinnydb.ui"
    glade = gtk.Builder()
    glade.add_from_file(gladefile)

    # Acceso a la BD
    oLogin = login.Login( glade )
    oLogin.main()

    if oLogin.conectado:
        #Continuamos con el programa principal si se pudo loguear en la BD
        oPrincipal = principal.Principal( oLogin.db, glade )
        oPrincipal.main()
