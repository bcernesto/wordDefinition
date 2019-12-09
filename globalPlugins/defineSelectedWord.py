import urllib
import json
import globalPluginHandler
import scriptHandler
import api
import textInfos
from ui import message, browseableMessage
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def define(self, word, lang='es'):
        link='https://googledictionaryapi.eu-gb.mybluemix.net/?define='+word+'&lang='+lang
        output=''
        f = urllib.urlopen(link)
        myfile = f.read().decode("utf-8")
        jsonDict=json.loads(myfile)
        meaning=jsonDict[0]['meaning']
        for k, v in meaning.items():
            if k!=u'':
                output+=k
            for d in v['definitions']:
                if d['definition']!=u'':
                    output+='\n'+d['definition']
        return output

    def script_defineSelectedWord(self,gesture):
        obj = api.getFocusObject()
        treeInterceptor = obj.treeInterceptor
        if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
            obj = treeInterceptor
        try:
            info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
        except (RuntimeError, NotImplementedError):
            info = None
        if not info or info.isCollapsed:
            # TRANSLATORS: Error message when there aren't any selected word
            message(_("Please select some word first."))
        else:
            browseableMessage(self.define(info.text.encode("utf-8")))

    # TRANSLATORS: Script __doc__
    script_defineSelectedWord.__doc__ = _("Defines selected word.")

    # TRANSLATORS: Script category
    script_defineSelectedWord.category = _("Text editing")

    __gestures = {
        "kb:control+shift+f11": "defineSelectedWord",
    }
