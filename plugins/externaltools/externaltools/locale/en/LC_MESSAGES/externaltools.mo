��    "      ,  /   <      �  ,   �  %   &     L     l     �     �     �     �     �     �  '   �            -   '  o   U  m   �  i   3  n   �               .     3     M     k  �       J  :   V     �  ;   �  >   �     &  
   ,  *   7  �  b  ,   Z  %   �     �     �     �     �               !     4  '   :     b     z  -   �  o   �  m   &  i   �  n   �     m     t     �     �     �     �  �  �     �  :   �     �  ;     >   H     �  
   �  *   �                                       	                                             !                                    
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
PO-Revision-Date: 2015-05-13 22:18+0300
Last-Translator: Eugeniy Ilin <jenyay.ilin@gmail.com>
Language-Team: jenyay.net <jenyay.ilin@gmail.com>
Language: en_GB
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Poedit-KeywordsList: _;gettext;gettext_noop
X-Poedit-Basepath: ../../..
X-Poedit-SourceCharset: utf-8
X-Generator: Poedit 1.5.4
X-Poedit-SearchPath-0: .
 %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Error Executables (*.exe)|*.exe|All Files|*.* External Tools [Plugin] ExternalTools ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Link Open Content File with... Open Result HTML File with... Open file dialog... Open notes files with external editor.

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
It may be unsafe. Show warning before executing applications by (:exec:) command Title Tools List http://jenyay.net/Outwiker/ExternalToolsEn 