# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri May 21 21:49:10 2010

import codecs
import os.path
import cgi

import wx
import wx.html
from wx.stc import StyledTextCtrl

from gui.LocalSearchPanel import LocalSearchPanel, LocalSearcher
import core.system
from core.application import Application
from guiconfig import EditorConfig
from core.htmltemplate import HtmlTemplate
from core.system import getTemplatesDir

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class TextEditor(wx.Panel):
	_fontConfigSection = "Font"

	def __init__(self, *args, **kwds):
		# begin wxGlade: TextEditor.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.textCtrl = StyledTextCtrl(self, -1)
		self.searchPanel = EditorSearchPanel(self, -1)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		self.createCoders()

		self.config = EditorConfig (Application.config)

		self.setDefaultSettings()
		self.searchPanel.setEditor (self, self.textCtrl)
		
		self.textCtrl.Bind(wx.EVT_MENU, self.onCopyFromEditor, id = wx.ID_COPY)
		self.textCtrl.Bind(wx.EVT_MENU, self.onCutFromEditor, id = wx.ID_CUT)
		self.textCtrl.Bind(wx.EVT_MENU, self.onPasteToEditor, id = wx.ID_PASTE)
		self.textCtrl.Bind(wx.EVT_MENU, self.onUndo, id = wx.ID_UNDO)
		self.textCtrl.Bind(wx.EVT_MENU, self.onRedo, id = wx.ID_REDO)
		self.textCtrl.Bind (wx.EVT_CHAR, self.OnChar_ImeWorkaround)
		self.textCtrl.Bind (wx.EVT_KEY_DOWN, self.onKeyDown)


	def Print (self):
		text = self.textCtrl.GetText()
		text = cgi.escape (text, True)
		#text = text.replace ("\r\n", "\n")
		text = text.replace ("\n\n", "<P>")
		text = text.replace ("\n", "<BR>")

		print text

		tpl = HtmlTemplate (os.path.join (getTemplatesDir(), "html") )
		result = tpl.substitute (content=text)

		printout = wx.html.HtmlPrintout()
		printout.SetHtmlText(result)
		printout.SetFonts("Arial", "Courier New")

		data = wx.PrintData()
		data.SetPaperId(wx.PAPER_A4)

		pdd = wx.PrintDialogData(data)
		pdd.SetAllPages(True)

		printer = wx.Printer(pdd)
		printer.Print(self, printout, True)


	def onCopyFromEditor (self, event):
		self.textCtrl.Copy()


	def onCutFromEditor (self, event):
		self.textCtrl.Cut()


	def onPasteToEditor (self, event):
		self.textCtrl.Paste()

	
	def onUndo (self, event):
		self.textCtrl.Undo()
	
	def onRedo (self, event):
		self.textCtrl.Redo()


	def __set_properties(self):
		# begin wxGlade: TextEditor.__set_properties
		pass
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: TextEditor.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		mainSizer.Add(self.textCtrl, 1, wx.EXPAND, 0)
		mainSizer.Add(self.searchPanel, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		# end wxGlade

		self.searchPanel.Hide()
		self.Layout()
	

	def setDefaultSettings (self):
		"""
		Установить шрифт по умолчанию в контрол StyledTextCtrl
		"""
		size = self.config.fontSizeOption.value
		faceName = self.config.fontFaceNameOption.value
		isBold = self.config.fontIsBold.value
		isItalic = self.config.fontIsItalic.value

		#style = "size:%d" % size
		#self.textCtrl.StyleSetSpec (wx.stc.STC_STYLE_DEFAULT, style)

		self.textCtrl.StyleSetSize (wx.stc.STC_STYLE_DEFAULT, size)
		self.textCtrl.StyleSetFaceName (wx.stc.STC_STYLE_DEFAULT, faceName)
		self.textCtrl.StyleSetBold (wx.stc.STC_STYLE_DEFAULT, isBold)
		self.textCtrl.StyleSetItalic (wx.stc.STC_STYLE_DEFAULT, isItalic)
		
		# Заблокируем горячую клавишу Ctrl+D, чтобы использовать ее как добавление закладки
		self.textCtrl.CmdKeyClear (ord ("D"), wx.stc.STC_SCMOD_CTRL)
		self.textCtrl.CmdKeyClear (ord ("R"), wx.stc.STC_SCMOD_CTRL | wx.stc.STC_SCMOD_SHIFT)
		self.textCtrl.SetWrapMode (wx.stc.STC_WRAP_WORD)
		self.textCtrl.SetWrapVisualFlags (wx.stc.STC_WRAPVISUALFLAG_END)

		self._setMarginWidth (self.textCtrl)
		self.textCtrl.SetTabWidth (self.config.tabWidthOption.value)
	

	def _setMarginWidth (self, editor):
		"""
		Установить размер левой области, где пишутся номера строк в зависимости от шрифта
		"""
		linenumbers =  self.config.lineNumbersOption.value
		fontSize = self.config.fontSizeOption.value

		if linenumbers:
			width = int (35.0 / 10.0 * fontSize)
			editor.SetMarginWidth (0, width)
			editor.SetMarginWidth (1, 5)
		else:
			editor.SetMarginWidth (0, 0)
			editor.SetMarginWidth (1, 8)
	

	def calcByteLen(self, text):
		"""Посчитать длину строки в байтах, а не в символах"""
		return len(self.encoder(text)[0])


	def calcBytePos (self, text, pos):
		"""Преобразовать позицию в символах в позицию в байтах"""
		return len(self.encoder (text[: pos] )[0] )


	def createCoders (self):
		encoding = core.system.getOS().inputEncoding

		self._mbcsDec = codecs.getdecoder(encoding)
		self.mbcsEnc = codecs.getencoder(encoding)
		self.encoder = codecs.getencoder("utf-8")
	

	def onKeyDown (self, event):
		key = event.GetKeyCode()

		if key == wx.WXK_ESCAPE:
			self.searchPanel.Close()

		event.Skip()


	def OnChar_ImeWorkaround(self, evt):
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

# end of class TextEditor


class EditorSearchPanel (LocalSearchPanel):
	def __init__ (self, *args, **kwds):
		LocalSearchPanel.__init__ (self, *args, **kwds)
	
		self.editPanel = None
		self.editor = None


	def nextSearch (self):
		"""
		Искать следующее вхождение фразы
		"""
		self.searchTo (self.findNext)
		self.editor.SetFocus()


	def prevSearch (self):
		"""
		Искать предыдущее вхождение фразы
		"""
		self.searchTo (self.findPrev)
		self.editor.SetFocus()
	

	def startSearch (self):
		"""
		Начать поиск
		"""
		text = self.editor.GetSelectedText()

		self.phraseTextCtrl.SetValue (text)
		self.phraseTextCtrl.SetSelection (-1, -1)
		self.phraseTextCtrl.SetFocus ()
	

	def enterSearchPhrase (self):
		self.searchTo (self.findNextOnEnter)
	

	def searchTo (self, direction):
		"""
		Поиск фразы в нужном направлении (вперед / назад)
		direction - функция, которая ищет текст в нужном направлении (findNext / findPrev)
		"""
		assert self.editor != None

		text = self.editor.GetText()
		phrase = self.phraseTextCtrl.GetValue ()

		if len (phrase) == 0:
			self.phraseTextCtrl.SetFocus ()
			#self.startSearch()
			return

		result = direction (text, phrase)
		if result != None:
			self.resultLabel.SetLabel (u"")
			self.editor.SetSelection (self.editPanel.calcBytePos (text, result.position), 
					self.editPanel.calcBytePos (text, result.position + len (result.phrase)) )
		else:
			self.resultLabel.SetLabel (_(u"Not found"))

			#self.editor.SetFocus()

	
	def findNext (self, text, phrase):
		"""
		Найти следующее вхождение
		"""
		searcher = LocalSearcher (text, phrase)

		currpos = self.getCurrPosChars()

		result = None

		for currResult in searcher.result:
			if currResult.position >= currpos:
				result = currResult
				break

		if result == None and len (searcher.result) > 0:
			result = searcher.result[0]

		return result


	def findPrev (self, text, phrase):
		"""
		Найти предыдущее вхождение
		"""
		searcher = LocalSearcher (text, phrase)

		currpos = self.getStartSelectionChars()

		result = None

		for currResult in searcher.result:
			if currResult.position < currpos:
				result = currResult
				#break

		if result == None and len (searcher.result) > 0:
			result = searcher.result[-1]

		return result


	def findNextOnEnter (self, text, phrase):
		"""
		Найти следующее вхождение, но начиная с начала выделения текста
		"""
		searcher = LocalSearcher (text, phrase)

		currpos = self.getStartSelectionChars()

		result = None

		for currResult in searcher.result:
			if currResult.position >= currpos:
				result = currResult
				break

		if result == None and len (searcher.result) > 0:
			result = searcher.result[0]

		return result


	def getCurrPosChars (self):
		"""
		Посчитать текущее положение каретки в символах
		"""
		# Текущая позиция в байтах
		currpos_bytes = self.editor.GetCurrentPos()
		text_left = self.editor.GetTextRange (0, currpos_bytes)

		currpos_chars = len (text_left)

		return currpos_chars


	def getStartSelectionChars (self):
		"""
		Получить позицию начала выделенного текста в символах
		"""
		startsel_bytes = self.editor.GetSelectionStart()
		text_left = self.editor.GetTextRange (0, startsel_bytes)
		currpos = len (text_left)
		return currpos


	def setEditor (self, editPanel, editor):
		self.editPanel = editPanel
		self.editor = editor
	
