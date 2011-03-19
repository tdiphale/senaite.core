from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.ArchetypeTool import registerType
from Products.CMFCore import permissions
from Products.Five.browser import BrowserView
from Products.bika.browser.bika_folder_contents import BikaFolderContentsView
from Products.bika.config import PROJECTNAME
from Products.bika.content.bikaschema import BikaFolderSchema
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolder, ATFolderSchema
from Products.bika.interfaces.controlpanel import ISampleTypes
from zope.interface.declarations import implements

class SampleTypesView(BikaFolderContentsView):
    implements(IFolderContentsView)
    contentFilter = {'portal_type': 'SampleType'}
    content_add_buttons = {'Sample Type': "createObject?type_name=SampleType"}
    title = "Sample Types"
    description = ""
    show_editable_border = False
    batch = True
    b_size = 100
    full_objects = False
    columns = {
               'title_or_id': {'title': 'Title', 'icon':'sampletype.png'},
               'SampleTypeDescription': {'title': 'SampleTypeDescription'},
              }
    wflist_states = [
                    {'title_or_id': 'All', 'id':'all',
                     'columns': ['title_or_id', 'SampleTypeDescription'],
                     'buttons':[BikaFolderContentsView.default_buttons['delete']]},
                    ]

    def folderitems(self):
        items = BikaFolderContentsView.folderitems(self)
        for x in range(len(items)):
            # XXX some extra objects in items: {path: xxx}.  where from?  what are they?
            try: obj = items[x]['obj'].getObject()
            except KeyError: continue
            items[x]['SampleTypeDescription'] = obj.SampleTypeDescription()
            items[x]['links'] = {'title_or_id': items[x]['url'] + "/edit"}

        return items

schema = ATFolderSchema.copy()
class SampleTypes(ATFolder):
    implements(ISampleTypes)
    schema = schema
    displayContentsTab = False
schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(SampleTypes, PROJECTNAME)
