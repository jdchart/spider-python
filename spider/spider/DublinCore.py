import datetime
from .utils import *
from .MultiLangAttribute import *
from .Coverage import *
from .Format import *
from .Relation import *
from .InstructionalMethod import *

class Resource(object):
    """
    Represent a Dublin Core ressource.

    Create an object with all of the typical Dublin Core data fields.
    For more info:
    https://www.dublincore.org/specifications/dublin-core/usageguide/elements/

    Attributes
    ----------
    language : list
        a list of language codes.

    identifier : str
        a string indicating the path to the resource.

    title : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    subject : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    description : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    type : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    source : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    creator : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    publisher : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    contributor : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    rights : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    identifier : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    audience : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    provenance : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    rightsHolder : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    accrualMethod : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    accrualPeriodicity : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    accrualPolicy : str | dict
        a string giving the ressource's title, or a dict where each key is a language code
        and the value is the title.

    date : datetime.datetime
        a datetime.datetime indicating the creation of the element.

    relation : Relation()
        a Relation class object. Describes an edge.

    coverage : Coverage()
        a Coverage class object. Describes a dates and regions for the element.

    format : Format()
        a Format class object. Describes the media linked with the element.
        
    instructionalMethod : InstructionalMethod()
        an InstructionalMethod class object. Describes how to display the linked media.

    Methods
    ----------
    collectData() -> dict
        return a dict structure with the elements attributes and their values.

    setFromReadData(data: dict) -> None
        set the object's attributes from dict data.

    appendLanguage(toAppend: str | list) -> None
        add a new language or list of languages without removing old ones.
    """

    def __init__(self, **kwargs):
        # Private language attribute:
        self._language = []
        self._language = parseStrListToList(self._language, kwargs.get('language', ["en"]))
        
        # The identifier will be set to the path:
        self.identifier = kwargs.get("identifier", "")

        # Create private multi language attributes:
        self._multiLangAttributes = []
        self._title = MultiLangAttribute(self, "title", languages = self._language, value = kwargs.get("title", ""))
        self._subject = MultiLangAttribute(self, "subject", languages = self._language, value = kwargs.get("subject", ""))
        self._description = MultiLangAttribute(self, "description", languages = self._language, value = kwargs.get("description", ""))
        self._type = MultiLangAttribute(self, "type", languages = self._language, value = kwargs.get("type", ""))
        self._source = MultiLangAttribute(self, "source", languages = self._language, value = kwargs.get("source", ""))
        self._creator = MultiLangAttribute(self, "creator", languages = self._language, value = kwargs.get("creator", ""))
        self._publisher = MultiLangAttribute(self, "publisher", languages = self._language, value = kwargs.get("publisher", ""))
        self._contributor = MultiLangAttribute(self, "contributor", languages = self._language, value = kwargs.get("contributor", ""))
        self._rights = MultiLangAttribute(self, "rights", languages = self._language, value = kwargs.get("rights", ""))
        self._audience = MultiLangAttribute(self, "audience", languages = self._language, value = kwargs.get("audience", ""))
        self._provenance = MultiLangAttribute(self, "provenance", languages = self._language, value = kwargs.get("provenance", ""))
        self._rightsHolder = MultiLangAttribute(self, "rightsHolder", languages = self._language, value = kwargs.get("rightsHolder", ""))
        self._accrualMethod = MultiLangAttribute(self, "accrualMethod", languages = self._language, value = kwargs.get("accrualMethod", ""))
        self._accrualPeriodicity = MultiLangAttribute(self, "accrualPeriodicity", languages = self._language, value = kwargs.get("accrualPeriodicity", ""))
        self._accrualPolicy = MultiLangAttribute(self, "accrualPolicy", languages = self._language, value = kwargs.get("accrualPolicy", ""))

        # Date must be a datetime.datetime:
        self.date = kwargs.get('date', datetime.datetime.now())
        
        # Modified Dublin Core attributes:
        self.relation = Relation(**kwargs.get('relation', {}))
        self.coverage = Coverage(**kwargs.get('coverage', {}))
        self.format = Format(**kwargs.get('format', {}))
        self.instructionalMethod = InstructionalMethod(**kwargs.get('instructionalMethod', {}))

    def collectData(self) -> dict:
        """Return a dict structure with the elements attributes and their values."""
        return {
            "title" : self._title.get(),
            "subject" : self._subject.get(),
            "description" : self._description.get(),
            "type" : self._type.get(),
            "source" : self._source.get(),
            "relation" : self.relation.toString(),
            "coverage" : self.coverage.toString(),
            "creator" : self._creator.get(),
            "publisher" : self._publisher.get(),
            "contributor" : self._contributor.get(),
            "rights" : self._rights.get(),
            "date" : self.date.strftime("%m-%d-%Y:%H:%M:%S.%f"),
            "format" : self.format.toString(),
            "identifier" : self.identifier,
            "language" : self._language,
            "audience" : self._audience.get(),
            "provenance" : self._provenance.get(),
            "rightsHolder" : self._rightsHolder.get(),
            "instructionalMethod" : self.instructionalMethod.toString(),
            "accrualMethod" : self._accrualMethod.get(),
            "accrualPeriodicity" : self._accrualPeriodicity.get(),
            "accrualPolicy" : self._accrualPolicy.get()
        }

    def setFromReadData(self, data: dict) -> None:
        """Set the object's attributes from dict data."""
        
        self._language = data["language"]

        for item in data:
            if item == "coverage":
                setattr(self, item, Coverage(from_string = data[item]))
            elif item == "format":
                setattr(self, item, Format(from_string = data[item]))
            elif item == "relation":
                setattr(self, item, Relation(from_string = data[item]))
            elif item == "instructionalMethod":
                setattr(self, item, InstructionalMethod(from_string = data[item]))
            elif item == "date":
                setattr(self, item, datetime.datetime.strptime(data[item], "%m-%d-%Y:%H:%M:%S.%f")) 
            elif item in self._multiLangAttributes:
                setattr(self, "_" + item, MultiLangAttribute(self, item, languages = self._language, value = data[item]))
            else:
                setattr(self, item, data[item])

    def appendLanguage(self, toAppend: str | list) -> None:
        """Add a new language or list of languages without removing old ones"""

        if type(toAppend) == str:
            if toAppend not in self._language:
                self._language.append(toAppend)
        elif type(toAppend) == list:
            for lang in toAppend:
                if lang not in self._language:
                    self._language.append(lang)
        for item in self._multiLangAttributes:
            thisItem = getattr(self, "_" + item)
            thisItem.set(self._language, "languages")
        self._sanitizeTags()

    # The public language attribute:
    @property
    def language(self):
        return self._language
    @language.setter
    def language(self, value):
        self._language = parseStrListToList(self._language, value)
        for item in self._multiLangAttributes:
            thisItem = getattr(self, "_" + item)
            thisItem.set(self._language, "languages")
        self._sanitizeTags()

    # Public multi language attributes attributes:
    @property
    def title(self):
        return self._title.get()
    @title.setter
    def title(self, value):
        self._title.set(value)

    @property
    def subject(self):
        return self._subject.get()
    @subject.setter
    def subject(self, value):
        self._subject.set(value)

    @property
    def description(self):
        return self._description.get()
    @description.setter
    def description(self, value):
        self._description.set(value)

    @property
    def type(self):
        return self._type.get()
    @type.setter
    def type(self, value):
        self._type.set(value)

    @property
    def source(self):
        return self._source.get()
    @source.setter
    def source(self, value):
        self._source.set(value)

    @property
    def creator(self):
        return self._creator.get()
    @creator.setter
    def creator(self, value):
        self._creator.set(value)

    @property
    def publisher(self):
        return self._publisher.get()
    @publisher.setter
    def publisher(self, value):
        self._publisher.set(value)

    @property
    def contributor(self):
        return self._contributor.get()
    @contributor.setter
    def contributor(self, value):
        self._contributor.set(value)

    @property
    def rights(self):
        return self._rights.get()
    @rights.setter
    def rights(self, value):
        self._rights.set(value)

    @property
    def audience(self):
        return self._audience.get()
    @audience.setter
    def audience(self, value):
        self._audience.set(value)

    @property
    def provenance(self):
        return self._provenance.get()
    @provenance.setter
    def provenance(self, value):
        self._provenance.set(value)

    @property
    def rightsHolder(self):
        return self._rightsHolder.get()
    @rightsHolder.setter
    def rightsHolder(self, value):
        self._rightsHolder.set(value)

    @property
    def accrualMethod(self):
        return self._accrualMethod.get()
    @accrualMethod.setter
    def accrualMethod(self, value):
        self._accrualMethod.set(value)

    @property
    def accrualPeriodicity(self):
        return self._accrualPeriodicity.get()
    @accrualPeriodicity.setter
    def accrualPeriodicity(self, value):
        self._accrualPeriodicity.set(value)

    @property
    def accrualPolicy(self):
        return self._accrualPolicy.get()
    @accrualPolicy.setter
    def accrualPolicy(self, value):
        self._accrualPolicy.set(value)