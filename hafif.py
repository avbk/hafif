import gtk
import data
from ui import HafifWindow

projects = data.load()
window = HafifWindow(projects)
gtk.main()