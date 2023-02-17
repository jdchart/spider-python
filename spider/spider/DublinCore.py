'''
For more info, consult:
https://www.dublincore.org/specifications/dublin-core/usageguide/elements/
'''

import datetime
from .utils import *
from .Coverage import *
from .Format import *
from .Relation import *
from .InstructionalMethod import *

class Resource:
    def __init__(self, **kwargs):
        '''
        1. TITLE
        The name given to the resource.
        Typically, a Title will be a name by which the resource is formally known.
        '''
        self.title = kwargs.get('title', "")

        '''
        2. SUBJECT
        The topic of the content of the resource.
        Typically, a Subject will be expressed as keywords or key phrases or classification codes that describe the topic of the resource.
        Recommended best practice is to select a value from a controlled vocabulary or formal classification scheme.
        '''
        self.subject = kwargs.get('subject', "")

        '''
        3. DESCRIPTION
        An account of the content of the resource.
        Description may include but is not limited to: an abstract, table of contents, reference to a graphical representation of content or a free-text account of the content.
        '''
        self.description = kwargs.get('description', "")

        '''
        4. TYPE
        The nature or genre of the content of the resource.
        Type includes terms describing general categories, functions, genres, or aggregation levels for content.
        Recommended best practice is to select a value from a controlled vocabulary (for example, the DCMIType vocabulary ).
        To describe the physical or digital manifestation of the resource, use the FORMAT element.
        '''
        self.type = kwargs.get('type', "")

        '''
        5. SOURCE
        A Reference to a resource from which the present resource is derived.
        The present resource may be derived from the Source resource in whole or part.
        Recommended best practice is to reference the resource by means of a string or number conforming to a formal identification system.
        '''
        self.source = kwargs.get('source', "")

        '''
        6. RELATION
        A reference to a related resource.
        Recommended best practice is to reference the resource by means of a string or number conforming to a formal identification system.
        '''
        self.relation = Relation(**kwargs.get('relation', {}))

        '''
        7. COVERAGE
        The extent or scope of the content of the resource.
        Coverage will typically include spatial location (a place name or geographic co-ordinates), temporal period (a period label, date, or date range) or jurisdiction (such as a named administrative entity).
        Recommended best practice is to select a value from a controlled vocabulary (for example, the Thesaurus of Geographic Names [Getty Thesaurus of Geographic Names, http://www. getty.edu/research/tools/vocabulary/tgn/]).
        Where appropriate, named places or time periods should be used in preference to numeric identifiers such as sets of co-ordinates or date ranges.
        '''
        self.coverage = Coverage(**kwargs.get('coverage', {}))

        '''
        8. CREATOR
        An entity primarily responsible for making the content of the resource.
        Examples of a Creator include a person, an organization, or a service.
        Typically the name of the Creator should be used to indicate the entity.
        '''
        self.creator = kwargs.get('creator', "")

        '''
        9. PUBLISHER
        The entity responsible for making the resource available.
        Examples of a Publisher include a person, an organization, or a service.
        Typically, the name of a Publisher should be used to indicate the entity.
        '''
        self.publisher = kwargs.get('publisher', "")

        '''
        10. CONTRIBUTOR
        An entity responsible for making contributions to the content of the resource.
        Examples of a Contributor include a person, an organization or a service.
        Typically, the name of a Contributor should be used to indicate the entity.
        '''
        self.contributor = kwargs.get('contributor', "")

        '''
        11. RIGHTS
        Information about rights held in and over the resource.
        Typically a Rights element will contain a rights management statement for the resource, or reference a service providing such information.
        Rights information often encompasses Intellectual Property Rights (IPR), Copyright, and various Property Rights.
        If the rights element is absent, no assumptions can be made about the status of these and other rights with respect to the resource.
        '''
        self.rights = kwargs.get('rights', "")

        '''
        12. DATE
        A date associated with an event in the life cycle of the resource.
        Typically, Date will be associated with the creation or availability of the resource.
        Recommended best practice for encoding the date value is defined in a profile of ISO 8601 [Date and Time Formats, W3C Note, http://www.w3.org/TR/NOTE- datetime] and follows the YYYY-MM-DD format.
        '''
        self.date = kwargs.get('date', datetime.datetime.now())

        '''
        13. FORMAT
        The physical or digital manifestation of the resource.
        Typically, Format may include the media-type or dimensions of the resource.
        Examples of dimensions include size and duration.
        Format may be used to determine the software, hardware or other equipment needed to display or operate the resource.
        Recommended best practice is to select a value from a controlled vocabulary (for example, the list of Internet Media Types [http://www.iana.org/ assignments/media-types/] defining computer media formats).
        '''
        self.format = Format(**kwargs.get('format', {}))

        '''
        14. IDENTIFIER
        An unambiguous reference to the resource within a given context.
        Recommended best practice is to identify the resource by means of a string or number conforming to a formal identification system.
        Examples of formal identification systems include the Uniform Resource Identifier (URI) (including the Uniform Resource Locator (URL), the Digital Object Identifier (DOI) and the International Standard Book Number (ISBN).
        '''
        self.identifier = kwargs.get('identifier', "")

        '''
        15. LANGUAGE
        A language of the intellectual content of the resource.
        Recommended best practice for the values of the Language element is defined by RFC 3066 [RFC 3066, http://www.ietf.org/rfc/ rfc3066.txt] which, in conjunction with ISO 639 [ISO 639, http://www.oasis- open.org/cover/iso639a.html]), defines two- and three-letter primary language tags with optional subtags.
        Examples include "en" or "eng" for English, "akk" for Akkadian, and "en-GB" for English used in the United Kingdom.
        '''
        self.language = kwargs.get('language', "en")

        '''
        16. AUDIENCE
        A class of entity for whom the resource is intended or useful.
        A class of entity may be determined by the creator or the publisher or by a third party.
        '''
        self.audience = kwargs.get('audience', "")

        '''
        17. PROVENANCE
        A statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity and interpretation.
        The statement may include a description of any changes successive custodians made to the resource.
        '''
        self.provenance = kwargs.get('provenance', "")

        '''
        18. RIGHTS HOLDER
        A person or organization owning or managing rights over the resource.
        Recommended best practice is to use the URI or name of the Rights Holder to indicate the entity.
        '''
        self.rightsHolder = kwargs.get('rightsHolder', "")

        '''
        19. INSTRUCTIONAL METHOD
        A process, used to engender knowledge, attitudes and skills, that the resource is designed to support.
        Instructional Method will typically include ways of presenting instructional materials or conducting instructional activities, patterns of learner-to-learner and learner-to-instructor interactions, and mechanisms by which group and individual levels of learning are measured.
        Instructional methods include all aspects of the instruction and learning processes from planning and implementation through evaluation and feedback.
        '''
        self.instructionalMethod = InstructionalMethod(**kwargs.get('instructionalMethod', {}))

        '''
        20. ACCURAL METHOD
        The method by which items are added to a collection.
        Recommended best practice is to use a value from a controlled vocabulary.
        '''
        self.accrualMethod = kwargs.get('accrualMethod', "")

        '''
        21. ACCURAL PERIODICITY
        The frequency with which items are added to a collection.
        Recommended best practice is to use a value from a controlled vocabulary.
        '''
        self.accrualPeriodicity = kwargs.get('accrualPeriodicity', "")

        '''
        22. ACCURAL POLICY
        The policy governing the addition of items to a collection.
        Recommended best practice is to use a value from a controlled vocabulary.
        '''
        self.accrualPolicy = kwargs.get('accrualPolicy', "")

    def collectData(self):
        return {
            "title" : self.title,
            "subject" : self.subject,
            "description" : self.description,
            "type" : self.type,
            "source" : self.source,
            "relation" : self.relation.toString(),
            "coverage" : self.coverage.toString(),
            "creator" : self.creator,
            "publisher" : self.publisher,
            "contributor" : self.contributor,
            "rights" : self.rights,
            "date" : self.date.strftime("%m-%d-%Y:%H:%M:%S.%f"),
            "format" : self.format.toString(),
            "identifier" : self.identifier,
            "language" : self.language,
            "audience" : self.audience,
            "provenance" : self.provenance,
            "rightsHolder" : self.rightsHolder,
            "instructionalMethod" : self.instructionalMethod.toString(),
            "accrualMethod" : self.accrualMethod,
            "accrualPeriodicity" : self.accrualPeriodicity,
            "accrualPolicy" : self.accrualPolicy
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