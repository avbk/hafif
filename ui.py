import cairo
import gtk
import shlex
import subprocess
import os.path

PROJECT_WIDTH = 300


def get_pixbuf_from_path(path, size):
    if path.startswith('~/'):
        icon_path = os.path.expanduser(path)
    elif path.startswith('/'):
        icon_path = path
    else:
        icon_path = "/usr/share/icons/Faenza/%s.png" % path

    pixbuf = gtk.gdk.pixbuf_new_from_file(icon_path)
    scaled_buf = pixbuf.scale_simple(size, size, gtk.gdk.INTERP_BILINEAR)
    return scaled_buf


class HafifWindow(gtk.Window):
    def __init__(self, projects):
        super(HafifWindow, self).__init__()

        self.screen = self.get_screen()
        width = PROJECT_WIDTH * len(projects)
        self.set_size_request(width, self.screen.get_height() - 10)
        self.set_border_width(0)
        self.set_decorated(False)
        self.set_keep_below(True)
        self.set_can_focus(False)
        self.move(self.screen.get_width() - width, 0)

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

        self.connect("destroy", gtk.main_quit)
        self.show_all()

    def click(self, widget):
        x = self.fixed.child_get_property(self.button, "x")
        if x > 250:
            gtk.main_quit()
        else:
            self.fixed.child_set_property(self.button, "x", x + 10)

    def area_draw(self, widget, event):
        cr = widget.get_window().cairo_create()
        cr.set_source_rgba(0, 0, 0, 0.3)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        return False


PROJECT_ICON_SIZE = 96

SHORTCUTS_COL_COUNT = 4
SHORTCUTS_ROW_COUNT = 2
SHORTCUT_ICON_SIZE = 48
SHORTCUTS_PADDING = 16


class ProjectLayout(gtk.VBox):
    def __init__(self, project):
        super(ProjectLayout, self).__init__(False)
        self.set_spacing(16)
        self.project = project
        self.__add_icon()
        self.__add_title()
        self.__add_shortcuts()

    def __add_icon(self):
        self.icon = gtk.Image()
        self.icon.set_from_pixbuf(get_pixbuf_from_path(self.project.icon, PROJECT_ICON_SIZE))
        self.icon.set_size_request(PROJECT_ICON_SIZE, PROJECT_ICON_SIZE)
        self.pack_start(self.icon, False)

    def __add_title(self):
        self.title = gtk.Label()
        self.title.set_markup('<span color="#AAAAAA">%s</span>' % self.project.title)
        self.pack_start(self.title, False)

    def __add_shortcuts(self):
        self.shortcuts = gtk.Table(SHORTCUTS_COL_COUNT, SHORTCUTS_ROW_COUNT, False)
        self.shortcuts.set_col_spacings(SHORTCUTS_PADDING)
        self.shortcuts.set_row_spacings(SHORTCUTS_PADDING)
        col = 0
        row = 0
        for shortcut in self.project.shortcuts:
            self.shortcuts.attach(ShortcutIcon(shortcut), col, col + 1, row, row + 1, 0, 0)
            col += 1
            if col % SHORTCUTS_COL_COUNT == 0:
                row += 1
                col = 0
        self.pack_start(self.shortcuts, False)


class ShortcutIcon(gtk.Button):
    def __init__(self, shortcut):
        super(ShortcutIcon, self).__init__()
        icon = gtk.Image()
        icon.set_from_pixbuf(get_pixbuf_from_path(shortcut.icon, SHORTCUT_ICON_SIZE))
        icon.set_size_request(SHORTCUT_ICON_SIZE, SHORTCUT_ICON_SIZE)
        self.set_relief(gtk.RELIEF_NONE)
        self.set_image(icon)
        self.connect("clicked", self.__on_icon_click, shortcut)

    def __on_icon_click(self, _, shortcut):
        subprocess.Popen(shlex.split(shortcut.command))
