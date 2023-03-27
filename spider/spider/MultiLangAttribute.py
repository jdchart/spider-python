from .utils import *

class MultiLangAttribute:
    """
    An attribute that can have several languages.

    Designed to be work in a system where attributes can have several
    languages. Reccomended to use the get() method for retriving the
    value of the attribute (self.value returns a value list).

    Attributes
    ----------
    name : str
        the arrtibute name.

    languages : list
        a list of language code strings.
        
    value : str | dict
        a dict of values (one entry for each language code).
        
    Methods
    ----------
    get(lang: str | None) -> str | dict
        get the value, supply a language (if no language is supplied,
        the method returns every value in dict form).

    set(value: str | dict | list, setType: str = "value") -> None
        set the "value" (by default) or "languages" of the attribute.
    """

    def __init__(self, parent, name: str, **kwargs):
        # Name the attribute and collect it's parent:
        self.name = name
        self._parent = parent

        # The two main attributes, languages and value
        # (set as pivate here, see properties below)
        self._languages = []
        self._value = {}
        self._languages = self._parseLanguageValue(kwargs.get("languages", ["en"]))
        self._value = self._parseValueValue(kwargs.get("value", {"en" : ""}))

        # Compare languages and value and make them match.
        self._sanitizeAttributes()

        # Append this attribute's name to the parent's multiLangAttributes list:
        if hasattr(parent, "_multiLangAttributes"):
            if self.name not in parent._multiLangAttributes:
                parent._multiLangAttributes.append(self.name)
    
    # The public language and value properties.
    @property
    def languages(self) -> list:
        return self._languages
    @languages.setter
    def languages(self, value: str | list):
        self._languages = self._parseLanguageValue(value)
        self._sanitizeAttributes()
        self._updateParentLanguage()

    @property
    def value(self) -> dict:
        return self._value
    @value.setter
    def value(self, value: str | list):
        self._value = self._parseValueValue(value)
        self._sanitizeAttributes()

    def get(self, lang: str | None = None) -> str | dict:
        """Get the value of the attribute."""

        if lang == None:
            return self._value
        else:
            if lang in self._value.keys():
                return self._value[lang]
            else:
                raise Exception("\"" + lang + "\" was not a valid language in " + str(self._languages))
            
    def set(self, value: str | dict | list, setType: str = "value") -> None:
        """Set the value (by default) or languages of the attribute."""

        if setType == 'value':
            if type(value) == list:
                raise Exception("Value must be str or dict when value language.")
            self._sanitizeAttributes()
            self._value = self._parseValueValue(value)
        elif setType == "languages":
            if type(value) == dict:
                raise Exception("Value must be str or list when setting langiage.")
            self._languages = self._parseLanguageValue(value)
            self._sanitizeAttributes()
            self._updateParentLanguage()
        else:
            raise Exception("Can only set \"value\" or \"languages\".")

    def _parseLanguageValue(self, toParse: str | list) -> list:
        """Parse an input value to language list."""

        toReturn = parseStrListToList(self._languages, toParse)
        return toReturn
    
    def _parseValueValue(self, toParse: str | dict) -> dict:
        """Parse an input value to value dict."""

        toReturn = self._value
        if type(toParse) == str:
            toReturn[self._languages[0]] = toParse
        else:
            for item in toParse:
                toReturn[item] = toParse[item]
                if item not in self._languages:
                    self._languages.append(item)

        return toReturn
    
    def _sanitizeAttributes(self) -> None:
        """Update language list and value dict."""

        if len(self._languages) < len(self._value.keys()):
            for lang in self._value:
                if lang not in self._languages:
                    self._languages.append(lang)
        
        if len(self._value.keys()) < len(self._languages):
            for lang in self._languages:
                if lang not in self._value.keys():
                    self._value[lang] = ""

    def _updateParentLanguage(self) -> None:
        """Trigger updating of the parent's language attribute"""
        if "language" in list(self._parent.__dict__.keys()):
            self._parent.language = self._languages