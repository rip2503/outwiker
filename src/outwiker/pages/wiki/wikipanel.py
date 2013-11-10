#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import os

from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.config import Config, StringOption
from outwiker.core.tree import RootWikiPage
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style

from .wikieditor import WikiEditor
from .wikitoolbar import WikiToolBar
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from wikiconfig import WikiConfig
from htmlgenerator import HtmlGenerator

from actions.bold import WikiBoldAction
from actions.italic import WikiItalicAction
from actions.bolditalic import WikiBoldItalicAction
from actions.underline import WikiUnderlineAction
from actions.strike import WikiStrikeAction
from actions.subscript import WikiSubscriptAction
from actions.superscript import WikiSuperscriptAction
from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.monospace import WikiMonospaceAction
from actions.alignleft import WikiAlignLeftAction
from actions.alignright import WikiAlignRightAction
from actions.aligncenter import WikiAlignCenterAction
from actions.alignjustify import WikiAlignJustifyAction
from actions.preformat import WikiPreformatAction
from actions.nonparsed import WikiNonParsedAction
from actions.listbullets import WikiListBulletsAction
from actions.listnumbers import WikiListNumbersAction
from actions.headings import *
from actions.thumb import WikiThumbAction
from actions.link import WikiLinkAction
from actions.anchor import WikiAnchorAction
from actions.horline import WikiHorLineAction
from actions.linebreak import WikiLineBreakAction
from actions.equation import WikiEquationAction
from actions.escapehtml import WikiEscapeHtmlAction
from actions.openhtmlcode import WikiOpenHtmlCodeAction
from actions.updatehtml import WikiUpdateHtmlAction
from actions.attachlist import WikiAttachListAction
from actions.childlist import WikiChildListAction
from actions.include import WikiIncludeAction
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction


class WikiPagePanel (BaseHtmlPanel):
    HTML_RESULT_PAGE_INDEX = BaseHtmlPanel.RESULT_PAGE_INDEX + 1


    def __init__ (self, parent, *args, **kwds):
        super (WikiPagePanel, self).__init__ (parent, *args, **kwds)

        self._application = Application

        self._configSection = u"wiki"
        self._hashKey = u"md5_hash"
        self.__WIKI_MENU_INDEX = 7
        self.__toolbarName = "wiki"

        # Список действий, которые нужно удалять с панелей и из меню. 
        # А еще их надо дизаблить при переходе на вкладки просмотра результата или HTML
        self.__wikiNotationActions = [
                WikiBoldAction,
                WikiItalicAction,
                WikiBoldItalicAction,
                WikiUnderlineAction,
                WikiStrikeAction,
                WikiSubscriptAction,
                WikiSuperscriptAction,
                WikiFontSizeBigAction,
                WikiFontSizeSmallAction,
                WikiMonospaceAction,
                WikiAlignLeftAction,
                WikiAlignRightAction,
                WikiAlignCenterAction,
                WikiAlignJustifyAction,
                WikiPreformatAction,
                WikiNonParsedAction,
                WikiListBulletsAction,
                WikiListNumbersAction,
                WikiHeading1Action,
                WikiHeading2Action,
                WikiHeading3Action,
                WikiHeading4Action,
                WikiHeading5Action,
                WikiHeading6Action,
                WikiThumbAction,
                WikiLinkAction,
                WikiAnchorAction,
                WikiHorLineAction,
                WikiLineBreakAction,
                WikiEquationAction,
                WikiEscapeHtmlAction,
                WikiAttachListAction,
                WikiChildListAction,
                WikiIncludeAction,
                ]

        self._wikiPanelName = "wiki"

        self.mainWindow.toolbars[self._wikiPanelName] = WikiToolBar(self.mainWindow, self.mainWindow.auiManager)
        self.mainWindow.toolbars[self._wikiPanelName].UpdateToolBar()

        self.notebook.SetPageText (0, _(u"Wiki"))

        self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.htmlSizer.AddGrowableRow(0)
        self.htmlSizer.AddGrowableCol(0)

        # Номер вкладки с кодом HTML. -1, если вкладки нет
        self.htmlcodePageIndex = -1

        self.config = WikiConfig (Application.config)

        self.__createCustomTools()
        Application.mainWindow.updateShortcuts()

        if self.config.showHtmlCodeOptions.value:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()


    def onClose (self, event):
        self._removeActionTools()

        if self._wikiPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._wikiPanelName)

        super (WikiPagePanel, self).onClose (event)


    def _removeActionTools (self):
        actionController = Application.actionController

        # Удалим элементы меню
        map (lambda action: actionController.removeMenuItem (action.stringId), 
                self.__wikiNotationActions)

        actionController.removeMenuItem (WikiOpenHtmlCodeAction.stringId)
        actionController.removeMenuItem (WikiUpdateHtmlAction.stringId)
        actionController.removeMenuItem (SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        if self._wikiPanelName in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId), 
                self.__wikiNotationActions)

            actionController.removeToolbarButton (WikiOpenHtmlCodeAction.stringId)
            actionController.removeToolbarButton (SwitchCodeResultAction.stringId)


    @property
    def toolsMenu (self):
        return self.__wikiMenu


    def __createHtmlCodePanel (self, parentSizer):
        # Окно для просмотра получившегося кода HTML
        self.htmlCodeWindow = HtmlTextEditor(self.notebook, -1)
        self.htmlCodeWindow.SetReadOnly (True)
        parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 2)
        
        self.addPage (self.htmlCodeWindow, _("HTML"))
        return self.pageCount - 1
    

    def GetTextEditor(self):
        return WikiEditor


    def GetSearchPanel (self):
        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel
        elif self.selectedPageIndex == self.htmlcodePageIndex:
            return self.htmlCodeWindow.searchPanel

        return None


    def onTabChanged(self, event):
        if self._currentpage == None:
            return

        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            self._onSwitchToCode()

        elif self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()

        elif self.selectedPageIndex == self.htmlcodePageIndex:
            self._onSwitchCodeHtml()

        self.savePageTab(self._currentpage)


    def _enableActions (self, enabled):
        actionController = Application.actionController

        self.mainWindow.Freeze()

        map (lambda action: actionController.enableTools (action.stringId, enabled), 
                self.__wikiNotationActions)

        self.mainWindow.Thaw()


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions (True)
        super (WikiPagePanel, self)._onSwitchToCode()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self._enableActions (False)
        super (WikiPagePanel, self)._onSwitchToPreview()


    def _onSwitchCodeHtml (self):
        assert self._currentpage != None

        self._enableActions (False)

        self.Save()
        status_item = 0
        setStatusText (_(u"Page rendered. Please wait…"), status_item)
        Application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

        try:
            self.currentHtmlFile = self.generateHtml (self._currentpage)
            self._showHtmlCode(self.currentHtmlFile)
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
        except OSError as e:
            MessageBox (_(u"Can't save HTML-file\n\n%s") % (unicode (e)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)

        setStatusText (u"", status_item)
        Application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)

        self._enableAllTools ()
        self.htmlCodeWindow.SetFocus()
        self.htmlCodeWindow.Update()


    def _showHtmlCode (self, path):
        try:
            with open (path) as fp:
                text = unicode (fp.read(), "utf8")

                self.htmlCodeWindow.SetReadOnly (False)
                self.htmlCodeWindow.SetText (text)
                self.htmlCodeWindow.SetReadOnly (True)
        except IOError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)
        except OSError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__fontMenu

        # Полужирный шрифт
        Application.actionController.appendMenuItem (WikiBoldAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiBoldAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False)


        # Курсивный шрифт
        Application.actionController.appendMenuItem (WikiItalicAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiItalicAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False)

        # Полужирный курсивный шрифт
        Application.actionController.appendMenuItem (WikiBoldItalicAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiBoldItalicAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold_italic.png"),
                fullUpdate=False)


        # Подчеркнутый шрифт
        Application.actionController.appendMenuItem (WikiUnderlineAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiUnderlineAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False)


        # Зачеркнутый шрифт
        Application.actionController.appendMenuItem (WikiStrikeAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiStrikeAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False)


        # Нижний индекс
        Application.actionController.appendMenuItem (WikiSubscriptAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiSubscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False)


        # Верхний индекс
        Application.actionController.appendMenuItem (WikiSuperscriptAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiSuperscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False)


        # Крупный шрифт
        Application.actionController.appendMenuItem (WikiFontSizeBigAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiFontSizeBigAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_big.png"),
                fullUpdate=False)


        # Мелкий шрифт
        Application.actionController.appendMenuItem (WikiFontSizeSmallAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiFontSizeSmallAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_small.png"),
                fullUpdate=False)


        # Моноширинный шрифт
        Application.actionController.appendMenuItem (WikiMonospaceAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiMonospaceAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_monospace.png"),
                fullUpdate=False)


    def __addAlignTools (self):
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__alignMenu

        # Выравнивание по левому краю
        Application.actionController.appendMenuItem (WikiAlignLeftAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignLeftAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False)


        # Выравнивание по центру
        Application.actionController.appendMenuItem (WikiAlignCenterAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignCenterAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False)


        # Выравнивание по правому краю
        Application.actionController.appendMenuItem (WikiAlignRightAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignRightAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False)


        # Выравнивание по ширине
        Application.actionController.appendMenuItem (WikiAlignJustifyAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignJustifyAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False)


    def __addFormatTools (self):
        menu = self.__formatMenu

        # Форматированный текст
        Application.actionController.appendMenuItem (WikiPreformatAction.stringId, menu)

        # Текст, который не нужно разбирать википарсером
        Application.actionController.appendMenuItem (WikiNonParsedAction.stringId, menu)


    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__listMenu

        # Ненумерованный список
        Application.actionController.appendMenuItem (WikiListBulletsAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiListBulletsAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False)


        # Нумерованный список
        Application.actionController.appendMenuItem (WikiListNumbersAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiListNumbersAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False)


    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__headingMenu

        Application.actionController.appendMenuItem (WikiHeading1Action.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHeading1Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (WikiHeading2Action.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHeading2Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (WikiHeading3Action.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHeading3Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (WikiHeading4Action.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHeading4Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (WikiHeading5Action.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHeading5Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (WikiHeading6Action.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHeading6Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False)


    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        # Добавить миниатюру
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__wikiMenu

        Application.actionController.appendMenuItem (WikiThumbAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiThumbAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "images.png"),
                fullUpdate=False)


        # Вставка ссылок
        Application.actionController.appendMenuItem (WikiLinkAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiLinkAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False)


        # Вставка якоря
        Application.actionController.appendMenuItem (WikiAnchorAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAnchorAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False)


        # Вставка горизонтальной линии
        Application.actionController.appendMenuItem (WikiHorLineAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiHorLineAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False)


        # Вставка разрыва страницы
        Application.actionController.appendMenuItem (WikiLineBreakAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiLineBreakAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "linebreak.png"),
                fullUpdate=False)


        # Вставка формулы
        Application.actionController.appendMenuItem (WikiEquationAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiEquationAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "equation.png"),
                fullUpdate=False)


        self.__wikiMenu.AppendSeparator()

        # Преобразовать некоторые символы в и их HTML-представление
        Application.actionController.appendMenuItem (WikiEscapeHtmlAction.stringId, menu)


    def _addRenderTools (self):
        Application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        Application.actionController.appendToolbarButton (SwitchCodeResultAction.stringId, 
                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                os.path.join (self.imagesDir, "render.png"),
                fullUpdate=False)


    def __createCustomTools (self):
        assert self.mainWindow != None

        self.__wikiMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__commandsMenu = wx.Menu()

        self.mainWindow.Freeze()

        self._addRenderTools()

        # Переключиться на код HTML
        Application.actionController.appendMenuItem (WikiOpenHtmlCodeAction.stringId, self.__wikiMenu)
        Application.actionController.appendToolbarButton (WikiOpenHtmlCodeAction.stringId, 
                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                os.path.join (self.imagesDir, "html.png"),
                fullUpdate=False)

        # Обновить код HTML
        Application.actionController.appendMenuItem (WikiUpdateHtmlAction.stringId, self.__wikiMenu)

        self.toolsMenu.AppendSeparator()

        self.__wikiMenu.AppendSubMenu (self.__headingMenu, _(u"Heading"))
        self.__wikiMenu.AppendSubMenu (self.__fontMenu, _(u"Font"))
        self.__wikiMenu.AppendSubMenu (self.__alignMenu, _(u"Alignment"))
        self.__wikiMenu.AppendSubMenu (self.__formatMenu, _(u"Formatting"))
        self.__wikiMenu.AppendSubMenu (self.__listMenu, _(u"Lists"))
        self.__wikiMenu.AppendSubMenu (self.__commandsMenu, _(u"Commands"))

        self.__addCommandsTools()
        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addListTools()
        self.__addFormatTools()
        self.__addOtherTools()

        Application.mainWindow.updateShortcuts()

        self.mainWindow.mainMenu.Insert (self.__WIKI_MENU_INDEX, 
                self.__wikiMenu, 
                _(u"Wiki") )

        self.mainWindow.Thaw()


    @property
    def commandsMenu (self):
        """
        Свойство возвращает меню с викикомандами
        """
        return self.__commandsMenu


    def __addCommandsTools (self):
        # Команда (:attachlist:)
        Application.actionController.appendMenuItem (WikiAttachListAction.stringId, self.commandsMenu)

        # Команда (:childlist:)
        Application.actionController.appendMenuItem (WikiChildListAction.stringId, self.commandsMenu)

        # Команда (:include:)
        Application.actionController.appendMenuItem (WikiIncludeAction.stringId, self.commandsMenu)


    @BaseHtmlPanel.selectedPageIndex.setter
    def selectedPageIndex (self, index):
        """
        Устанавливает выбранную страницу (код, просмотр или полученный HTML)
        """
        if index == self.HTML_RESULT_PAGE_INDEX and self.htmlcodePageIndex == -1:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)
            selectedPage = self.htmlcodePageIndex
        else:
            selectedPage = index

        BaseHtmlPanel.selectedPageIndex.fset (self, selectedPage)


    def openHtmlCode (self):
        self.selectedPageIndex = self.HTML_RESULT_PAGE_INDEX


    def generateHtml (self, page):
        style = Style()
        stylepath = style.getPageStyle (page)
        generator = HtmlGenerator (page)

        try:
            html = generator.makeHtml(stylepath)
        except:
            MessageBox (_(u"Page style Error. Style by default is used"),  
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

            html = generator.makeHtml (style.getDefaultStyle())

        return html


    def removeGui (self):
        super (WikiPagePanel, self).removeGui ()
        self.mainWindow.mainMenu.Remove (self.__WIKI_MENU_INDEX - 1)


    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений

        Перегрузка метода из BaseTextPanel
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += "Attach:" + fnames[n]
            if n != count -1:
                text += "\n"

        return text


    def updateHtml (self):
        """
        Сбросить кэш для того, чтобы заново сделать HTML
        """
        HtmlGenerator (self._currentpage).resetHash()
        if self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()
        elif self.selectedPageIndex == self.HTML_RESULT_PAGE_INDEX:
            self._onSwitchCodeHtml()
