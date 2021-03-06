��    +      t  ;   �      �  ,   �  %   �          ,     L     X     e     l     �  �   �  g   2     �     �  '   �  �   �     �     �  �  �  -   {  o   �  m   	  i   �	  n   �	     `
     g
  �  �
     V     [     u  x   �             �   ,  :        @  ;   Z  e   �  �   �     �  
   �  6     +   ;  �  g  +     )   9  "   c  "   �     �     �     �  &   �  )   �  �   !  o   �     :  	   A  5   K  �   �     p     �  �  �  -   J  }   x  {   �  }   r  }   �     n     u  �  �     �     �  !   �  �   �     B     `  �   s  L   R     �  N   �  o     �   ~     y       F   �  +   �                  (                             '                
           %         !             "      	                                   &          )                   $       +   *      #               %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Error Examples Executables (*.exe)|*.exe|All Files|*.* Execute application.exe from attachments folder:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
or
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code> External Tools [Plugin] ExternalTools ExternalTools plug-in allows to open the notes files with external applications.

The plug-in adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command allows to run many applications. Every application must be placed at the separated lines.

If a line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.
 ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Inside (:exec:) command may be macroses. The macroses will be replaced by appropriate paths:
<ul>
<li><b>%page%</b>. The macros will be replaced by full path to page text file.</li>
<li><b>%html%</b>. The macros will be replaced by full path to HTML content file.</li>
<li><b>%folder%</b>. The macros will be replaced by full path to page folder.</li>
<li><b>%attach%</b>. The macros will be replaced by full path to attach folder without slash on the end.</li>
</ul> Link Open Content File with... Open Result HTML File with... Open attached file with application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code> Open file dialog... Remove tool Run a lot of applications:
<code><pre>(:exec title="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Run application by ExternalTools plugin?
It may be unsafe. Run applications (:exec:) Run applications by ExternalTools plugin?
It may be unsafe. Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> The (:exec:) command has the following optional parameters:
<ul>
<li><b>format</b>. If the parameter equals "button" command will create a button instead of a link.</li>
<li><b>title</b>. The parameter sets the text for link or button.</li>
</ul> Title Tools List Warn before executing applications by (:exec:) command https://jenyay.net/Outwiker/ExternalToolsEn Project-Id-Version: outwiker
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2018-08-23 13:02+0300
Last-Translator: Jenyay <jenyay.ilin@gmail.com>
Language-Team: German
Language: de_DE
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: Poedit 2.0.6
X-Crowdin-Project: outwiker
X-Crowdin-Language: de
X-Crowdin-File: externaltools.po
 %attach%. Pfad zu aktuellem Anhänge Ordner %folder%. Pfad zu aktuellem Seiten Ordner %html%. Aktuelle Seite. HTML-Datei %page%. Aktuelle Seite. Text-Datei Alle Dateien|* Tools hinzufügen Knopf Werkzeug kann nicht ausgeführt werden Optionen können nicht gespeichert werden Erstellt einen Link zum ausführenvon application.exe mit Parameter:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Erstellt einen Link um application.exe auszuführen:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Fehler Beispiele Ausführbare Dateien (*.exe)|*.exe|alle Dateien| *. * Führen Sie application.exe aus Anhängeordner aus: 
<code><pre>(:exec:) 
%attach%/application.exe %attach%/my_file.txt
 (:execend:)</pre></code>
oder
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
 (:execend:)</pre></code> Externe Tools [Plugin] ExternalTools ExternalTools-Plug-in ermöglicht es, um die Notizen mit externen Applikationen zu öffnen.

Das Plugin fügt den (:exec:) Befehl hinzu, erstellt einen Link oder Knopf um mit externer Anwendung auszuführen.

Der (:exec:) Befehl erlaubt es mehrere Anwendungen auszuführen. Jede Anwendung muss als eingene Linie angegeben werden.

Wen die Zeile mit "#" beginnt, wird diese Zeile ignoriert. "#" als Begin einer Zeile ist ein Kommentar. 
 ExternalTools Plugin. Einfügebefehl (:exec:) ExternalTools Plugin. Ein %attach% -Makro einfügen. Die Makros werden durch einen Pfad zur aktuellen Anhängeordner ersetzt. ExternalTools Plugin. Ein %folder% -Makro einfügen. Die Makros werden durch einen Pfad zur aktuellen Seitenordner ersetzt. ExternalTools Plugin. Ein %html% -Makro einfügen. Die Makros werden durch einen Pfad zur aktuellen Seite HTML-Datei ersetzt. ExternalTools Plugin. Ein %page% -Makro einfügen. Die Makros werden durch einen Pfad zur aktuellen Seite Text-Datei ersetzt. Format Befehl (:exec:) einfügen Im (:exec:) Befehl können Macros enthalten sein.Die Makros werden durch den entsprechenden Pfad ersetzt.:
<ul>
<li><b>%page%</b>. Die Makros werden durch den vollen Pfad der Seitendatei ersetzt.</li>
<li><b>%html%</b>.Die Makros werden durch den vollen Pfad der HTML-Datei ersetzt.</li>
<li><b>%folder%</b>. Die Makros werden durch den vollen Pfad des Seitenordners ersetzt.</li>
<li><b>%attach%</b>. Die Makros werden durch den vollen Pfad des Anhängeordners ersetzt one Slash am Schluss.</li>
</ul> Link Öffne Datei mit... Öffne Ergebnis HTML-Datei mit... Angehängte Datei öffnen mit application.exe:
<code><pre>(:exec:) 
application.exe Attach:my_file.txt
 (:execend:)</pre></code> Dialogfeld "Datei öffnen"... Werkzeug entfernen Starte eine menge Applikationen:
<code><pre>(:exec title="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Anwendung von ExternalTools Plugin laufen lassen? 
Es kann gefährlich sein. Anwendungen ausführen (:exec:) Anwendungen von ExternalTools Plugin laufen lassen? 
Es kann gefährlich sein. Macht das gleiche jedoch einen Knopf
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> Der (:exec:) Befehl hat folgende Parameter als Option.:
<ul>
<li><b>Format</b>. Wenn der Parameter "button" ist, wird ein Knopf anstelle eines Links erzeugt.</li>
<li><b>title</b>. Der Parameter setzt den Text für den Link oder den Knopf.</li>
</ul> Titel Werkzeugliste Warnen bevor der Ausführung von Anwendungen durch den Befehl (:exec:) https://jenyay.net/Outwiker/ExternalToolsEn 