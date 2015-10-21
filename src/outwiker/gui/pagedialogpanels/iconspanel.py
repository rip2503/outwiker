# -*- coding: UTF-8 -*-

import os
import os.path

import wx
import wx.combo

from outwiker.core.system import getIconsDirList
from outwiker.core.iconscollection import IconsCollection
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT
from outwiker.core.commands import MessageBox
from outwiker.gui.iconlistctrl import IconListCtrl
from basepanel import BasePageDialogPanel


class IconsPanel (BasePageDialogPanel):
    """
    Class of the panel in the "Icon" tab.
    """
    def __init__ (self, parent, application):
        super (IconsPanel, self).__init__ (parent, application)

        self._iconsCollections = [IconsCollection (path) for path in getIconsDirList()]
        self.__createGui()

        self.__appendGroups ()
        self.groupCtrl.SetSelection (0)
        self.__switchToCurrentGroup()


    @property
    def title (self):
        return _(u'Icon')


    def setPageProperties (self, page):
        """
        Return True if success and False otherwise
        """
        selection = self.iconsList.getSelection()

        assert len (selection) != 0
        icon = selection[0]

        # If icon not exists, page may be renamed. Don't will to change icon
        if os.path.exists (icon):
            try:
                page.icon = icon
            except EnvironmentError as e:
                MessageBox (_(u"Can't set page icon\n") + unicode (e),
                            _(u"Error"),
                            wx.ICON_ERROR | wx.OK)
                return False

        return True


    def __createGui (self):
        self.iconsList = IconListCtrl (self)
        self.iconsList.SetMinSize((200, 150))

        # Control for selection icons group
        self.groupCtrl = wx.combo.BitmapComboBox (self, style=wx.CB_READONLY)
        self.groupCtrl.Bind (wx.EVT_COMBOBOX, handler=self.__onGroupSelect)

        self.__layout()


    def __layout (self):
        iconSizer = wx.FlexGridSizer(rows=2)
        iconSizer.AddGrowableRow(1)
        iconSizer.AddGrowableCol(0)
        iconSizer.Add(self.groupCtrl, 1, wx.ALL | wx.EXPAND, 2)
        iconSizer.Add(self.iconsList, 1, wx.ALL | wx.EXPAND, 2)

        self.SetSizer (iconSizer)
        self.Layout()


    def __appendGroups (self):
        for n, collection in enumerate (self._iconsCollections):
            # First None is root directory
            for group in [None] + sorted (collection.getGroups(), key=self._localize):
                # Get group name
                if group is None:
                    title = _(u'Not in groups')
                else:
                    title = self._localize(group)

                if n != 0:
                    title += u' *'
                # Every item has tuple (collection index, group name)
                self.groupCtrl.Append (title,
                                       self._getCover (collection, group),
                                       (n, group))


    def _getImageForGroup (self, fname):
        neww = ICON_WIDTH
        newh = ICON_HEIGHT + 2

        wx.Log_EnableLogging(False)
        image = wx.Image (fname)
        wx.Log_EnableLogging(True)

        if not image.IsOk():
            print _(u'Invalid icon file: {}').format (fname)
            return wx.NullBitmap

        posx = (neww - image.Width) / 2
        posy = (newh - image.Height) / 2
        image.Resize ((neww, newh), (posx, posy), 255, 255, 255)

        return wx.BitmapFromImage (image)


    def _getCover (self, collection, groupname):
        """
        Return bitmap for combobox item
        """
        fname = collection.getCover (groupname)
        if fname is not None:
            return self._getImageForGroup (fname)

        return wx.NullBitmap


    def _getRootCover (self):
        """
        Return bitmap for combobox item
        """
        # fname = self._iconsCollections[0].getCover (None)
        fname = None
        for collection in self._iconsCollections:
            cover = collection.getCover (None)
            if cover is not None:
                fname = cover

        if fname is not None:
            return self._getImageForGroup (fname)

        return wx.NullBitmap


    def __onGroupSelect (self, event):
        self.__switchToCurrentGroup()


    def __getCurrentIcons (self):
        index, groupname = self.groupCtrl.GetClientData (self.groupCtrl.GetSelection())

        icons = self._iconsCollections[index].getIcons (groupname)
        icons.sort()

        return icons


    def __switchToCurrentGroup (self):
        icons = self.__getCurrentIcons()
        icons.sort (key=os.path.basename)
        self.iconsList.setIconsList (icons)


    def _localize (self, groupname):
        name = _(groupname)
        return name.capitalize()


    def initBeforeEditing (self, currentPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        icon = currentPage.icon
        if icon is not None:
            self.iconsList.setCurrentIcon (icon)