import datetime
from .utils import *
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
    title : str
        a string giving the ressource's title.
    subject : str
        a string giving the ressource's subject.
    description : str
        a string giving the ressource's description.
    type : str
        a string giving the ressource's type.
    source : str
        a string giving the ressource's source.
    creator : str
        a string giving the ressource's creator.
    publisher : str
        a string giving the ressource's publisher.
    contributor : str
        a string giving the ressource's contributor.
    rights : str
        a string giving the ressource's rights.
    identifier : str
        a string giving the ressource's identifier.
    audience : str
        a string giving the ressource's audience.
    provenance : str
        a string giving the ressource's provenance.
    rightsHolder : str
        a string giving the ressource's rightsHolder.
    accrualMethod : str
        a string giving the ressource's accrualMethod.
    accrualPeriodicity : str
        a string giving the ressource's accrualPeriodicity.
    accrualPolicy : str
        a string giving the ressource's accrualPolicy.
    """

    def __init__(self, **kwargs):
        self.language = kwargs.get('language', "en")

        self._title = kwargs.get('title', "")
        self._subject = kwargs.get('subject', "")
        self._description = kwargs.get('description', "")
        self._type = kwargs.get('type', "")
        self._source = kwargs.get('source', "")
        self._creator = kwargs.get('creator', "")
        self._publisher = kwargs.get('publisher', "")
        self._contributor = kwargs.get('contributor', "")
        self._rights = kwargs.get('rights', "")
        self._identifier = kwargs.get('identifier', "")
        self._audience = kwargs.get('audience', "")
        self._provenance = kwargs.get('provenance', "")
        self._rightsHolder = kwargs.get('rightsHolder', "")
        self._accrualMethod = kwargs.get('accrualMethod', "")
        self._accrualPeriodicity = kwargs.get('accrualPeriodicity', "")
        self._accrualPolicy = kwargs.get('accrualPolicy', "")

        self.relation = Relation(**kwargs.get('relation', {}))
        self.coverage = Coverage(**kwargs.get('coverage', {}))
        self.date = kwargs.get('date', datetime.datetime.now())
        self.format = Format(**kwargs.get('format', {}))
        self.instructionalMethod = InstructionalMethod(**kwargs.get('instructionalMethod', {}))

        self.specials = [
            "title", "subject", "description", "type", "source", "creator", "publisher",
            "contributor", "rights", "identifier", "audience", "provenance", "rightsHolder",
            "accrualMethod", "accrualPeriodicity", "accrualPolicy"
        ]

    def getFromLang(self, attr, lang):
        if attr in self.specials:
            return self.parseFromLang(getattr(self, "_" + attr), lang)

    def parseFromLang(self, prop, givenLang = None):
        if isinstance(prop, str) or isinstance(prop, list) or givenLang == "full":
            return prop
        else:
            langKey = list(prop.keys())[0]
            if givenLang != None:
                if givenLang in list(prop.keys()):
                    langKey = givenLang
            return prop[langKey]

    def collectData(self):
        return {
            "title" : self._title,
            "subject" : self._subject,
            "description" : self._description,
            "type" : self._type,
            "source" : self._source,
            "relation" : self.relation.toString(),
            "coverage" : self.coverage.toString(),
            "creator" : self._creator,
            "publisher" : self._publisher,
            "contributor" : self._contributor,
            "rights" : self._rights,
            "date" : self.date.strftime("%m-%d-%Y:%H:%M:%S.%f"),
            "format" : self.format.toString(),
            "identifier" : self._identifier,
            "language" : self.language,
            "audience" : self._audience,
            "provenance" : self._provenance,
            "rightsHolder" : self._rightsHolder,
            "instructionalMethod" : self.instructionalMethod.toString(),
            "accrualMethod" : self._accrualMethod,
            "accrualPeriodicity" : self._accrualPeriodicity,
            "accrualPolicy" : self._accrualPolicy
        }

    def setFromReadData(self, data):
        for item in data:
            if item == "coverage":
                setattr(self, item, Coverage(from_string = data[item]))
            if item == "format":
                setattr(self, item, Format(from_string = data[item]))
            if item == "relation":
                setattr(self, item, Relation(from_string = data[item]))
            if item == "instructionalMethod":
                setattr(self, item, InstructionalMethod(from_string = data[item]))
            if item == "date":
                setattr(self, item, datetime.datetime.strptime(data[item], "%m-%d-%Y:%H:%M:%S.%f"))
            if item in self.specials:
                setattr(self, "_" + item, data[item])

    @property
    def title(self):
        return self.parseFromLang(self._title)
    @title.setter
    def title(self, content):
        self._title = content

    @property
    def subject(self):
        return self.parseFromLang(self._subject)
    @subject.setter
    def subject(self, content):
        self._subject = content

    @property
    def description(self):
        return self.parseFromLang(self._description)
    @description.setter
    def description(self, content):
        self._description = content

    @property
    def type(self):
        return self.parseFromLang(self._type)
    @type.setter
    def type(self, content):
        self._type = content

    @property
    def source(self):
        return self.parseFromLang(self._source)
    @source.setter
    def source(self, content):
        self._source = content

    @property
    def creator(self):
        return self.parseFromLang(self._creator)
    @creator.setter
    def creator(self, content):
        self._creator = content

    @property
    def publisher(self):
        return self.parseFromLang(self._publisher)
    @publisher.setter
    def publisher(self, content):
        self._publisher = content

    @property
    def contributor(self):
        return self.parseFromLang(self._contributor)
    @contributor.setter
    def contributor(self, content):
        self._contributor = content

    @property
    def rights(self):
        return self.parseFromLang(self._rights)
    @rights.setter
    def rights(self, content):
        self._rights = content

    @property
    def identifier(self):
        return self.parseFromLang(self._identifier)
    @identifier.setter
    def identifier(self, content):
        self._identifier = content

    @property
    def audience(self):
        return self.parseFromLang(self._audience)
    @audience.setter
    def audience(self, content):
        self._audience = content

    @property
    def provenance(self):
        return self.parseFromLang(self._provenance)
    @provenance.setter
    def provenance(self, content):
        self._provenance = content

    @property
    def rightsHolder(self):
        return self.parseFromLang(self._rightsHolder)
    @rightsHolder.setter
    def rightsHolder(self, content):
        self._rightsHolder = content

    @property
    def accrualMethod(self):
        return self.parseFromLang(self._accrualMethod)
    @accrualMethod.setter
    def accrualMethod(self, content):
        self._accrualMethod = content

    @property
    def accrualPeriodicity(self):
        return self.parseFromLang(self._accrualPeriodicity)
    @accrualPeriodicity.setter
    def accrualPeriodicity(self, content):
        self._accrualPeriodicity = content

    @property
    def accrualPolicy(self):
        return self.parseFromLang(self._accrualPolicy)
    @accrualPolicy.setter
    def accrualPolicy(self, content):
        self._accrualPolicy = content