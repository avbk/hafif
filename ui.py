import cairo
import gtk


class HafifWindow(gtk.Window):
    def __init__(self, projects):
        super(HafifWindow, self).__init__()
        self.set_position(gtk.WIN_POS_CENTER)

        self.set_size_request(300, 220)
        self.set_border_width(0)
        #self.set_decorated(False)

        self.screen = self.get_screen()
        colormap = self.screen.get_rgba_colormap()
        if colormap is not None and self.screen.is_composited():
            self.set_colormap(colormap)

        self.set_app_paintable(True)
        self.connect("expose-event", self.area_draw)
        b = gtk.Button()
        b.set_label("Hello")
        self.button = b
        f = gtk.Fixed()
        self.fixed = f
        b.connect("clicked", self.click)
        f.put(b, 100, 100)
        self.add(ProjectLayout(projects[0]))

        self.show_all()
        self.move(100, 0)


    def click(self, widget):
        x = self.fixed.child_get_property(self.button, "x")
        if x > 250:
            gtk.main_quit()
        else:
            self.fixed.child_set_property(self.button, "x", x + 10)


    def area_draw(self, widget, event):
        cr = widget.get_window().cairo_create()
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        return False


class ProjectLayout(gtk.VBox):
    def __init__(self, project):
        super(ProjectLayout, self).__init__()
        self.project = project
        self.add(gtk.Label(self.project.title))

