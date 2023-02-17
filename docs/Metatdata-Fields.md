# Metadata fields

Every element in spider (webs, nodes and edges) has a certain amount of metadata that is based on [Dublin Core](https://www.dublincore.org/). The fields don't have to be filled-in, but it is recommended to provide a maximum of information for each field.

Some fields are [Pure Dublin Core](#pure-dublin-core), and can be filled in as the user sees fit.

Others are [Modified Dublin Core](#modified-dublin-core). This means that they have extra fields for allowing the elements to fit into a network structure or to be decoded by viewer software. The information is stored as a string with a W3C inspired structure (`&fieldName=content`).

There are a few [Other Fields](#other-fields) that have been added for internal spider usage.

1. [Pure Dublin Core](#pure-dublin-core)
    - [Title](#title)
    - [Subject](#subject)
    - [Description](#description)
    - [Date](#date)
    - [Type](#type)
    - [Source](#source)
    - [Creator](#creator)
    - [Publisher](#publisher)
    - [Contributor](#contributor)
    - [Rights](#rights)
    - [Language](#language)
    - [Audience](#audience)
    - [Provenance](#provenance)
    - [Rights Holder](#rights-holder)
    - [Accrual Method](#accural-method)
    - [Accrual Periodicity](#accrual-periodicity)
    - [Accrual Policy](#accrual-policy)
2. [Modified Dublin Core](#modified-dublin-core)
    - [Relation](#relation)
    - [Coverage](#coverage)
    - [Format](#format)
    - [Identifier](#identifier)
    - [Instructional Method](#instructional-method)
3. [Other Fields](#other-fields)
    - [Tags](#tags)
    - [UUID](#uuid)
    - [Path](#path)

## Pure Dublin Core

### Title
- attribute: `title`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#title) description: The name given to the resource. Typically, a Title will be a name by which the resource is formally known.
- Default: `""`

### Subject
- attribute: `subject`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#subject) description: The topic of the content of the resource. Typically, a Subject will be expressed as keywords or key phrases or classification codes that describe the topic of the resource. Recommended best practice is to select a value from a controlled vocabulary or formal classification scheme.
- Default: `""`

### Description
- attribute: `description`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#description) description: An account of the content of the resource. Description may include but is not limited to: an abstract, table of contents, reference to a graphical representation of content or a free-text account of the content.
- Default: `""`

### Date
- attribute: `date`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#date) description: A date associated with an event in the life cycle of the resource. Typically, Date will be associated with the creation or availability of the resource. Recommended best practice for encoding the date value is defined in a profile of ISO 8601 [Date and Time Formats, W3C Note, [http://www.w3.org/TR/NOTE-datetime](https://www.w3.org/TR/NOTE-datetime) and follows the YYYY-MM-DD format.
- Default: `datetime.datetime.now()`

### Type
- attribute: `type`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#type) description: The nature or genre of the content of the resource. Type includes terms describing general categories, functions, genres, or aggregation levels for content. Recommended best practice is to select a value from a controlled vocabulary (for example, the [DCMIType vocabulary](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)). To describe the physical or digital manifestation of the resource, use the FORMAT element.
- Default: `""`

### Source
- attribute: `source`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#source) description: A Reference to a resource from which the present resource is derived. The present resource may be derived from the Source resource in whole or part. Recommended best practice is to reference the resource by means of a string or number conforming to a formal identification system.
- Default: `""`

### Creator
- attribute: `creator`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#creator) description: An entity primarily responsible for making the content of the resource. Examples of a Creator include a person, an organization, or a service. Typically the name of the Creator should be used to indicate the entity.
- Default: `""`

### Publisher
- attribute: `publisher`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#publisher) description: The entity responsible for making the resource available. Examples of a Publisher include a person, an organization, or a service. Typically, the name of a Publisher should be used to indicate the entity.
- Default: `""`

### Contributor
- attribute: `contributor`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#contributor) description: An entity responsible for making contributions to the content of the resource. Examples of a Contributor include a person, an organization or a service. Typically, the name of a Contributor should be used to indicate the entity.
- Default: `""`

### Rights
- attribute: `rights`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#rights) description: Information about rights held in and over the resource. Typically a Rights element will contain a rights management statement for the resource, or reference a service providing such information. Rights information often encompasses Intellectual Property Rights (IPR), Copyright, and various Property Rights. If the rights element is absent, no assumptions can be made about the status of these and other rights with respect to the resource.
- Default: `""`

### Language
- attribute: `language`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#language) description: A language of the intellectual content of the resource. Recommended best practice for the values of the Language element is defined by RFC 3066 [RFC 3066, [http://www.ietf.org/rfc/rfc3066.txt](https://www.ietf.org/rfc/rfc3066.txt) which, in conjunction with ISO 639 [ISO 639, [http://www.oasis-open.org/cover/iso639a.html](http://xml.coverpages.org/iso639a.html)), defines two- and three-letter primary language tags with optional subtags. Examples include "en" or "eng" for English, "akk" for Akkadian, and "en-GB" for English used in the United Kingdom.
- Recommended to use the format "en", "fr" etc. for Mirador parsing.
- Default: `"en"`

### Audience
- attribute: `audience`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#audience) description: A class of entity for whom the resource is intended or useful. A class of entity may be determined by the creator or the publisher or by a third party.
- Default: `""`

### Provenance
- attribute: `provenance`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#provenance) description: A statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity and interpretation. The statement may include a description of any changes successive custodians made to the resource.
- Default: `""`

### Rights Holder
- attribute: `rightsHolder`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#rightsholder) description: A person or organization owning or managing rights over the resource. Recommended best practice is to use the URI or name of the Rights Holder to indicate the entity.
- Default: `""`

### Accural Method
- attribute: `accrualMethod`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#accrualmethod) description: The method by which items are added to a collection. Recommended best practice is to use a value from a controlled vocabulary.
- Default: `""`

### Accrual Periodicity
- attribute: `accrualPeriodicity`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#accrualperiodicity) description: The frequency with which items are added to a collection. Recommended best practice is to use a value from a controlled vocabulary.
- Default: `""`

### Accrual Policy
- attribute: `accrualPolicy`
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#accrualpolicy) description: The policy governing the addition of items to a collection. Recommended best practice is to use a value from a controlled vocabulary.
- Default: `""`

## Modified Dublin Core

### Relation
- attribute: `relation`
- The Dublin Core `relation` field looks to represent a reference to a related resource. This is where spider puts information pertaining to an edge between two elements. Note that the edge is itself an element and can be described in the same way as anything else. Spider will parse data into a single relation entry which can be easily decoded.
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#relation) description: A reference to a related resource. Recommended best practice is to reference the resource by means of a string or number conforming to a formal identification system.
#### Attributes:
- `source` : UUID string corresponding to a node.
- `target` : UUID string corresponding to a node.
- `sourceRegions` : a list of the following objects:
```python
{
    "start" : -1, # The start time in the source node for the edge in ms (-1 = beginning).
    "end" : 1000, # The end time in the source node for the edge in ms (-1 = the end).
    "dims" : [-1] # The coordinates the edge occupies for the source ([-1] = the whole of the ressource, or [x, y, w, h])
}
```
- `targetRegions` : a list of the same objects.

### Coverage
- attribute: `coverage`
- The Dublin Core `coverage` field looks to represent the extent or scope of the content of the resource. Notably: time period and geographic location. Spider will parse data into a single coverage entry which can be easily decoded.
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#coverage) description: The extent or scope of the content of the resource. Coverage will typically include spatial location (a place name or geographic co-ordinates), temporal period (a period label, date, or date range) or jurisdiction (such as a named administrative entity). Recommended best practice is to select a value from a controlled vocabulary (for example, the Thesaurus of Geographic Names [Getty Thesaurus of Geographic Names, [http://www.getty.edu/research/tools/vocabulary/tgn/](https://www.getty.edu/research/tools/vocabularies/tgn/)). Where appropriate, named places or time periods should be used in preference to numeric identifiers such as sets of co-ordinates or date ranges.
#### Attributes:
- `startDateTime`: a `datetime.datetime` object representing the creation of the object.
- `endDateTime`: a `datetime.datetime` object representing the desctruction or the end of the object.
- `modificationDateTimes` : a list of the following objects:
```python
{
    "datetime" : datetime.datetime.now(),
    "title" : "Modif 1",
    "description" : "My modification 1"
}
```
- `region` : a string indicating the region the object covers.

### Format
- attribute: `format`
- The Dublin Core `format` field looks to represent the physical or digital manifestation of the resource. Notably: media-type, dimensions, size, duration etc. Spider will parse data into a single format entry which can be easily decoded. You can set the format for any element, but it only really applies to nodes.
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#format) description: The physical or digital manifestation of the resource. Typically, Format may include the media-type or dimensions of the resource. Examples of dimensions include size and duration. Format may be used to determine the software, hardware or other equipment needed to display or operate the resource. Recommended best practice is to select a value from a controlled vocabulary (for example, the list of Internet Media Types [http://www.iana.org/assignments/media-types/](https://www.iana.org/assignments/media-types/media-types.xhtmldefining computer media formats).
#### Attributes:
- `type` : a string for example `"video"` or `"image"`.
- `fileFormat` : a string for example `"mp4"` or `"jpg"`.
- `fullDuration` : full duration in ms.
- `start`: the beginning of this item (-1 = the beginning).
- `end`: the end of this item (-1 = the end)
- `fullDimensions`: an array of dimensions in px.
- `region`: the region this item covers. [-1] = the whole media, or [x, y, w, h]
- `uri`: the path to the media file as a string.
- `pages`: an int indicating the number of pages for paged media.

### Identifier
- attribute: `identifier`
- Note that this is set to the element's [path](#path).
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#identifier) description: An unambiguous reference to the resource within a given context. Recommended best practice is to identify the resource by means of a string or number conforming to a formal identification system. Examples of formal identification systems include the Uniform Resource Identifier (URI) (including the Uniform Resource Locator (URL), the Digital Object Identifier (DOI) and the International Standard Book Number (ISBN).
- Default: `os.getcwd()`

### Instructional Method
- attribute: `instructionalMethod`
- The Dublin Core `instructionalMethod` field looks to represent a process, used to engender knowledge, attitudes and skills, that the resource is designed to support. We have interpreted this as a field indicating the method by which the ressource can be displayed/viewed/communicated. Therefore this is where information pertaining to the display of the ressource is given. Notably and options for MemoRekall conversion. This data will have different meanings according to the element type (web, edge or node) and the way it is to be decoded. Spider will parse data into a single instructionalMethod entry which can be easily decoded.
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/usageguide/elements/#instructionalmethod) description: A process, used to engender knowledge, attitudes and skills, that the resource is designed to support. Instructional Method will typically include ways of presenting instructional materials or conducting instructional activities, patterns of learner-to-learner and learner-to-instructor interactions, and mechanisms by which group and individual levels of learning are measured. Instructional methods include all aspects of the instruction and learning processes from planning and implementation through evaluation and feedback.
#### Attributes:
- `color` : a hex color as a string (including the #).
- `important` : a boolean. For MemoRekall parsing, this will indicate if it is a top-level manifest or not.
- `annotationPaint` : a boolean. For MemoRekall parsing, indicate if the node is painted when it is an annotation.
- `annotationOverlay` : a boolean. For MemoRekall parsing, indicate if the annotation is painted ontop of the main ressource or underneath.
- `annotationDisplayPos` : an array of 2 coordinate values in px. For MemoRekall parsing, where to paint the ressourse on the canvas. (starting from top left if overlayed, starting from bottom of main ressource if not overlayed).
- `annotationDisplayScale` : a float. For MemoRekall parsing, the scale of the ressource (1 = full size).

## Other Fields

### Tags
- attribute: `tags`
- Description: An array of strings of ad hoc tags.
- Default: `[]`

### UUID
- attribute: `uuid`
- Description: An unique identifier.
- Default: `uuid.uuid4()`

### Path
- attribute: `path`
- Description: A string indicating the absolute path in disk of the web element. This is equal to [`identifier`](#identifier).
- Default: `os.getcwd()`