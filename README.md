#### README.md # VersionizerErstellt einen versions.json und einen compile.json File.Es hält zum einen die Versionsnummer fest, zum anderen erstellt er eine Entwicklungshistorie.Der visionizer ist dafür geschrieben um ihn automatisch von der IDE bei jedem Compilieren aufzurufen.## version.jsonEin Json-File aus dem die Versionsnummer und die Buildnummer hervorgeht.Verionizer kann die Build-Nummer automatisch um eins incrementieren.Der Json-File hat folgendes Format:    {        "date": "04.07.2014 14:40:37",         "version": "0.0.1",         "build": "1"    }Folgende Inhalte sind in dem Json-File enthalten:- **date** Das Datum des Build. Es wird automatisch bei jedem build auf das aktuelle Datum gesetzt.- **version** Die Version der Software. Wird von Hand gesetzt.- **build** Die Build-Nr. Wird automatisch gesetzt und bei jedem Build um eins incrementiert.## compile.jsonEin Json-File aus dem die Entwicklungshistorie hervor geht.Der Json-File hat folgendes Format:    [        {            "zeit": 17,             "start": "04.07.2014 14:23:37",              "end": "04.07.2014 14:40:37"        },        {            "zeit": 0,             "start": "04.07.2014 15:29:20",             "end": "04.07.2014 15:29:27"        }    ]- **start** Das Datum/Zeit an dem der Eintrag erfolgt ist- **end** Das Datum/Zeit an dem der zweite eintrag erfolgt ist- **zeit** Die Differenz der o.g. Werte in Minuten.Der Ablauf der Einträge:*Aufruf 1*  Es wird ein Eintrag erzeugt bei dem ```start``` und ```end``` gleich sind. Sie werden auf das aktuelle Datum/Zeit gesetzt. ```zeit``` erhält den Wert 0*Aufruf n(a)*   Ein Aufruf der zeitlich innerhalb 30 Minuten nach dem Ersten/Letzten Aufruf stattfindet.Der Wert von ```end``` wird auf das Datum/Zeit des Aufrufes gesetzt.*Aufruf n(b)*   Ein Aufruf der zeitlich ausserhalb 30 Minuten nach dem Ersten/Letzten Aufruf stattfindet.Der Wert von ```end``` wird so belassen und der Wert von ```zeit``` wird berechnet und eingetragen.```zeit``` ist die differenz zwischen ```start``` und ```end``` und wird in Minuten angegeben.Weiterhin wird ein neuer Eintrag erzeugt. (siehe Aufruf 1)Somit ist nach mehreren Einträgen eine zeitliche achse erkennbar.