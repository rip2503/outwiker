# -*- coding: utf-8 -*-

import os
import re

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.application import Application
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style

from outwiker.gui.linkdialogcontroller import LinkDialogContoller

from .htmltoolbar import HtmlToolBar
from .basehtmlpanel import BaseHtmlPanel

from actions.bold import HtmlBoldAction
from actions.italic import HtmlItalicAction
from actions.underline import HtmlUnderlineAction
from actions.strike import HtmlStrikeAction
from actions.subscript import HtmlSubscriptAction
from actions.superscript import HtmlSuperscriptAction
from actions.alignleft import HtmlAlignLeftAction
from actions.aligncenter import HtmlAlignCenterAction
from actions.alignright import HtmlAlignRightAction
from actions.alignjustify import HtmlAlignJustifyAction
from actions.table import HtmlTableAction
from actions.tablerow import HtmlTableRowAction
from actions.tablecell import HtmlTableCellAction

from actions.autolinewrap import HtmlAutoLineWrap
from actions.switchcoderesult import SwitchCodeResultAction


class HtmlPagePanel (BaseHtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        super (HtmlPagePanel, self).__init__ (parent, *args, **kwds)

        self._htmlPanelName = "html"

        self.mainWindow.toolbars[self._htmlPanelName] = HtmlToolBar(self.mainWindow, self.mainWindow.auiManager)
        self.mainWindow.toolbars[self._htmlPanelName].UpdateToolBar()

        self.__HTML_MENU_INDEX = 7
        self.__createCustomTools()

        # Список действий, которые нужно удалять с панелей и из меню. 
        # А еще их надо дизаблить при переходе на вкладку просмотра результата
        self.__htmlNotationActions = [
                HtmlBoldAction,
                HtmlItalicAction,
                HtmlUnderlineAction,
                HtmlStrikeAction,
                HtmlSubscriptAction,
                HtmlSuperscriptAction,
                HtmlAlignLeftAction,
                HtmlAlignCenterAction,
                HtmlAlignRightAction,
                HtmlAlignJustifyAction,
                HtmlTableAction,
                HtmlTableRowAction,
                HtmlTableCellAction,
                ]

        Application.onPageUpdate += self.__onPageUpdate


    @property
    def toolsMenu (self):
        return self.__htmlMenu


    def onClose (self, event):
        Application.onPageUpdate -= self.__onPageUpdate

        self._removeActionTools()

        if self._htmlPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._htmlPanelName)

        super (HtmlPagePanel, self).onClose (event)


    def _removeActionTools (self):
        actionController = Application.actionController

        # Удалим элементы меню
        map (lambda action: actionController.removeMenuItem (action.stringId), 
                self.__htmlNotationActions)

        Application.actionController.removeMenuItem (HtmlAutoLineWrap.stringId)
        Application.actionController.removeMenuItem (SwitchCodeResultAction.stringId)
        
        # Удалим кнопки с панелей инструментов
        if self._htmlPanelName in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId), 
                self.__htmlNotationActions)

            Application.actionController.removeToolbarButton (HtmlAutoLineWrap.stringId)
            Application.actionController.removeToolbarButton (SwitchCodeResultAction.stringId)


    def _enableActions (self, enabled):
        actionController = Application.actionController

        self.mainWindow.Freeze()

        map (lambda action: actionController.enableTools (action.stringId, enabled), 
                self.__htmlNotationActions)

        self.mainWindow.Thaw()


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions (True)
        super (HtmlPagePanel, self)._onSwitchToCode()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self._enableActions (False)
        super (HtmlPagePanel, self)._onSwitchToPreview()


    def __onPageUpdate (self, sender):
        if sender == self._currentpage:
            if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
                self._showHtml()


    def UpdateView (self, page):
        self.__updateLineWrapTools()
        BaseHtmlPanel.UpdateView (self, page)


    def __createLineWrapTools (self):
        """
        Создать кнопки и пункты меню, отображающие настройки страницы
        """
        image = os.path.join (self.imagesDir, "linewrap.png")
        toolbarName = "html"
        toolbar = self.mainWindow.toolbars[toolbarName]

        Application.actionController.appendMenuCheckItem (HtmlAutoLineWrap.stringId, self.__htmlMenu)
        Application.actionController.appendToolbarCheckButton (HtmlAutoLineWrap.stringId, 
                toolbar,
                image,
                fullUpdate=False)

        self.__updateLineWrapTools()


    def __updateLineWrapTools (self):
        if self._currentpage != None:
            Application.actionController.check (HtmlAutoLineWrap.stringId, 
                    self._currentpage.autoLineWrap)


    def __createCustomTools (self):
        """
        Создать кнопки и меню для данного типа страниц
        """
        assert self.mainWindow != None

        self.__htmlMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__tableMenu = wx.Menu()

        self.mainWindow.Freeze()

        self.__createLineWrapTools ()
        self.toolsMenu.AppendSeparator()

        self.__htmlMenu.AppendSubMenu (self.__headingMenu, _(u"Heading"))
        self.__htmlMenu.AppendSubMenu (self.__fontMenu, _(u"Font"))
        self.__htmlMenu.AppendSubMenu (self.__alignMenu, _(u"Alignment"))
        self.__htmlMenu.AppendSubMenu (self.__formatMenu, _(u"Formatting"))
        self.__htmlMenu.AppendSubMenu (self.__listMenu, _(u"Lists"))
        self.__htmlMenu.AppendSubMenu (self.__tableMenu, _(u"Table"))

        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addTableTools()
        self.__addListTools()
        self.__addFormatTools()
        self.__addOtherTools()
        self._addRenderTools()

        Application.mainWindow.updateShortcuts()

        self.mainWindow.Thaw()

        self.mainWindow.mainMenu.Insert (self.__HTML_MENU_INDEX, self.__htmlMenu, _(u"Html"))


    def _addRenderTools (self):
        Application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        Application.actionController.appendToolbarButton (SwitchCodeResultAction.stringId, 
                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                os.path.join (self.imagesDir, "render.png"),
                fullUpdate=False)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbarName = "html"
        toolbar = self.mainWindow.toolbars[toolbarName]


        # Полужирный шрифт
        Application.actionController.appendMenuItem (HtmlBoldAction.stringId, self.__fontMenu)
        Application.actionController.appendToolbarButton (HtmlBoldAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False)


        # Курсивный шрифт
        Application.actionController.appendMenuItem (HtmlItalicAction.stringId, self.__fontMenu)
        Application.actionController.appendToolbarButton (HtmlItalicAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False)


        # Подчеркнутый шрифт
        Application.actionController.appendMenuItem (HtmlUnderlineAction.stringId, self.__fontMenu)
        Application.actionController.appendToolbarButton (HtmlUnderlineAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False)


        # Зачеркнутый шрифт
        Application.actionController.appendMenuItem (HtmlStrikeAction.stringId, self.__fontMenu)
        Application.actionController.appendToolbarButton (HtmlStrikeAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False)


        # Нижний индекс
        Application.actionController.appendMenuItem (HtmlSubscriptAction.stringId, self.__fontMenu)
        Application.actionController.appendToolbarButton (HtmlSubscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False)


        # Верхний индекс
        Application.actionController.appendMenuItem (HtmlSuperscriptAction.stringId, self.__fontMenu)
        Application.actionController.appendToolbarButton (HtmlSuperscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False)


    
    def __addAlignTools (self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbarName = "html"
        toolbar = self.mainWindow.toolbars[toolbarName]

        # Выравнивание по левому краю
        Application.actionController.appendMenuItem (HtmlAlignLeftAction.stringId, self.__alignMenu)
        Application.actionController.appendToolbarButton (HtmlAlignLeftAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False)


        # Выравнивание по центру
        Application.actionController.appendMenuItem (HtmlAlignCenterAction.stringId, self.__alignMenu)
        Application.actionController.appendToolbarButton (HtmlAlignCenterAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False)


        # Выравнивание по правому краю
        Application.actionController.appendMenuItem (HtmlAlignRightAction.stringId, self.__alignMenu)
        Application.actionController.appendToolbarButton (HtmlAlignRightAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False)


        # Выравнивание по ширине
        Application.actionController.appendMenuItem (HtmlAlignJustifyAction.stringId, self.__alignMenu)
        Application.actionController.appendToolbarButton (HtmlAlignJustifyAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False)



    def __addTableTools (self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbarName = "html"
        toolbar = self.mainWindow.toolbars[toolbarName]

        # Вставить таблицу
        Application.actionController.appendMenuItem (HtmlTableAction.stringId, self.__tableMenu)
        Application.actionController.appendToolbarButton (HtmlTableAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "table.png"),
                fullUpdate=False)


        # Вставить строку таблицы
        Application.actionController.appendMenuItem (HtmlTableRowAction.stringId, self.__tableMenu)
        Application.actionController.appendToolbarButton (HtmlTableRowAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "table_insert_row.png"),
                fullUpdate=False)


        # Вставить ячейку таблицы
        Application.actionController.appendMenuItem (HtmlTableCellAction.stringId, self.__tableMenu)
        Application.actionController.appendToolbarButton (HtmlTableCellAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "table_insert_cell.png"),
                fullUpdate=False)


    
    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        self.addTool (self.__listMenu, 
                "ID_MARK_LIST", 
                lambda event: self.codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'), 
                _(u"Bullets list") + "\tCtrl+G", 
                _(u"Bullets list (<ul>…</ul>)"), 
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__listMenu, 
                "ID_NUMBER_LIST", 
                lambda event: self.codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'), 
                _(u"Numbers list") + "\tCtrl+J", 
                _(u"Numbers list (<ul>…</ul>)"), 
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False,
                panelname="html")
    

    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        self.addTool (self.__headingMenu, 
                "ID_H1", 
                lambda event: self.codeEditor.turnText (u"<h1>", u"</h1>"), 
                _(u"H1") + "\tCtrl+1", 
                _(u"H1 (<h1>…</h1>)"), 
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H2", 
                lambda event: self.codeEditor.turnText (u"<h2>", u"</h2>"), 
                _(u"H2") + "\tCtrl+2", 
                _(u"H2 (<h2>…</h2>)"), 
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False,
                panelname="html")
        
        self.addTool (self.__headingMenu, 
                "ID_H3", 
                lambda event: self.codeEditor.turnText (u"<h3>", u"</h3>"), 
                _(u"H3") + "\tCtrl+3", 
                _(u"H3 (<h3>…</h3>)"), 
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H4", 
                lambda event: self.codeEditor.turnText (u"<h4>", u"</h4>"), 
                _(u"H4") + "\tCtrl+4", 
                _(u"H4 (<h4>…</h4>)"), 
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H5", 
                lambda event: self.codeEditor.turnText (u"<h5>", u"</h5>"), 
                _(u"H5") + "\tCtrl+5", 
                _(u"H5 (<h5>…</h5>)"), 
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H6", 
                lambda event: self.codeEditor.turnText (u"<h6>", u"</h6>"), 
                _(u"H6") + "\tCtrl+6", 
                _(u"H6 (<h6>…</h6>)"), 
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False,
                panelname="html")


    def __addFormatTools (self):
        self.addTool (self.__formatMenu, 
                "ID_CODE", 
                lambda event: self.codeEditor.turnText (u"<code>", u"</code>"), 
                _(u"Code") + "\tCtrl+Alt+D", 
                _(u"Code (<code>…</code>)"), 
                os.path.join (self.imagesDir, "code.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__formatMenu, 
                "ID_PREFORMAT", 
                lambda event: self.codeEditor.turnText (u"<pre>", u"</pre>"), 
                _(u"Preformat") + "\tCtrl+Alt+F", 
                _(u"Preformat (<pre>…</pre>)"), 
                None,
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__formatMenu, 
                "ID_BLOCKQUOTE", 
                lambda event: self.codeEditor.turnText (u"<blockquote>", u"</blockquote>"), 
                _(u"Quote") + "\tCtrl+Alt+Q", 
                _(u"Quote (<blockquote>…</blockquote>)"), 
                os.path.join (self.imagesDir, "quote.png"),
                fullUpdate=False,
                panelname="html")
    

    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        self.addTool (self.__htmlMenu, 
                "ID_IMAGE", 
                lambda event: self.codeEditor.turnText (u'<img src="', u'"/>'), 
                _(u'Image') + '\tCtrl+M', 
                _(u'Image (<img src="…"/>'), 
                os.path.join (self.imagesDir, "image.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__htmlMenu, 
                "ID_LINK", 
                self.__onInsertLink, 
                _(u"Link") + "\tCtrl+L", 
                _(u'Link (<a href="…">…</a>)'), 
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__htmlMenu, 
                "ID_ANCHOR", 
                lambda event: self.codeEditor.turnText (u'<a name="', u'"></a>'), 
                _(u"Anchor") + "\tCtrl+Alt+N", 
                _(u'Anchor (<a name="…">…</a>)'), 
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__htmlMenu, 
                "ID_HORLINE", 
                lambda event: self.codeEditor.replaceText (u'<hr>'), 
                _(u"Horizontal line") + "\tCtrl+H", 
                _(u"Horizontal line (<hr>)"), 
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False,
                panelname="html")

        self.__htmlMenu.AppendSeparator()

        self.addTool (self.__htmlMenu, 
                "ID_ESCAPEHTML", 
                self.codeEditor.escapeHtml, 
                _(u"Convert HTML Symbols"), 
                _(u"Convert HTML Symbols"), 
                None,
                fullUpdate=False,
                panelname="html")


    def generateHtml (self, page):
        path = self.getHtmlPath (page)

        if page.readonly and os.path.exists (path):
            # Если страница открыта только для чтения и html-файл уже существует, то покажем его
            return path

        style = Style()
        stylepath = style.getPageStyle (page)

        try:
            tpl = HtmlTemplate (stylepath)
        except:
            MessageBox (_(u"Page style Error. Style by default is used"),  
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

            tpl = HtmlTemplate (style.getDefaultStyle())

        if page.autoLineWrap:
            text = HtmlImprover.run (page.content)
            text = re.sub ("\n<BR>\n(<li>)|(<LI>)", "\n<LI>", text)
        else:
            text = page.content

        result = tpl.substitute (content=text)

        with open (path, "wb") as fp:
            fp.write (result.encode ("utf-8"))

        return path


    def removeGui (self):
        super (HtmlPagePanel, self).removeGui ()
        self.mainWindow.mainMenu.Remove (self.__HTML_MENU_INDEX - 1)


    def __onInsertLink (self, event):
        linkController = LinkDialogContoller (self, self.codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            text = u'<a href="{link}">{comment}</a>'.format (comment=linkController.comment, 
                    link=linkController.link)

            self.codeEditor.replaceText (text)

