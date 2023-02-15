# Metadata fields

Every element in spider (webs, nodes and edges) has a certain amount of metadata that is based on [Dublin Core](https://www.dublincore.org/). The fields don't have to be filled-in, but it is recommended to provide a maximum of information for each field.

1. [Golbal Dublin Core](#global-dublin-core)
    - [Title](#title)
    - [Subject](#subject)
    - [Description](#description)
    - [Type](#type)
    - [Source](#source)
    - [Relation](#relation)
    - [Coverage](#coverage)
    - [Creator](#creator)
    - [Publisher](#publisher)
    - [Contributor](#contributor)
    - [Rights](#rights)
    - [Date](#date)
    - [Format](#format)
    - [Identifier](#identifier)
    - [Language](#language)
    - [Audience](#audience)
    - [Provenance](#provenance)
    - [Rights Holder](#rights-holder)
    - [Instructional Method](#instructional-method)
    - [Accrual Method](#accural-method)
    - [Accrual Periodicity](#accrual-periodicity)
    - [Accrual Policy](#accrual-policy)

## Global Dublin Core

These are the fields dervied from Dublin Core that apply to **ALL** elements:

### Title
- attribute: `title`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#title) description: The name given to the resource. Typically, a Title will be a name by which the resource is formally known.

### Subject
- attribute: `subject`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#subject) description: The topic of the content of the resource. Typically, a Subject will be expressed as keywords or key phrases or classification codes that describe the topic of the resource. Recommended best practice is to select a value from a controlled vocabulary or formal classification scheme.

### Description
- attribute: `description`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#description) description: An account of the content of the resource. Description may include but is not limited to: an abstract, table of contents, reference to a graphical representation of content or a free-text account of the content.

### Type
- attribute: `type`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#type) description: The nature or genre of the content of the resource. Type includes terms describing general categories, functions, genres, or aggregation levels for content. Recommended best practice is to select a value from a controlled vocabulary (for example, the [DCMIType vocabulary](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)). To describe the physical or digital manifestation of the resource, use the FORMAT element.

### Source
- attribute: `source`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#source) description: A Reference to a resource from which the present resource is derived. The present resource may be derived from the Source resource in whole or part. Recommended best practice is to reference the resource by means of a string or number conforming to a formal identification system.

### Relation
- attribute: `relation`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#relation) description: A reference to a related resource. Recommended best practice is to reference the resource by means of a string or number conforming to a formal identification system.

### Coverage
- attribute: `coverage`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#coverage) description: The extent or scope of the content of the resource. Coverage will typically include spatial location (a place name or geographic co-ordinates), temporal period (a period label, date, or date range) or jurisdiction (such as a named administrative entity). Recommended best practice is to select a value from a controlled vocabulary (for example, the Thesaurus of Geographic Names [Getty Thesaurus of Geographic Names, [http://www.getty.edu/research/tools/vocabulary/tgn/](https://www.getty.edu/research/tools/vocabularies/tgn/)). Where appropriate, named places or time periods should be used in preference to numeric identifiers such as sets of co-ordinates or date ranges.

### Creator
- attribute: `creator`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#creator) description: An entity primarily responsible for making the content of the resource. Examples of a Creator include a person, an organization, or a service. Typically the name of the Creator should be used to indicate the entity.

### Publisher
- attribute: `publisher`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#publisher) description: The entity responsible for making the resource available. Examples of a Publisher include a person, an organization, or a service. Typically, the name of a Publisher should be used to indicate the entity.

### Contributor
- attribute: `contributor`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#contributor) description: An entity responsible for making contributions to the content of the resource. Examples of a Contributor include a person, an organization or a service. Typically, the name of a Contributor should be used to indicate the entity.

### Rights
- attribute: `rights`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#rights) description: Information about rights held in and over the resource. Typically a Rights element will contain a rights management statement for the resource, or reference a service providing such information. Rights information often encompasses Intellectual Property Rights (IPR), Copyright, and various Property Rights. If the rights element is absent, no assumptions can be made about the status of these and other rights with respect to the resource.

### Date
- attribute: `date`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#date) description: A date associated with an event in the life cycle of the resource. Typically, Date will be associated with the creation or availability of the resource. Recommended best practice for encoding the date value is defined in a profile of ISO 8601 [Date and Time Formats, W3C Note, [http://www.w3.org/TR/NOTE-datetime](https://www.w3.org/TR/NOTE-datetime) and follows the YYYY-MM-DD format.

### Format
- attribute: `format`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#format) description: The physical or digital manifestation of the resource. Typically, Format may include the media-type or dimensions of the resource. Examples of dimensions include size and duration. Format may be used to determine the software, hardware or other equipment needed to display or operate the resource. Recommended best practice is to select a value from a controlled vocabulary (for example, the list of Internet Media Types [http://www.iana.org/assignments/media-types/](https://www.iana.org/assignments/media-types/media-types.xhtmldefining computer media formats).

### Identifier
- attribute: `identifier`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#identifier) description: An unambiguous reference to the resource within a given context. Recommended best practice is to identify the resource by means of a string or number conforming to a formal identification system. Examples of formal identification systems include the Uniform Resource Identifier (URI) (including the Uniform Resource Locator (URL), the Digital Object Identifier (DOI) and the International Standard Book Number (ISBN).

### Language
- attribute: `language`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#language) description: A language of the intellectual content of the resource. Recommended best practice for the values of the Language element is defined by RFC 3066 [RFC 3066, [http://www.ietf.org/rfc/rfc3066.txt](https://www.ietf.org/rfc/rfc3066.txt) which, in conjunction with ISO 639 [ISO 639, [http://www.oasis-open.org/cover/iso639a.html](http://xml.coverpages.org/iso639a.html)), defines two- and three-letter primary language tags with optional subtags. Examples include "en" or "eng" for English, "akk" for Akkadian, and "en-GB" for English used in the United Kingdom.

### Audience
- attribute: `audience`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#audience) description: A class of entity for whom the resource is intended or useful. A class of entity may be determined by the creator or the publisher or by a third party.

### Provenance
- attribute: `provenance`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#provenance) description: A statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity and interpretation. The statement may include a description of any changes successive custodians made to the resource.

### Rights Holder
- attribute: `rightsHolder`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#rightsholder) description: A person or organization owning or managing rights over the resource. Recommended best practice is to use the URI or name of the Rights Holder to indicate the entity.

### Instructional Method
- attribute: `instructionalMethod`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#instructionalmethod) description: A process, used to engender knowledge, attitudes and skills, that the resource is designed to support. Instructional Method will typically include ways of presenting instructional materials or conducting instructional activities, patterns of learner-to-learner and learner-to-instructor interactions, and mechanisms by which group and individual levels of learning are measured. Instructional methods include all aspects of the instruction and learning processes from planning and implementation through evaluation and feedback.

### Accural Method
- attribute: `accrualMethod`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#accrualmethod) description: The method by which items are added to a collection. Recommended best practice is to use a value from a controlled vocabulary.

### Accrual Periodicity
- attribute: `accrualPeriodicity`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#accrualperiodicity) description: The frequency with which items are added to a collection. Recommended best practice is to use a value from a controlled vocabulary.

### Accrual Policy
- attribute: `accrualPolicy`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#accrualpolicy) description: The policy governing the addition of items to a collection. Recommended best practice is to use a value from a controlled vocabulary.