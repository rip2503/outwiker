# -*- coding: utf-8 -*-

import os
import os.path
import gettext
import locale
import logging

import wx

from .config import StringOption
from .system import getCurrentDir


# Константа, показывающая, что язык нужно определить самостоятельно
AUTO_LANGUAGE = u"Auto"


class I18nConfig(object):
    """Настройки, связанные с локализацией"""

    def __init__(self, config):
        self.config = config

        self.languageOption = StringOption(self.config,
                                           u"General",
                                           u"language",
                                           AUTO_LANGUAGE)


def getDefaultLanguage():
    return locale.getdefaultlocale()[0]


def init_i18n(language):
    langdir = os.path.join(getCurrentDir(), u'locale')
    lang = loadLanguage(language, langdir, u"outwiker")
    assert lang is not None
    lang.install()
    return lang


def loadLanguage(language, langdir, domain):
    """
    Загрузить язык из указанной директории
    language - язык, который надо загрузить или константа AUTO_LANGUAGE
    """
    # Если в качестве языка передана константа AUTO_LANGUAGE,
    # значит язык надо определить самостоятельно
    reallanguage = (getDefaultLanguage()
                    if language == AUTO_LANGUAGE
                    else language)

    try:
        lang = gettext.translation(domain,
                                   langdir,
                                   languages=[reallanguage, 'en'])
    except IOError:
        return None

    return lang


def getLanguageFromConfig(config):
    """
    Прочитать настройку языка из конфига
    """
    i18config = I18nConfig(config)
    language = i18config.languageOption.value
    return language


def isLangDir(root, folder):
    """
    Возвращает True, если path - путь до папки с локализацией
    """
    path = os.path.join(root, folder)

    if not os.path.isdir(path):
        return False

    messdir = os.path.join(path, u"LC_MESSAGES")
    if not os.path.exists(messdir) or not os.path.isdir(messdir):
        return False

    langfile = os.path.join(messdir, u"outwiker.mo")
    if not os.path.exists(langfile):
        return False

    return True


def getLanguages():
    """
    Получить список всех языков, находящихся в папке locale
    """
    langdir = os.path.join(getCurrentDir(), u'locale')

    languages = []
    for folder in os.listdir(langdir):
        if isLangDir(langdir, folder):
            languages.append(folder)

    return languages


def initLocale(config):
    """
    Locale initialization

    config - instance of the outwiker.core.config.Config class
    """
    locale = None
    language = getLanguageFromConfig(config)
    try:
        init_i18n(language)
    except IOError:
        logging.warning(u"Can't load language: {}".format(language))

    if wx.GetApp() is not None:
        locale = wx.Locale(wx.LANGUAGE_DEFAULT)

    return locale
