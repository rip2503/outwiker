# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp, NamedTemporaryFile
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir


class GraphBuilderTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.GraphBuilder = self.loader[u'DataGraph'].GraphBuilder

        self._defaultWidth = 700
        self._defaultHeight = 400

        self.path = mkdtemp (prefix=u'Абырвалг абыр')
        self.wikiroot = WikiDocument.create (self.path)
        self.page = WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        Application.wikiroot = None


    def tearDown (self):
        self.loader.clear()
        Application.wikiroot = None
        removeDir (self.path)


    def testEmpty (self):
        params = {}
        content = u''
        page = None

        builder = self.GraphBuilder(params, content, page)
        graph = builder.graph

        self.assertEqual (graph.getProperty (u'width', 0), self._defaultWidth)
        self.assertEqual (graph.getProperty (u'height', 0), self._defaultHeight)

        self.assertEqual (graph.getProperty (u'Width', 0), self._defaultWidth)
        self.assertEqual (graph.getProperty (u'HEIGHT', 0), self._defaultHeight)

        self.assertIsNotNone (graph.getObject (u'pane'))
        self.assertIsNotNone (graph.getObject (u'PANE'))
        self.assertIsNotNone (graph.getObject (u'pane1'))
        self.assertIsNotNone (graph.getObject (u'PANE1'))

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))


    def testGraphProperties (self):
        params = {
            u'width': 100,
            u'height': 150,

            u'pane.title': u'Заголовок графика',

            # invalid values
            u'pane': u'Бла-бла-бла',
            u'abyrvalg': u'Абырвалг',
            u'Абырвалг': u'Главрыба',
            u'qwerty.qw': 42,
            u'qwerty.qw.sss': 42,
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        pane = graph.getObject (u'pane')

        self.assertIsNotNone (pane)
        self.assertIsNotNone (graph.getObject(u'pane1'))

        self.assertEqual (graph.getProperty (u'width', 0), 100)
        self.assertEqual (graph.getProperty (u'height', 0), 150)

        self.assertEqual (pane.getProperty (u'title', None), u'Заголовок графика')

        self.assertEqual (graph.getProperty (u'abyrvalg', None), u'Абырвалг')
        self.assertEqual (graph.getProperty (u'Абырвалг', None), u'Главрыба')


    def testCurvesCount_01 (self):
        params = {
            'curve2': u'Абырвалг',
            'curve3': u'Абырвалг',
            'curve23sdf': u''
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNone (graph.getObject (u'curve2'))
        self.assertIsNone (graph.getObject (u'curve3'))
        self.assertIsNone (graph.getObject (u'curve23sdf'))


    def testCurvesCount_02 (self):
        params = {
            'curve.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))


    def testCurvesCount_03 (self):
        params = {
            'curve1.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))


    def testCurvesCount_04 (self):
        params = {
            'curve2.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph

        self.assertIsNotNone (graph.getObject (u'curve'))
        self.assertIsNotNone (graph.getObject (u'curve1'))
        self.assertIsNotNone (graph.getObject (u'curve2'))


    def testCurveProperties_01 (self):
        params = {
            'curve.property': u'Абырвалг',
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')
        curve1 = graph.getObject (u'curve1')

        self.assertEqual (curve, curve1)
        self.assertEqual (curve.getProperty (u'property', None), u'Абырвалг')

        self.assertEqual (curve.getProperty (u'xcol', 42), None)
        self.assertEqual (curve.getProperty (u'ycol', 42), 1)
        self.assertEqual (curve.getProperty (u'data', 42), None)


    def testCurveData_01 (self):
        params = {
            u'curve.data.colsep': u',',
        }
        content = u''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        self.assertIsNotNone (curve)
        self.assertIsNone (curve.getProperty (u'data', 'xxx'))

        data = curve.getObject (u'data')
        self.assertIsNotNone (data)

        self.assertEqual (data.getProperty (u'colsep', None), u',')


    def testCurveData_02 (self):
        params = {}
        content = u'''123
456
789'''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123'], [u'456'], [u'789']])


    def testCurveData_03 (self):
        params = {}
        content = u'''123    111
456    222
789    333'''
        page = None

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123', u'111'], [u'456', u'222'], [u'789', u'333']])


    def testCurveAttachData_01 (self):
        data = u'''123
456
789'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            u'curve.data': 'Attach:{}'.format (attachname),
        }
        content = u''
        page = self.page

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123'], [u'456'], [u'789']])


    def testCurveAttachData_02 (self):
        data = u'''123
456
789'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            u'curve.data': attachname,
        }
        content = u''
        page = self.page

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123'], [u'456'], [u'789']])


    def testCurveAttachData_03 (self):
        params = {
            u'curve.data': u'invalid_fname.txt',
        }
        content = u''
        page = self.page

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [])


    def testCurveAttachData_04 (self):
        data = u'''123    111
456    222
789    333'''

        attachname = self._saveDataAndAttach (self.page, data)
        params = {
            u'curve.data': 'Attach:{}'.format (attachname),
        }
        content = u''
        page = self.page

        builder = self.GraphBuilder (params, content, page)
        graph = builder.graph
        curve = graph.getObject (u'curve')

        curveData = curve.getObject (u'data')

        self.assertIsNotNone (curveData)
        self.assertIsNotNone (curveData.getSource())

        data = list (curveData.getRowsIterator())
        self.assertEqual (data, [[u'123', u'111'], [u'456', u'222'], [u'789', u'333']])


    def _saveDataAndAttach (self, page, data):
        with NamedTemporaryFile ('w') as tempfile:
            tempfile.write (data)
            tempfile.flush()

            Attachment(page).attach ([tempfile.name])
            name = os.path.basename (tempfile.name)

        return name
