import logging
from gi.repository import Gtk

logger = logging.getLogger(__name__)


class ResultItemWidget(Gtk.EventBox):
    __gtype_name__ = "ResultItemWidget"
    shortcut = None

    index = None
    builder = None
    name = None
    query = None
    item_object = None

    def initialize(self, builder, item_object, index, query):
        self.builder = builder
        item_frame = self.builder.get_object('item-frame')
        item_frame.connect("button-release-event", self.on_click)
        item_frame.connect("enter_notify_event", self.on_mouse_hover)

        self.item_object = item_object
        self.query = query
        self.set_index(index)

        self.set_icon(item_object.get_icon())
        self.set_name(item_object.get_name())
        self.set_description(item_object.get_description(query))

    def set_index(self, index):
        """
        Set index for the item and assign shortcut
        """
        self.index = index
        # Alt+1..9, then Alt+a..z
        index_text = index + 1 if index < 9 else chr(97 + index - 9)
        self.shortcut = 'Alt+%s' % index_text
        self.set_shortcut(self.shortcut)

    def select(self):
        self.get_style_context().add_class('selected')

    def deselect(self):
        self.get_style_context().remove_class('selected')

    def set_icon(self, icon):
        """
        :param PixBuf icon:
        """
        if icon:
            iconWgt = self.builder.get_object('item-icon')
            iconWgt.set_from_pixbuf(icon)

    def set_name(self, name):
        self.builder.get_object('item-name').set_text(name)
        self.name = name

    def get_name(self):
        return self.name

    def on_click(self, widget, event=None):
        self.get_toplevel().select_result_item(self.index)
        self.get_toplevel().enter_result_item()

    def on_mouse_hover(self, widget, event):
        self.get_toplevel().select_result_item(self.index, onHover=True)

    def set_description(self, description):
        description_obj = self.builder.get_object('item-descr')
        if not description_obj:
            return

        if description:
            description_obj.set_text(description)
        else:
            description_obj.destroy()  # remove description label
            self.builder.get_object('item-name').set_margin_top(8)  # shift name label down to the center

    def set_shortcut(self, text):
        self.builder.get_object('item-shortcut').set_text(text)

    def on_enter(self, query):
        return self.item_object.on_enter(query)

    def on_alt_enter(self, query):
        return self.item_object.on_alt_enter(query)

    def get_keyword(self):
        return self.item_object.get_keyword()

    def selected_by_default(self, query):
        return self.item_object.selected_by_default(query)