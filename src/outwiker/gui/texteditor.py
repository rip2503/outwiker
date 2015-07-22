# -*- coding: utf-8 -*-

import codecs
import cgi
import math
import re
from datetime import datetime, timedelta
import threading

import wx
import wx.lib.newevent
from wx.stc import StyledTextCtrl

import outwiker.core.system
from outwiker.core.application import Application
from outwiker.core.textprinter import TextPrinter
from outwiker.core.spellchecker import SpellChecker
from outwiker.gui.guiconfig import EditorConfig
from outwiker.gui.searchreplacecontroller import SearchReplaceController
from outwiker.gui.searchreplacepanel import SearchReplacePanel
from outwiker.gui.mainid import MainId

ApplyStyleEvent, EVT_APPLY_STYLE = wx.lib.newevent.NewEvent()


class TextEditor(wx.Panel):
    _fontConfigSection = "Font"

    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self._enableSpellChecking = True
        self._spellChecker = None
        self._wordRegex = re.compile ('\w+', re.U)
        self._digitRegex = re.compile ('\d', re.U)

        self.SPELL_ERROR_INDICATOR = 0
        self.SPELL_ERROR_INDICATOR_MASK = wx.stc.STC_INDIC0_MASK

        # Уже были установлены стили текста (раскраска)
        self._styleSet = False
        # Начинаем раскраску кода не менее чем через это время с момента его изменения
        self._DELAY = timedelta (milliseconds=300)

        # Время последней модификации текста страницы.
        # Используется для замера времени после модификации, чтобы не парсить текст
        # после каждой введенной буквы
        self._lastEdit = datetime.now() - self._DELAY * 2

        self._colorizingThread = None

        self.textCtrl = StyledTextCtrl(self, -1)

        # Создание панели поиска и ее контроллера
        self._searchPanel = SearchReplacePanel (self)
        self._searchPanelController = SearchReplaceController (self._searchPanel, self)
        self._searchPanel.setController (self._searchPanelController)

        self.__do_layout()

        self.__createCoders()

        self.config = EditorConfig (Application.config)
        self.__showlinenumbers = self.config.lineNumbers.value

        self.setDefaultSettings()

        self.textCtrl.Bind(wx.EVT_MENU, self.__onCopyFromEditor, id = MainId.ID_COPY)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onCutFromEditor, id = MainId.ID_CUT)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onPasteToEditor, id = MainId.ID_PASTE)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onUndo, id = MainId.ID_UNDO)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onRedo, id = MainId.ID_REDO)
        self.textCtrl.Bind (wx.EVT_CHAR, self.__OnChar_ImeWorkaround)
        self.textCtrl.Bind (wx.EVT_KEY_DOWN, self.__onKeyDown)

        # self.textCtrl.Bind (wx.stc.EVT_STC_STYLENEEDED, self._onStyleNeeded)
        self.textCtrl.Bind (wx.EVT_IDLE, self._onStyleNeeded)
        self.Bind (EVT_APPLY_STYLE, self._onApplyStyle)

        # При перехвате этого сообщения в других классах, нужно вызывать event.Skip(),
        # чтобы это сообщение дошло досюда
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.__onChange)


    @property
    def enableSpellChecking (self):
        return self._enableSpellChecking


    @enableSpellChecking.setter
    def enableSpellChecking (self, value):
        self._enableSpellChecking = value
        self._styleSet = False


    def __onChange (self, event):
        self._styleSet = False
        self._lastEdit = datetime.now()
        self.__setMarginWidth (self.textCtrl)


    @property
    def searchPanel (self):
        """
        Возвращает контроллер панели поиска
        """
        return self._searchPanelController


    def Print (self):
        selectedtext = self.textCtrl.GetSelectedText()
        text = self.textCtrl.GetText()

        printer = TextPrinter (self)
        printer.printout (text if len (selectedtext) == 0 else selectedtext)


    def __onCopyFromEditor (self, event):
        self.textCtrl.Copy()


    def __onCutFromEditor (self, event):
        self.textCtrl.Cut()


    def __onPasteToEditor (self, event):
        self.textCtrl.Paste()


    def __onUndo (self, event):
        self.textCtrl.Undo()


    def __onRedo (self, event):
        self.textCtrl.Redo()


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(rows=2)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        mainSizer.Add(self.textCtrl, 0, wx.EXPAND, 0)
        mainSizer.Add(self._searchPanel, 0, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self._searchPanel.Hide()
        self.Layout()


    def setDefaultSettings (self):
        """
        Установить стили и настройки по умолчанию в контрол StyledTextCtrl
        """
        self._spellChecker = self.getSpellChecker()

        size = self.config.fontSize.value
        faceName = self.config.fontName.value
        isBold = self.config.fontIsBold.value
        isItalic = self.config.fontIsItalic.value
        fontColor = self.config.fontColor.value
        backColor = self.config.backColor.value

        self.__showlinenumbers = self.config.lineNumbers.value
        self.textCtrl.SetEndAtLastLine (False)

        self.textCtrl.StyleSetSize (wx.stc.STC_STYLE_DEFAULT, size)
        self.textCtrl.StyleSetFaceName (wx.stc.STC_STYLE_DEFAULT, faceName)
        self.textCtrl.StyleSetBold (wx.stc.STC_STYLE_DEFAULT, isBold)
        self.textCtrl.StyleSetItalic (wx.stc.STC_STYLE_DEFAULT, isItalic)
        self.textCtrl.StyleSetForeground (wx.stc.STC_STYLE_DEFAULT, fontColor)
        self.textCtrl.StyleSetBackground (wx.stc.STC_STYLE_DEFAULT, backColor)

        self.textCtrl.StyleClearAll()

        self.textCtrl.SetCaretForeground (fontColor)
        self.textCtrl.SetCaretLineBack (backColor)

        # Заблокируем горячую клавишу Ctrl+D, чтобы использовать ее как добавление закладки
        self.textCtrl.CmdKeyClear (ord ("D"), wx.stc.STC_SCMOD_CTRL)
        self.textCtrl.CmdKeyClear (ord ("R"), wx.stc.STC_SCMOD_CTRL | wx.stc.STC_SCMOD_SHIFT)
        self.textCtrl.SetWrapMode (wx.stc.STC_WRAP_WORD)
        self.textCtrl.SetWrapVisualFlags (wx.stc.STC_WRAPVISUALFLAG_END)

        self.__setMarginWidth (self.textCtrl)
        self.textCtrl.SetTabWidth (self.config.tabWidth.value)

        if self.config.homeEndKeys.value == EditorConfig.HOME_END_OF_LINE:
            # Клавиши Home / End переносят курсор на начало / конец строки
            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_HOME,
                                        0,
                                        wx.stc.STC_CMD_HOMEDISPLAY)

            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_HOME,
                                        wx.stc.STC_SCMOD_ALT,
                                        wx.stc.STC_CMD_HOME)

            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_END,
                                        0,
                                        wx.stc.STC_CMD_LINEENDDISPLAY)

            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_END,
                                        wx.stc.STC_SCMOD_ALT,
                                        wx.stc.STC_CMD_LINEEND)
        else:
            # Клавиши Home / End переносят курсор на начало / конец абзаца
            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_HOME,
                                        0,
                                        wx.stc.STC_CMD_HOME)

            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_HOME,
                                        wx.stc.STC_SCMOD_ALT,
                                        wx.stc.STC_CMD_HOMEDISPLAY)

            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_END,
                                        0,
                                        wx.stc.STC_CMD_LINEEND)

            self.textCtrl.CmdKeyAssign (wx.stc.STC_KEY_END,
                                        wx.stc.STC_SCMOD_ALT,
                                        wx.stc.STC_CMD_LINEENDDISPLAY)

        self.textCtrl.IndicatorSetStyle(self.SPELL_ERROR_INDICATOR, wx.stc.STC_INDIC_SQUIGGLE)
        self.textCtrl.IndicatorSetForeground(self.SPELL_ERROR_INDICATOR, "red")


    def __setMarginWidth (self, editor):
        """
        Установить размер левой области, где пишутся номера строк в зависимости от шрифта
        """
        if self.__showlinenumbers:
            editor.SetMarginWidth (0, self.__getMarginWidth())
            editor.SetMarginWidth (1, 5)
        else:
            editor.SetMarginWidth (0, 0)
            editor.SetMarginWidth (1, 8)


    def __getMarginWidth (self):
        """
        Расчет размера серой области с номером строк
        """
        fontSize = self.config.fontSize.value
        linescount = len (self.GetText().split("\n"))

        if linescount == 0:
            width = 10
        else:
            # Количество десятичных цифр в числе строк
            digits = int (math.log10 (linescount) + 1)
            width = int (1.2 * fontSize * digits)

        return width


    def calcByteLen(self, text):
        """Посчитать длину строки в байтах, а не в символах"""
        return len(self.encoder(text)[0])


    def calcBytePos (self, text, pos):
        """Преобразовать позицию в символах в позицию в байтах"""
        return len(self.encoder (text[: pos])[0])


    def __createCoders (self):
        encoding = outwiker.core.system.getOS().inputEncoding

        self.mbcsEnc = codecs.getencoder(encoding)
        self.encoder = codecs.getencoder("utf-8")


    def __onKeyDown (self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self._searchPanel.Close()

        event.Skip()


    def __OnChar_ImeWorkaround(self, evt):
        """
        Обработка клавиш вручную, чтобы не было проблем с вводом русских букв в Linux.
        Основа кода взята из Wikidpad (WikiTxtCtrl.py -> OnChar_ImeWorkaround)
        """
        key = evt.GetKeyCode()

        # Return if this doesn't seem to be a real character input
        if evt.ControlDown() or (0 < key < 32):
            evt.Skip()
            return

        if key >= wx.WXK_START and evt.GetUnicodeKey() != key:
            evt.Skip()
            return

        unichar = unichr(evt.GetUnicodeKey())

        self.textCtrl.ReplaceSelection(self.mbcsEnc (unichar, "replace")[0])


    def AddText (self, text):
        self.textCtrl.AddText (text)


    def replaceText (self, text):
        self.textCtrl.ReplaceSelection (text)


    def turnText (self, lefttext, righttext):
        selText = self.textCtrl.GetSelectedText()
        newtext = lefttext + selText + righttext
        self.textCtrl.ReplaceSelection (newtext)

        currPos = self.GetSelectionEnd()
        if len (selText) == 0:
            """
            Если не оборачиваем текст, а делаем пустой тег, то поместим каретку до закрывающегося тега
            """
            newpos = currPos - len (righttext)
            self.SetSelection (newpos, newpos)
        else:
            self.SetSelection (currPos - len (selText) - len (righttext),
                               currPos - len (righttext))


    def escapeHtml (self):
        selText = self.textCtrl.GetSelectedText()
        text = cgi.escape (selText, quote=False)
        self.textCtrl.ReplaceSelection (text)


    def SetReadOnly (self, readonly):
        self.textCtrl.SetReadOnly (readonly)


    def GetReadOnly (self):
        return self.textCtrl.GetReadOnly()


    def GetText(self):
        return self.textCtrl.GetText()


    def SetText (self, text):
        self.textCtrl.SetText (text)


    def EmptyUndoBuffer (self):
        self.textCtrl.EmptyUndoBuffer()


    def GetSelectedText (self):
        return self.textCtrl.GetSelectedText()


    def SetSelection (self, start, end):
        """
        start и end в символах, а не в байтах, в отличие от исходного StyledTextCtrl
        """
        startText = self.GetText()[:start]
        endText = self.GetText()[:end]

        firstByte = self.calcByteLen (startText)
        endByte = self.calcByteLen (endText)

        self.textCtrl.SetSelection (firstByte, endByte)


    def GetCurrentPosition (self):
        """
        Возвращает номер символа (а не байта), перед которых находится курсор
        """
        return self.__calcCharPos (self.textCtrl.GetCurrentPos())


    def GetSelectionStart (self):
        """
        Возвращает позицию начала выбранной области в символах, а не в байтах
        """
        return self.__calcCharPos (self.textCtrl.GetSelectionStart())


    def GetSelectionEnd (self):
        """
        Возвращает позицию конца выбранной области в символах, а не в байтах
        """
        return self.__calcCharPos (self.textCtrl.GetSelectionEnd())


    def SetFocus (self):
        self.textCtrl.SetFocus()
        self.textCtrl.SetSTCFocus(True)


    def __calcCharPos (self, pos_bytes):
        """
        Пересчет позиции в байтах в позицию в символах
        """
        text_left = self.textCtrl.GetTextRange (0, pos_bytes)
        currpos = len (text_left)
        return currpos


    def checkSpellWord (self, word):
        match = self._digitRegex.search (word)
        if match is not None:
            return True

        return self._spellChecker.check (word)


    def _getTextForParse (self):
        # Табуляция в редакторе считается за несколько символов
        return self.textCtrl.GetText().replace ("\t", " ")


    def setSpellError (self, stylelist, startpos, endpos):
        """
        Mark positions as error
        startpos, endpos - positions in characters
        """
        text = self._getTextForParse()
        startbytes = self.calcBytePos (text, startpos)
        endbytes = self.calcBytePos (text, endpos)

        self.addStyle (stylelist, self.SPELL_ERROR_INDICATOR_MASK, startbytes, endbytes)


    def addStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет (с помощью операции побитового ИЛИ) стиль с идентификатором styleid к массиву байт stylelist
        """
        style_src = stylelist[bytepos_start: bytepos_end]
        style_new = [style | styleid for style in style_src]

        stylelist[bytepos_start: bytepos_end] = style_new


    def setStyle (self, stylelist, styleid, bytepos_start, bytepos_end):
        """
        Добавляет стиль с идентификатором styleid к массиву байт stylelist
        """
        stylelist[bytepos_start: bytepos_end] = [styleid] * (bytepos_end - bytepos_start)


    def runSpellChecking (self, stylelist, start, end):
        if not self._enableSpellChecking:
            return

        text = self._getTextForParse()[start: end]

        words = self._wordRegex.finditer (text)
        for wordMatch in words:
            word = wordMatch.group(0)
            if not self.checkSpellWord (word):
                self.setSpellError (stylelist, wordMatch.start() + start, wordMatch.end() + start)


    def _onStyleNeeded (self, event):
        if (not self._styleSet and
                datetime.now() - self._lastEdit >= self._DELAY and
                (self._colorizingThread is None or not self._colorizingThread.isAlive())):
            text = self._getTextForParse()
            self._colorizingThread = threading.Thread (None, self._colorizeThreadFunc, args=(text,))
            self._colorizingThread.start()


    def _colorizeThreadFunc (self, text):
        stylebytes = self.getStyleBytes (text)
        indicatorsbytes = self.getIndcatorsStyleBytes (text)
        event = ApplyStyleEvent (text=text,
                                 stylebytes=stylebytes,
                                 indicatorsbytes = indicatorsbytes)
        wx.PostEvent (self, event)


    def _onApplyStyle (self, event):
        if event.text == self._getTextForParse():
            stylebytes = event.stylebytes
            indicatorsbytes = event.indicatorsbytes

            if stylebytes is not None:
                self.textCtrl.StartStyling (0, 0xff ^ wx.stc.STC_INDICS_MASK)
                self.textCtrl.SetStyleBytes (len (stylebytes), stylebytes)

            if indicatorsbytes is not None:
                self.textCtrl.StartStyling (0, wx.stc.STC_INDICS_MASK)
                self.textCtrl.SetStyleBytes (len (indicatorsbytes), indicatorsbytes)

            self._styleSet = True


    def getStyleBytes (self, text):
        """
        Функция должна возвращать список байт, описывающих раскраску (стили)
        для текста text (за исключением индикаторов).
        Функцию нужно переопределить, если используется собственная раскраска текста.
        Исли функция возвращает None, то раскраска синтаксиса не применяется.
        """
        return None


    def getIndcatorsStyleBytes (self, text):
        """
        Функция должна возвращать список байт, описывающих раскраску (стили индикаторов) для текста text.
        Функцию нужно переопределить, если используются индикаторы.
        Исли функция возвращает None, то раскраска индикаторов не применяется.
        """
        return None


    def getSpellChecker (self):
        langlist = ["ru_RU", "en_US"]
        return SpellChecker (langlist,
                             outwiker.core.system.getSpellDirList())
