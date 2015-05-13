��    "      ,  /   <      �  ,   �  %   &     L     l     �     �     �     �     �     �  '   �            -   '  o   U  m   �  i   3  n   �               .     3     M     k  �       J  :   V     �  ;   �  >   �     &  
   ,  *   7  �  b  Q   Z  B   �  6   �  D   &     k  %        �  0   �  2   �       E   #  %   i     �  D   �  �   �  �   �  �   o  �   %     �  &   �       >   ,  "   k  6   �  D  �  #   
  �   .  0   �  �   �  �   a     �  !     (   #                                       	                                             !                                    
          "                            %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Error Executables (*.exe)|*.exe|All Files|*.* External Tools [Plugin] ExternalTools ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Link Open Content File with... Open Result HTML File with... Open file dialog... Open notes files with external editor.

For OutWiker 1.9 and above ExternalTools adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command has the following optional parameters:
<ul>
<li>format. If the parameter equals "button" command will create a button instead of a link.</li>
<li>title. The parameter sets the text for link or button.</li>
</ul>

The (:exec:) command allow to run many applications. Every application must writed on the separated lines.

If line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.

<b>Examples</b>

Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>

Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>

Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code>

Run many applications:
<code><pre>(:exec text="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>
 Remove tool Run application by ExternalTools plugin?
It may be unsafe. Run applications (:exec:) Run applications by ExternalTools plugin?
It may be unsafe. Show warning before executing applications by (:exec:) command Title Tools List http://jenyay.net/Outwiker/ExternalToolsEn Project-Id-Version: externaltools
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2015-05-13 22:18+0300
PO-Revision-Date: 2015-05-13 22:23+0300
Last-Translator: Eugeniy Ilin <jenyay.ilin@gmail.com>
Language-Team: jenyay.net <jenyay.ilin@gmail.com>
Language: ru_RU
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Poedit-KeywordsList: _;gettext;gettext_noop
X-Poedit-Basepath: ../../..
X-Poedit-SourceCharset: utf-8
X-Generator: Poedit 1.5.4
X-Poedit-SearchPath-0: .
 %attach%. Путь до текущей папки вложенных файлов %folder%. Путь до папки текущей страницы %html%. Текущая страница. Файл HTML %page%. Текущая страница. Текстовый файл Все файлы|* Добавить приложение Кнопка Ошибка запуска приложения Ошибка сохранения настроек Ошибка Выполняемые файлы (*.exe)|*.exe|Все файлы|*.* External Tools [Расширение] ExternalTools Плагин ExternalTools. Вставить команду (:exec:) Плагин ExternalTools. Вставить макрос %attach%. Этот макрос будет заменен на путь до папки с вложенными файлами текущей страницы. Плагин ExternalTools. Вставить макрос %folder%. Этот макрос будет заменен на путь до папки текущей страницы. Плагин ExternalTools. Вставить макрос %html%. Этот макрос будет заменен на путь до файла HTML текущей страницы. Плагин ExternalTools. Вставить макрос %page%. Этот макрос будет заменен на путь до текстового файла текущей страницы. Формат Вставка команды (:exec:) Ссылка Открыть файл с текстом заметки в... Открыть HTML-файл в... Открыть диалог выбора файла... Открывает файлы заметок во внешних редакторах.

Для OutWiker 1.9 и выше ExternalTools добавляет команду (:exec:) для создания ссылки или кнопки для запуска внешних приложений с викистраницы.

Команда (:exec:) имеет следующие необязательные параметры:
<ul>
<li>format. Если этот параметр равен "button", то команда создаст кнопку вместо ссылки (по умолчанию).</li>
<li>title. Этот параметр устанавливает текст для ссылки или кнопки.</li>
</ul>

Команда (:exec:) позволяет запускать несколкьо приложений. Каждое приложение должно быть записано на отдельной строке.

Если строка начинается с "#", то эта строка игнорируется. "#" в начале строки - это знак комментария.

<b>Примеры</b>

Создание ссылки для запуска application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>

То же самое, но для создания кнопки
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>

Создать ссылку для запуска application.exe с параметрами:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code>

Запустить несколько приложений:
<code><pre>(:exec text="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>
 Удалить приложение Запустить приложение с помощью плагина ExternalTools?
Это может быть опасно. Запустить приложения (:exec:) Запустить приложения с помощью плагина ExternalTools?
Это может быть опасно. Показывать предупреждение перед запуском
приложений с помощью команды (:exec:) Заголовок Список приложений http://jenyay.net/Outwiker/ExternalTools 