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
        {'name': 'Mustee'},
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
        {'name': 'Sargento Mayor Actual de Esta Ciudad'},
        {'name': 'Spinner'},
        {'name': 'Tanner'}
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
        {'name': 'Unspecified'},
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
        {'name': 'DOI', 'display_name': 'DOI' },
        {'name': 'ISBN', 'display_name': 'ISBN' },
        {'name': 'ISSN', 'display_name': 'ISSN' },
        {'name': 'abstractNote', 'display_name': 'Abstract Note' },
        {'name': 'accessDate', 'display_name': 'Access Date' },
        {'name': 'applicationNumber', 'display_name': 'Application Number' },
        {'name': 'archive', 'display_name': 'Archive' },
        {'name': 'archiveLocation', 'display_name': 'Archive Location' },
        {'name': 'artworkMedium', 'display_name': 'Artwork Medium' },
        {'name': 'artworkSize', 'display_name': 'Artwork Size' },
        {'name': 'assignee', 'display_name': 'Assignee' },
        {'name': 'audioFileType', 'display_name': 'Audio File Type' },
        {'name': 'audioRecordingFormat', 'display_name': 'Audio Recording Format' },
        {'name': 'billNumber', 'display_name': 'Bill Number' },
        {'name': 'blogTitle', 'display_name': 'Blog Title' },
        {'name': 'bookTitle', 'display_name': 'Book Title' },
        {'name': 'callNumber', 'display_name': 'Call Number' },
        {'name': 'caseName', 'display_name': 'Case Name' },
        {'name': 'code', 'display_name': 'Code' },
        {'name': 'codeNumber', 'display_name': 'Code Number' },
        {'name': 'codePages', 'display_name': 'Code Pages' },
        {'name': 'codeVolume', 'display_name': 'Code Volume' },
        {'name': 'collections', 'display_name': 'Collections' }, #Zotero metadata
        {'name': 'committee', 'display_name': 'Committee' },
        {'name': 'company', 'display_name': 'Company' },
        {'name': 'conferenceName', 'display_name': 'Conference Name' },
        {'name': 'country', 'display_name': 'Country' },
        {'name': 'court', 'display_name': 'Court' },
        {'name': 'creators', 'display_name': 'Creators' }, #Special concerns
        {'name': 'date', 'display_name': 'Date' },
        {'name': 'dateDecided', 'display_name': 'Date Decided' },
        {'name': 'dateEnacted', 'display_name': 'Date Enacted' },
        {'name': 'dictionaryTitle', 'display_name': 'Dictionary Title' },
        {'name': 'distributor', 'display_name': 'Distributor' },
        {'name': 'docketNumber', 'display_name': 'Docket Number' },
        {'name': 'documentNumber', 'display_name': 'Document Number' },
        {'name': 'edition', 'display_name': 'Edition' },
        {'name': 'encyclopediaTitle', 'display_name': 'Encyclopedia Title' },
        {'name': 'episodeNumber', 'display_name': 'Episode Number' },
        {'name': 'extra', 'display_name': 'Extra' },
        {'name': 'filingDate', 'display_name': 'Filing Date' },
        {'name': 'firstPage', 'display_name': 'First Page' },
        {'name': 'forumTitle', 'display_name': 'Forum Title' },
        {'name': 'genre', 'display_name': 'Genre' },
        {'name': 'history', 'display_name': 'History' },
        {'name': 'institution', 'display_name': 'Institution' },
        {'name': 'interviewMedium', 'display_name': 'Interview Medium' },
        {'name': 'issue', 'display_name': 'Issue' },
        {'name': 'issueDate', 'display_name': 'Issue Date' },
        {'name': 'issuingAuthority', 'display_name': 'Issuing Authority' },
        {'name': 'itemType', 'display_name': 'Item Type' }, #Zotero metadata 
        {'name': 'journalAbbreviation', 'display_name': 'Journal Abbreviation' },
        {'name': 'label', 'display_name': 'Label' },
        {'name': 'language', 'display_name': 'Language' },
        {'name': 'legalStatus', 'display_name': 'Legal Status' },
        {'name': 'legislativeBody', 'display_name': 'Legislative Body' },
        {'name': 'letterType', 'display_name': 'Letter Type' },
        {'name': 'libraryCatalog', 'display_name': 'Library Catalog' },
        {'name': 'manuscriptType', 'display_name': 'Manuscript Type' },
        {'name': 'mapType', 'display_name': 'Map Type' },
        {'name': 'meetingName', 'display_name': 'Meeting Name' },
        {'name': 'nameOfAct', 'display_name': 'Name of Act' },
        {'name': 'network', 'display_name': 'Network' },
        {'name': 'note', 'display_name': 'Note' },
        {'name': 'numPages', 'display_name': 'Num Pages' },
        {'name': 'numberOfVolumes', 'display_name': 'Number of Volumes' },
        {'name': 'pages', 'display_name': 'Pages' },
        {'name': 'patentNumber', 'display_name': 'Patent Number' },
        {'name': 'place', 'display_name': 'Place' },
        {'name': 'postType', 'display_name': 'Post Type' },
        {'name': 'presentationType', 'display_name': 'Presentation Type' },
        {'name': 'priorityNumbers', 'display_name': 'Priority Numbers' },
        {'name': 'proceedingsTitle', 'display_name': 'Proceedings Title' },
        {'name': 'programTitle', 'display_name': 'Program Title' },
        {'name': 'programmingLanguage', 'display_name': 'Programming Language' },
        {'name': 'publicLawNumber', 'display_name': 'Public Law Number' },
        {'name': 'publicationTitle', 'display_name': 'Publication Title' },
        {'name': 'publisher', 'display_name': 'Publisher' },
        {'name': 'references', 'display_name': 'References' },
        {'name': 'relations', 'display_name': 'Relations' }, #Zotero metadata
        {'name': 'reportNumber', 'display_name': 'Report Number' },
        {'name': 'reportType', 'display_name': 'Report Type' },
        {'name': 'reporter', 'display_name': 'Reporter' },
        {'name': 'reporterVolume', 'display_name': 'Reporter Volume' },
        {'name': 'rights', 'display_name': 'Rights' },
        {'name': 'runningTime', 'display_name': 'Running Time' },
        {'name': 'scale', 'display_name': 'Scale' },
        {'name': 'section', 'display_name': 'Section' },
        {'name': 'series', 'display_name': 'Series' },
        {'name': 'seriesNumber', 'display_name': 'Series Number' },
        {'name': 'seriesText', 'display_name': 'Series Text' },
        {'name': 'seriesTitle', 'display_name': 'Series Title' },
        {'name': 'session', 'display_name': 'Session' },
        {'name': 'shortTitle', 'display_name': 'Short Title' },
        {'name': 'studio', 'display_name': 'Studio' },
        {'name': 'subject', 'display_name': 'Subject' },
        {'name': 'system', 'display_name': 'System' },
        {'name': 'tags', 'display_name': 'Tags' }, #Zotero metadata
        {'name': 'thesisType', 'display_name': 'Thesis Type' },
        {'name': 'title', 'display_name': 'Title' },
        {'name': 'university', 'display_name': 'University' },
        {'name': 'url', 'display_name': 'URL' },
        {'name': 'versionNumber', 'display_name': 'Version Number' },
        {'name': 'videoRecordingFormat', 'display_name': 'Video Recording Format' },
        {'name': 'volume', 'display_name': 'Volume' },
        {'name': 'websiteTitle', 'display_name': 'Website Title' },
        {'name': 'websiteType', 'display_name': 'Website Type' },
        {'name': 'author', 'display_name': 'Author' },
        {'name': 'director', 'display_name': 'Director' },
        {'name': 'inventor', 'display_name': 'Inventor' },
        {'name': 'performer', 'display_name': 'Performer' },
        {'name': 'presenter', 'display_name': 'Presenter' },
        {'name': 'programmer', 'display_name': 'Programmer' },
        {'name': 'contributor', 'display_name': 'Contributor' },
        {'name': 'artist', 'display_name': 'Artist' },
        {'name': 'sponsor', 'display_name': 'Sponsor' },
        {'name': 'interviewee', 'display_name': 'Interviewee' },
        {'name': 'cartographer', 'display_name': 'Cartographer' },
        {'name': 'podcaster', 'display_name': 'Podcaster' }
    ]

    location_types = [
        {'name': 'Colony/State'},
        {'name': 'Location'},
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

    many_to_many = [
        (models.ReferenceType, models.Role, referencetype_roles,
            'name', 'name', 'roles'),
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

def load_many_to_many_with_attr():

    zoterotype_fields = [
        ('artwork', ['title', 'artist', 'abstractNote', 'artworkMedium', 'artworkSize', 'date', 'language', 'shortTitle', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'url', 'accessDate', 'rights', 'extra']),
        ('audioRecording', ['title', 'performer', 'abstractNote', 'audioRecordingFormat', 'seriesTitle', 'volume', 'numberOfVolumes', 'place', 'label', 'date', 'runningTime', 'language', 'ISBN', 'shortTitle', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'url', 'accessDate', 'rights', 'extra']),
        ('bill', ['title', 'sponsor', 'abstractNote', 'billNumber', 'code', 'codeVolume', 'section', 'codePages', 'legislativeBody', 'session', 'history', 'date', 'language', 'url', 'accessDate', 'shortTitle', 'rights', 'extra']),
        ('blogPost', ['title', 'author', 'abstractNote', 'blogTitle', 'websiteType', 'date', 'url', 'accessDate', 'language', 'shortTitle', 'rights', 'extra']),
        ('book', ['title', 'author', 'abstractNote', 'series', 'seriesNumber', 'volume', 'numberOfVolumes', 'edition', 'place', 'publisher', 'date', 'numPages', 'language', 'ISBN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('bookSection', ['title', 'author', 'abstractNote', 'bookTitle', 'series', 'seriesNumber', 'volume', 'numberOfVolumes', 'edition', 'place', 'publisher', 'date', 'pages', 'language', 'ISBN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('case', ['caseName', 'author', 'abstractNote', 'reporter', 'reporterVolume', 'court', 'docketNumber', 'firstPage', 'history', 'dateDecided', 'language', 'shortTitle', 'url', 'accessDate', 'rights', 'extra']),
        ('computerProgram', ['title', 'programmer', 'abstractNote', 'seriesTitle', 'versionNumber', 'date', 'system', 'place', 'company', 'programmingLanguage', 'ISBN', 'shortTitle', 'url', 'rights', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'accessDate', 'extra']),
        ('conferencePaper', ['title', 'author', 'abstractNote', 'date', 'proceedingsTitle', 'conferenceName', 'place', 'publisher', 'volume', 'pages', 'series', 'language', 'DOI', 'ISBN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('dictionaryEntry', ['title', 'author', 'abstractNote', 'dictionaryTitle', 'series', 'seriesNumber', 'volume', 'numberOfVolumes', 'edition', 'place', 'publisher', 'date', 'pages', 'language', 'ISBN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('document', ['title', 'author', 'abstractNote', 'publisher', 'date', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('email', ['subject', 'author', 'abstractNote', 'date', 'shortTitle', 'url', 'accessDate', 'language', 'rights', 'extra']),
        ('encyclopediaArticle', ['title', 'author', 'abstractNote', 'encyclopediaTitle', 'series', 'seriesNumber', 'volume', 'numberOfVolumes', 'edition', 'place', 'publisher', 'date', 'pages', 'ISBN', 'shortTitle', 'url', 'accessDate', 'language', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('film', ['title', 'director', 'abstractNote', 'distributor', 'date', 'genre', 'videoRecordingFormat', 'runningTime', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('forumPost', ['title', 'author', 'abstractNote', 'forumTitle', 'postType', 'date', 'language', 'shortTitle', 'url', 'accessDate', 'rights', 'extra']),
        ('hearing', ['title', 'contributor', 'abstractNote', 'committee', 'place', 'publisher', 'numberOfVolumes', 'documentNumber', 'pages', 'legislativeBody', 'session', 'history', 'date', 'language', 'shortTitle', 'url', 'accessDate', 'rights', 'extra']),
        ('instantMessage', ['title', 'author', 'abstractNote', 'date', 'language', 'shortTitle', 'url', 'accessDate', 'rights', 'extra']),
        ('interview', ['title', 'interviewee', 'abstractNote', 'date', 'interviewMedium', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('journalArticle', ['title', 'author', 'abstractNote', 'publicationTitle', 'volume', 'issue', 'pages', 'date', 'series', 'seriesTitle', 'seriesText', 'journalAbbreviation', 'language', 'DOI', 'ISSN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('letter', ['title', 'author', 'abstractNote', 'letterType', 'date', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('magazineArticle', ['title', 'author', 'abstractNote', 'publicationTitle', 'volume', 'issue', 'date', 'pages', 'language', 'ISSN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('manuscript', ['title', 'author', 'abstractNote', 'manuscriptType', 'place', 'date', 'numPages', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('map', ['title', 'cartographer', 'abstractNote', 'mapType', 'scale', 'seriesTitle', 'edition', 'place', 'publisher', 'date', 'language', 'ISBN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('newspaperArticle', ['title', 'author', 'abstractNote', 'publicationTitle', 'place', 'edition', 'date', 'section', 'pages', 'language', 'shortTitle', 'ISSN', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('patent', ['title', 'inventor', 'abstractNote', 'place', 'country', 'assignee', 'issuingAuthority', 'patentNumber', 'filingDate', 'pages', 'applicationNumber', 'priorityNumbers', 'issueDate', 'references', 'legalStatus', 'language', 'shortTitle', 'url', 'accessDate', 'rights', 'extra']),
        ('podcast', ['title', 'podcaster', 'abstractNote', 'seriesTitle', 'episodeNumber', 'audioFileType', 'runningTime', 'url', 'accessDate', 'language', 'shortTitle', 'rights', 'extra']),
        ('presentation', ['title', 'presenter', 'abstractNote', 'presentationType', 'date', 'place', 'meetingName', 'url', 'accessDate', 'language', 'shortTitle', 'rights', 'extra']),
        ('radioBroadcast', ['title', 'director', 'abstractNote', 'programTitle', 'episodeNumber', 'audioRecordingFormat', 'place', 'network', 'date', 'runningTime', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('report', ['title', 'author', 'abstractNote', 'reportNumber', 'reportType', 'seriesTitle', 'place', 'institution', 'date', 'pages', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('statute', ['nameOfAct', 'author', 'abstractNote', 'code', 'codeNumber', 'publicLawNumber', 'dateEnacted', 'pages', 'section', 'session', 'history', 'language', 'shortTitle', 'url', 'accessDate', 'rights', 'extra']),
        ('thesis', ['title', 'author', 'abstractNote', 'thesisType', 'university', 'place', 'date', 'numPages', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('tvBroadcast', ['title', 'director', 'abstractNote', 'programTitle', 'episodeNumber', 'videoRecordingFormat', 'place', 'network', 'date', 'runningTime', 'language', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('videoRecording', ['title', 'director', 'abstractNote', 'videoRecordingFormat', 'seriesTitle', 'volume', 'numberOfVolumes', 'place', 'studio', 'date', 'runningTime', 'language', 'ISBN', 'shortTitle', 'url', 'accessDate', 'archive', 'archiveLocation', 'libraryCatalog', 'callNumber', 'rights', 'extra']),
        ('webpage', ['title', 'author', 'abstractNote', 'websiteTitle', 'websiteType', 'date', 'shortTitle', 'url', 'accessDate', 'language', 'rights', 'extra'])
    ]

    many_to_many = [
        (models.ZoteroTypeField, models.ZoteroType, models.ZoteroField,
            zoterotype_fields, 'name', 'name',
            'zotero_type','zotero_field', 'rank')
    ]

    for many in many_to_many:
        table = many[0]
        assc1 = many[1]
        assc2 = many[2]
        for mapping in many[3]:
            query = { many[4]: mapping[0] }
            focus = assc1.query.filter_by( **query ).first()
            opts  = assc2.query.all()
            rel = [ o for o in opts if getattr(o, many[5]) in mapping[1] ]
            for r in rel:
                inst = table()
                setattr(inst, many[6],focus)
                setattr(inst, many[7],r)
                setattr(inst, many[8],mapping[1].index(getattr(r,many[5])))                
                db.session.add(inst)
            print( "{}:{} associated with {}:{}".format(
                assc1.__tablename__, mapping[0],
                assc2.__tablename__, mapping[1]) )
            db.session.commit()

def load_role_relationships():
    role_table = models.Role

    inverse_relationships = [
        ('Enslaved', 'Owner'),
        ('Bought', 'Buyer'),
        ('Sold', 'Seller'),
        ('Captured', 'Captor'),
        ('Emancipated', 'Owner'),
        ('Escaped', 'Owner'),
        ('Child', 'Mother'),
        ('Child', 'Father'),
        ('Spouse', 'Spouse')
    ]
    
    is_a_relationships = [
        ('Emancipated', 'Enslaved'),
        ('Inoculated', 'Enslaved'),
        ('Bought', 'Enslaved'),
        ('Sold', 'Enslaved'),
        ('Escaped', 'Enslaved'),
        ('Shipped', 'Enslaved'),
        ('Arrived', 'Enslaved'),
        ('Baptised', 'Enslaved'),
        ('Executed', 'Enslaved'),
        ('Mother', 'Parent'),
        ('Father', 'Parent'),
        ('Buyer', 'Owner'),
        ('Seller', 'Owner')
    ]