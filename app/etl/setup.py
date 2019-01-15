from app import db, models

def load_multivalued_attributes():
    roles = [
        {'name': 'Enslaved', 'name_as_relationship': 'enslaved by'},
        {'name': 'Owner', 'name_as_relationship': 'owner of'},
        {'name': 'Priest', 'name_as_relationship': 'priest for'},
        {'name': 'Inoculated', 'name_as_relationship': 'inoculated by'},
        {'name': 'Bought', 'name_as_relationship': 'bought by'},
        {'name': 'Sold', 'name_as_relationship': 'sold by'},
        {'name': 'Shipped', 'name_as_relationship': 'shipped by'},
        {'name': 'Arrived', 'name_as_relationship': 'delivered by'},
        {'name': 'Escaped', 'name_as_relationship': 'escaped from'},
        {'name': 'Captor', 'name_as_relationship': 'captured'},
        {'name': 'Captured', 'name_as_relationship': 'captured by'},
        {'name': 'Baptised', 'name_as_relationship': 'baptised by'},
        {'name': 'Emancipated', 'name_as_relationship': 'released by'},
        {'name': 'Executed', 'name_as_relationship': 'execeuted by'},
        {'name': 'Parent', 'name_as_relationship': 'parent of'},
        {'name': 'Spouse', 'name_as_relationship': 'spouse of'},
        {'name': 'Child', 'name_as_relationship': 'child of'},
        {'name': 'Mother', 'name_as_relationship': 'mother of'},
        {'name': 'Father', 'name_as_relationship': 'father of'},
        {'name': 'Buyer', 'name_as_relationship': 'buyer of'},
        {'name': 'Seller', 'name_as_relationship': 'seller of'}
    ]
    tribes = [
        {'name': 'Blanco'},
        {'name': 'Bocotora'},
        {'name': 'Codira'},
        {'name': 'Eastern Pequot'},
        {'name': 'Mashantucket Pequot'},
        {'name': 'Mohegan'},
        {'name': 'Naragansett'},
        {'name': 'Nidwa'},
        {'name': 'Noleva'},
        {'name': 'Pequot'},
        {'name': 'Rocotora'},
        {'name': 'Sambo'},
        {'name': 'Shalliba'},
        {'name': 'Shatyana'},
        {'name': 'Tanybec'},
        {'name': 'Tenebec'},
        {'name': 'Tenybec'},
        {'name': 'Toluskey'},
        {'name': 'Valiante'},
        {'name': 'Wampanoag'},
        {'name': 'Woolwa'},
        {'name': 'de Nacion Caribe Cuchibero'}
    ]
    enslavements = [
        {'name': 'Enslaved'},
        {'name': 'Maidservant'},
        {'name': 'Manservant'},
        {'name': 'Indentured Servant'},
        {'name': 'Pieza'},
        {'name': 'Manslave'},
        {'name': 'Servant'},
        {'name': 'Slave'},
        {'name': 'Indenture, Court-Ordered'},
        {'name': 'Indenture, Parental'},
        {'name': 'Indenture, Voluntary'},
        {'name': 'Woman Servant'}
    ]
    races = [
        {'name': 'Part African and Part Indian'},
        {'name': 'Carolina Indian'},
        {'name': 'Creole'},
        {'name': 'Criollo'},
        {'name': 'East India Negro'},
        {'name': 'Half Indian'},
        {'name': 'Indian'},
        {'name': 'Indian Mulatto'},
        {'name': 'Indio'},
        {'name': "Martha's Vineyard Indian"},
        {'name': 'Mestiza'},
        {'name': 'Mestizo'},
        {'name': 'Mulatto'},
        {'name': 'Sambo'},
        {'name': 'Spanish Indian'},
        {'name': 'Surinam Indian'},
        {'name': 'Surrinam Indian'},
        {'name': 'West India Mulatto'}
    ]
    titles = [
        {'name': 'Bro.'},
        {'name': 'Capt.'},
        {'name': 'Captain'},
        {'name': 'Don'},
        {'name': 'Dr.'},
        {'name': 'Esq.'},
        {'name': 'Fray'},
        {'name': 'Hon. Col.'},
        {'name': 'Mistress'},
        {'name': 'Mr.'},
        {'name': 'Mrs.'},
        {'name': 'Reverend Mr.'},
        {'name': 'Widow'}
    ]
    vocations = [
        {'name': 'Baker'},
        {'name': 'Butcher'},
        {'name': 'Carpenter'},
        {'name': 'Chimney-Sweeper'},
        {'name': 'Chirurgeon'},
        {'name': 'Cooper'},
        {'name': 'Cordwainer'},
        {'name': 'Farmer'},
        {'name': 'Gentleman'},
        {'name': 'Gobernador y Capitan General of the Trinidad Island'},
        {'name': 'Governor'},
        {'name': 'Herald'},
        {'name': 'Household Work'},
        {'name': 'Husbandman'},
        {'name': 'Lawyer'},
        {'name': 'Leather Dresser'},
        {'name': 'Leatherer'},
        {'name': 'Malster'},
        {'name': 'Mariner'},
        {'name': 'Merchant'},
        {'name': 'Mineworker'},
        {'name': 'Minister'},
        {'name': 'Sadler'},
        {'name': 'Sailor'},
        {'name': 'Sargento Mayor Actual (De Esta Ciudad)'},
        {'name': 'Sawyer'},
        {'name': 'Sawyer & Carpenter'},
        {'name': 'Ship Carpenter'},
        {'name': 'Ship Captain'},
        {'name': 'Shipwright'},
        {'name': 'Shopkeeper'},
        {'name': 'Tailor'},
        {'name': 'Cura y Vicario de la Iglesia Parroquia de Esta Ciudad'},
        {'name': 'Guardián del Convento de San Francisco de Esta Ciudad'},
        {'name': 'of Bragmans'},
        {'name': 'Presbitero'},
        {'name': 'Sacristán Mayor'},
        {'name': 'Sargento Mayor Actual de Esta Ciudad'}
    ]
    origins = [
        { 'name': 'Allentown' },
        { 'name': 'Bermuda' },
        { 'name': 'Casanare' },
        { 'name': 'Casanave' },
        { 'name': 'Chabba' },
        { 'name': 'Jamaica' },
        { 'name': 'Pueblo de Casanare' },
        { 'name': 'Pueblo de Pauto' },
        { 'name': 'Píritu' },
        { 'name': 'Rio de Orinoco' },
        { 'name': 'Shangena' },
        { 'name': 'Spain' },
        { 'name': 'Yiuby' },
        { 'name': 'Yulusky' }
    ]
    reference_types = [
        {'name': 'Baptism'},
        {'name': 'Runaway'},
        {'name': 'Sale'},
        {'name': 'Capture'},
        {'name': 'Inoculation'},
        {'name': 'Execution'},
        {'name': 'Manumission'},
        {'name': 'Entry'},
        {'name': 'Indenture'},
        {'name': 'Account'},
        {'name': 'Note'},
        {'name': 'Inventory'},
        {'name': 'Reference'}
    ]
    name_types = [
        { 'name': 'Alias' },
        { 'name': 'Baptismal' },
        { 'name': 'English' },
        { 'name': 'European' },
        { 'name': 'Indian' },
        { 'name': 'Nickname' },
        { 'name': 'Given' },
        { 'name': 'Unknown' }
    ]
    natl_ctx = [
        { 'name': 'British' },
        { 'name': 'American' },
        { 'name': 'French' },
        { 'name': 'Spanish' },
        { 'name': 'Other'}
    ]
    zotero_types = [
        {'name': 'artwork', 'creator_name' : 'artist'},
        {'name': 'audioRecording', 'creator_name' : 'performer'},
        {'name': 'bill', 'creator_name' : 'sponsor'},
        {'name': 'blogPost', 'creator_name' : 'author'},
        {'name': 'book', 'creator_name' : 'author'},
        {'name': 'bookSection', 'creator_name' : 'author'},
        {'name': 'case', 'creator_name' : 'author'},
        {'name': 'computerProgram', 'creator_name' : 'programmer'},
        {'name': 'conferencePaper', 'creator_name' : 'author'},
        {'name': 'dictionaryEntry', 'creator_name' : 'author'},
        {'name': 'document', 'creator_name' : 'author'},
        {'name': 'email', 'creator_name' : 'author'},
        {'name': 'encyclopediaArticle', 'creator_name' : 'author'},
        {'name': 'film', 'creator_name' : 'director'},
        {'name': 'forumPost', 'creator_name' : 'author'},
        {'name': 'hearing', 'creator_name' : 'contributor'},
        {'name': 'instantMessage', 'creator_name' : 'author'},
        {'name': 'interview', 'creator_name' : 'interviewee'},
        {'name': 'journalArticle', 'creator_name' : 'author'},
        {'name': 'letter', 'creator_name' : 'author'},
        {'name': 'magazineArticle', 'creator_name' : 'author'},
        {'name': 'manuscript', 'creator_name' : 'author'},
        {'name': 'map', 'creator_name' : 'cartographer'},
        {'name': 'newspaperArticle', 'creator_name' : 'author'},
        {'name': 'patent', 'creator_name' : 'inventor'},
        {'name': 'podcast', 'creator_name' : 'podcaster'},
        {'name': 'presentation', 'creator_name' : 'presenter'},
        {'name': 'radioBroadcast', 'creator_name' : 'director'},
        {'name': 'report', 'creator_name' : 'author'},
        {'name': 'statute', 'creator_name' : 'author'},
        {'name': 'thesis', 'creator_name' : 'author'},
        {'name': 'tvBroadcast', 'creator_name' : 'director'},
        {'name': 'videoRecording', 'creator_name' : 'director'},
        {'name': 'webpage', 'creator_name' : 'author'},
        {'name': 'note', 'creator_name' : None }
    ]
    zotero_fields = [
        { 'name': 'DOI' },
        { 'name': 'ISBN' },
        { 'name': 'ISSN' },
        { 'name': 'abstractNote' },
        { 'name': 'accessDate' },
        { 'name': 'applicationNumber' },
        { 'name': 'archive' },
        { 'name': 'archiveLocation' },
        { 'name': 'artworkMedium' },
        { 'name': 'artworkSize' },
        { 'name': 'assignee' },
        { 'name': 'audioFileType' },
        { 'name': 'audioRecordingFormat' },
        { 'name': 'billNumber' },
        { 'name': 'blogTitle' },
        { 'name': 'bookTitle' },
        { 'name': 'callNumber' },
        { 'name': 'caseName' },
        { 'name': 'code' },
        { 'name': 'codeNumber' },
        { 'name': 'codePages' },
        { 'name': 'codeVolume' },
        { 'name': 'collections' }, #Zotero metadata
        { 'name': 'committee' },
        { 'name': 'company' },
        { 'name': 'conferenceName' },
        { 'name': 'country' },
        { 'name': 'court' },
        { 'name': 'creators' }, #Special concerns
        { 'name': 'date' },
        { 'name': 'dateDecided' },
        { 'name': 'dateEnacted' },
        { 'name': 'dictionaryTitle' },
        { 'name': 'distributor' },
        { 'name': 'docketNumber' },
        { 'name': 'documentNumber' },
        { 'name': 'edition' },
        { 'name': 'encyclopediaTitle' },
        { 'name': 'episodeNumber' },
        { 'name': 'extra' },
        { 'name': 'filingDate' },
        { 'name': 'firstPage' },
        { 'name': 'forumTitle' },
        { 'name': 'genre' },
        { 'name': 'history' },
        { 'name': 'institution' },
        { 'name': 'interviewMedium' },
        { 'name': 'issue' },
        { 'name': 'issueDate' },
        { 'name': 'issuingAuthority' },
        { 'name': 'itemType' }, #Zotero metadata 
        { 'name': 'journalAbbreviation' },
        { 'name': 'label' },
        { 'name': 'language' },
        { 'name': 'legalStatus' },
        { 'name': 'legislativeBody' },
        { 'name': 'letterType' },
        { 'name': 'libraryCatalog' },
        { 'name': 'manuscriptType' },
        { 'name': 'mapType' },
        { 'name': 'meetingName' },
        { 'name': 'nameOfAct' },
        { 'name': 'network' },
        { 'name': 'note' },
        { 'name': 'numPages' },
        { 'name': 'numberOfVolumes' },
        { 'name': 'pages' },
        { 'name': 'patentNumber' },
        { 'name': 'place' },
        { 'name': 'postType' },
        { 'name': 'presentationType' },
        { 'name': 'priorityNumbers' },
        { 'name': 'proceedingsTitle' },
        { 'name': 'programTitle' },
        { 'name': 'programmingLanguage' },
        { 'name': 'publicLawNumber' },
        { 'name': 'publicationTitle' },
        { 'name': 'publisher' },
        { 'name': 'references' },
        { 'name': 'relations' }, #Zotero metadata
        { 'name': 'reportNumber' },
        { 'name': 'reportType' },
        { 'name': 'reporter' },
        { 'name': 'reporterVolume' },
        { 'name': 'rights' },
        { 'name': 'runningTime' },
        { 'name': 'scale' },
        { 'name': 'section' },
        { 'name': 'series' },
        { 'name': 'seriesNumber' },
        { 'name': 'seriesText' },
        { 'name': 'seriesTitle' },
        { 'name': 'session' },
        { 'name': 'shortTitle' },
        { 'name': 'studio' },
        { 'name': 'subject' },
        { 'name': 'system' },
        { 'name': 'tags' }, #Zotero metadata
        { 'name': 'thesisType' },
        { 'name': 'title' },
        { 'name': 'university' },
        { 'name': 'url' },
        { 'name': 'versionNumber' },
        { 'name': 'videoRecordingFormat' },
        { 'name': 'volume' },
        { 'name': 'websiteTitle' },
        { 'name': 'websiteType' }
    ]

    location_types = [
        {'name': 'Colony/State'},
        {'name': 'String Location'},
        {'name': 'Locale'},
        {'name': 'City'},
        {'name': 'Colony'},
        {'name': 'State'},
        {'name': 'Town'},
        {'name': 'County'},
        {'name': 'Region'},
        {'name': 'Church'},
        {'name': 'Ship'}
    ]

    tables = [
        ( models.Role, roles ),
        ( models.ReferenceType, reference_types ),
        ( models.Race, races ),
        ( models.Vocation, vocations ),
        ( models.Tribe, tribes ),
        ( models.Title, titles ),
        ( models.NameType, name_types ),
        ( models.EnslavementType, enslavements ),
        ( models.Location, origins ),
        ( models.NationalContext, natl_ctx ),
        ( models.ZoteroType, zotero_types ),
        ( models.ZoteroField, zotero_fields ),
        ( models.LocationType, location_types ),
    ]
    for pair in tables:
        table = pair[0]
        for data in pair[1]:
            row = table(**data)
            db.session.add(row)
            print('{}: value {}'.format(table.__tablename__, data))
        db.session.commit()

def load_many_to_one():
    citation_types = [
        #DISA local names
        {'name': 'Runaway Advertisement'},
        {'name': 'Runaway Capture Advertisement'},
        {'name': 'Advertisement of Sale'},
        {'name': 'Smallpox Inoculation Notice'},
        {'name': 'Execution Notice'},
        {'name': 'Census'},
        {'name': 'Court Document'},
        {'name': 'Inventory'},
        {'name': 'List'},
        {'name': 'Registry'},
        {'name': 'Probate Record'},
        {'name': 'Record'},
        {'name': 'Town Record'},
        {'name': 'Will'},
        {'name': 'Section'},

        #Zotero native types
        {'name': 'Artwork'},
        {'name': 'Audio Recording'},
        {'name': 'Bill'},
        {'name': 'Blog Post'},
        {'name': 'Book'},
        {'name': 'Book Section'},
        {'name': 'Case'},
        {'name': 'Computer Program'},
        {'name': 'Conference Paper'},
        {'name': 'Dictionary Entry'},
        {'name': 'Document'},
        {'name': 'Email'},
        {'name': 'Encyclopedia Article'},
        {'name': 'Film'},
        {'name': 'Forum Post'},
        {'name': 'Hearing'},
        {'name': 'Instant Message'},
        {'name': 'Interview'},
        {'name': 'Journal Article'},
        {'name': 'Letter'},
        {'name': 'Magazine Article'},
        {'name': 'Manuscript'},
        {'name': 'Map'},
        {'name': 'Newspaper Article'},
        {'name': 'Patent'},
        {'name': 'Podcast'},
        {'name': 'Presentation'},
        {'name': 'Radio Broadcast'},
        {'name': 'Report'},
        {'name': 'Statute'},
        {'name': 'Thesis'},
        {'name': 'TV Broadcast'},
        {'name': 'Video Recording'},
        {'name': 'Webpage'},
        {'name': 'Note'}
    ]
    ctype_ztype = {
        'Runaway Advertisement': 'newspaperArticle',
        'Runaway Capture Advertisement': 'newspaperArticle',
        'Advertisement of Sale': 'newspaperArticle',
        'Smallpox Inoculation Notice': 'newspaperArticle',
        'Execution Notice': 'newspaperArticle',
        'Census': 'manuscript',
        'Court Document': 'case',
        'Inventory': 'manuscript',
        'List': 'manuscript',
        'Registry': 'manuscript',
        'Probate Record': 'case',
        'Record': 'manuscript',
        'Town Record': 'manuscript',
        'Will': 'manuscript',
        'Section': 'manuscript',

        'Artwork' : 'artwork',
        'Audio Recording' : 'audioRecording',
        'Bill' : 'bill',
        'Blog Post' : 'blogPost',
        'Book' : 'book',
        'Book Section' : 'bookSection',
        'Case' : 'case',
        'Computer Program' : 'computerProgram',
        'Conference Paper' : 'conferencePaper',
        'Dictionary Entry' : 'dictionaryEntry',
        'Document' : 'document',
        'Email' : 'email',
        'Encyclopedia Article' : 'encyclopediaArticle',
        'Film' : 'film',
        'Forum Post' : 'forumPost',
        'Hearing' : 'hearing',
        'Instant Message' : 'instantMessage',
        'Interview' : 'interview',
        'Journal Article' : 'journalArticle',
        'Letter' : 'letter',
        'Magazine Article' : 'magazineArticle',
        'Manuscript' : 'manuscript',
        'Map' : 'map',
        'Newspaper Article' : 'newspaperArticle',
        'Patent' : 'patent',
        'Podcast' : 'podcast',
        'Presentation' : 'presentation',
        'Radio Broadcast' : 'radioBroadcast',
        'Report' : 'report',
        'Statute' : 'statute',
        'Thesis' : 'thesis',
        'TV Broadcast' : 'tvBroadcast',
        'Video Recording' : 'videoRecording',
        'Webpage' : 'webpage',
        'Note' : 'note'
    }

    many_to_one = [
        (models.CitationType, models.ZoteroType, citation_types,
            ctype_ztype, 'zotero_type_id')
    ]

    for one in many_to_one:
        table = one[0]
        ref = one[1]
        for data in one[2]:
            ref_obj = ref.query.filter_by(name=one[3][data['name']]).first()
            data[one[4]] = ref_obj.id
            row = table(**data)
            db.session.add(row)
            print('{}: value {}'.format(table.__tablename__, data))
        db.session.commit()


def load_many_to_many():
    referencetype_roles = [
        ('Manumission', ['Owner','Emancipated']),
        ('Runaway', ['Owner','Escaped']),
        ('Sale', ['Owner','Enslaved']),
        ('Baptism', ['Owner','Priest','Baptised']),
        ('Capture', ['Captor', 'Captured']),
        ('Inoculation', ['Inoculated','Owner']),
        ('Execution', ['Executed']),
    ]

    zoterotype_fields = [
        ('artwork', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'artworkMedium', 'artworkSize', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'libraryCatalog', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('audioRecording', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'audioRecordingFormat', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'label', 'language', 'libraryCatalog', 'numberOfVolumes', 'place', 'relations', 'rights', 'runningTime', 'seriesTitle', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('bill', ['abstractNote', 'accessDate', 'billNumber', 'code', 'codePages', 'codeVolume', 'collections', 'creators', 'date', 'extra', 'history', 'itemType', 'language', 'legislativeBody', 'relations', 'rights', 'section', 'session', 'shortTitle', 'tags', 'title', 'url']),
        ('blogPost', ['abstractNote', 'accessDate', 'blogTitle', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url', 'websiteType']),
        ('book', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'edition', 'extra', 'itemType', 'language', 'libraryCatalog', 'numPages', 'numberOfVolumes', 'place', 'publisher', 'relations', 'rights', 'series', 'seriesNumber', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('bookSection', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'bookTitle', 'callNumber', 'collections', 'creators', 'date', 'edition', 'extra', 'itemType', 'language', 'libraryCatalog', 'numberOfVolumes', 'pages', 'place', 'publisher', 'relations', 'rights', 'series', 'seriesNumber', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('case', ['abstractNote', 'accessDate', 'caseName', 'collections', 'court', 'creators', 'dateDecided', 'docketNumber', 'extra', 'firstPage', 'history', 'itemType', 'language', 'relations', 'reporter', 'reporterVolume', 'rights', 'shortTitle', 'tags', 'url']),
        ('computerProgram', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'company', 'creators', 'date', 'extra', 'itemType', 'libraryCatalog', 'place', 'programmingLanguage', 'relations', 'rights', 'seriesTitle', 'shortTitle', 'system', 'tags', 'title', 'url', 'versionNumber']),
        ('conferencePaper', ['DOI', 'ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'conferenceName', 'creators', 'date', 'extra', 'itemType', 'language', 'libraryCatalog', 'pages', 'place', 'proceedingsTitle', 'publisher', 'relations', 'rights', 'series', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('dictionaryEntry', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'dictionaryTitle', 'edition', 'extra', 'itemType', 'language', 'libraryCatalog', 'numberOfVolumes', 'pages', 'place', 'publisher', 'relations', 'rights', 'series', 'seriesNumber', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('document', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'libraryCatalog', 'publisher', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('email', ['abstractNote', 'accessDate', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'relations', 'rights', 'shortTitle', 'subject', 'tags', 'url']),
        ('encyclopediaArticle', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'edition', 'encyclopediaTitle', 'extra', 'itemType', 'language', 'libraryCatalog', 'numberOfVolumes', 'pages', 'place', 'publisher', 'relations', 'rights', 'series', 'seriesNumber', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('film', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'distributor', 'extra', 'genre', 'itemType', 'language', 'libraryCatalog', 'relations', 'rights', 'runningTime', 'shortTitle', 'tags', 'title', 'url', 'videoRecordingFormat']),
        ('forumPost', ['abstractNote', 'accessDate', 'collections', 'creators', 'date', 'extra', 'forumTitle', 'itemType', 'language', 'postType', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('hearing', ['abstractNote', 'accessDate', 'collections', 'committee', 'creators', 'date', 'documentNumber', 'extra', 'history', 'itemType', 'language', 'legislativeBody', 'numberOfVolumes', 'pages', 'place', 'publisher', 'relations', 'rights', 'session', 'shortTitle', 'tags', 'title', 'url']),
        ('instantMessage', ['abstractNote', 'accessDate', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('interview', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'interviewMedium', 'itemType', 'language', 'libraryCatalog', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('journalArticle', ['DOI', 'ISSN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'issue', 'itemType', 'journalAbbreviation', 'language', 'libraryCatalog', 'pages', 'publicationTitle', 'relations', 'rights', 'series', 'seriesText', 'seriesTitle', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('letter', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'letterType', 'libraryCatalog', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('magazineArticle', ['ISSN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'issue', 'itemType', 'language', 'libraryCatalog', 'pages', 'publicationTitle', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url', 'volume']),
        ('manuscript', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'libraryCatalog', 'manuscriptType', 'numPages', 'place', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('map', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'edition', 'extra', 'itemType', 'language', 'libraryCatalog', 'mapType', 'place', 'publisher', 'relations', 'rights', 'scale', 'seriesTitle', 'shortTitle', 'tags', 'title', 'url']),
        ('newspaperArticle', ['ISSN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'edition', 'extra', 'itemType', 'language', 'libraryCatalog', 'pages', 'place', 'publicationTitle', 'relations', 'rights', 'section', 'shortTitle', 'tags', 'title', 'url']),
        ('patent', ['abstractNote', 'accessDate', 'applicationNumber', 'assignee', 'collections', 'country', 'creators', 'extra', 'filingDate', 'issueDate', 'issuingAuthority', 'itemType', 'language', 'legalStatus', 'pages', 'patentNumber', 'place', 'priorityNumbers', 'references', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('podcast', ['abstractNote', 'accessDate', 'audioFileType', 'collections', 'creators', 'episodeNumber', 'extra', 'itemType', 'language', 'relations', 'rights', 'runningTime', 'seriesTitle', 'shortTitle', 'tags', 'title', 'url']),
        ('presentation', ['abstractNote', 'accessDate', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'meetingName', 'place', 'presentationType', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url']),
        ('radioBroadcast', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'audioRecordingFormat', 'callNumber', 'collections', 'creators', 'date', 'episodeNumber', 'extra', 'itemType', 'language', 'libraryCatalog', 'network', 'place', 'programTitle', 'relations', 'rights', 'runningTime', 'shortTitle', 'tags', 'title', 'url']),
        ('report', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'institution', 'itemType', 'language', 'libraryCatalog', 'pages', 'place', 'relations', 'reportNumber', 'reportType', 'rights', 'seriesTitle', 'shortTitle', 'tags', 'title', 'url']),
        ('statute', ['abstractNote', 'accessDate', 'code', 'codeNumber', 'collections', 'creators', 'dateEnacted', 'extra', 'history', 'itemType', 'language', 'nameOfAct', 'pages', 'publicLawNumber', 'relations', 'rights', 'section', 'session', 'shortTitle', 'tags', 'url']),
        ('thesis', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'libraryCatalog', 'numPages', 'place', 'relations', 'rights', 'shortTitle', 'tags', 'thesisType', 'title', 'university', 'url']),
        ('tvBroadcast', ['abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'episodeNumber', 'extra', 'itemType', 'language', 'libraryCatalog', 'network', 'place', 'programTitle', 'relations', 'rights', 'runningTime', 'shortTitle', 'tags', 'title', 'url', 'videoRecordingFormat']),
        ('videoRecording', ['ISBN', 'abstractNote', 'accessDate', 'archive', 'archiveLocation', 'callNumber', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'libraryCatalog', 'numberOfVolumes', 'place', 'relations', 'rights', 'runningTime', 'seriesTitle', 'shortTitle', 'studio', 'tags', 'title', 'url', 'videoRecordingFormat', 'volume']),
        ('webpage', ['abstractNote', 'accessDate', 'collections', 'creators', 'date', 'extra', 'itemType', 'language', 'relations', 'rights', 'shortTitle', 'tags', 'title', 'url', 'websiteTitle', 'websiteType']),
        ('note', ['collections', 'itemType', 'note', 'relations', 'tags'])
    ]

    many_to_many = [
        (models.ReferenceType, models.Role, referencetype_roles,
            'name', 'name', 'roles'),
        (models.ZoteroType, models.ZoteroField, zoterotype_fields,
            'name', 'name', 'template_fields')
    ]

    for many in many_to_many:
        model1 = many[0]
        model2 = many[1]
        for mapping in many[2]:
            query = { many[3]: mapping[0] }
            focus = model1.query.filter_by( **query ).first()
            opts  = model2.query.all()
            rel = [ o for o in opts if getattr(o, many[4]) in mapping[1] ]
            getattr(focus, many[5]).extend(rel)
            db.session.add(focus)
            print( "{}:{} associated with {}:{}".format(
                model1.__tablename__, mapping[0],
                model2.__tablename__, mapping[1]) )
            db.session.commit()

def load_self_references():
    tables = [ (models.Role, 'roles') ]

    role_references = [
        ('captor', 'captured')
    ]
    references = {}