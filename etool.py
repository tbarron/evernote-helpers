"""
etool - Evernote manipulations

Usage:
    etool create_notebook [-d] NAME
    etool get_token [-d]
    etool list_notebooks [-d]
    etool list_notes [-d]
"""
from ConfigParser import ConfigParser
from docopt_dispatch import dispatch
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.types as NSTypes
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.api.client import EvernoteClient
import pdb
import sys
import time


# -----------------------------------------------------------------------------
@dispatch.on('create_notebook')
def et_create_notebook(**kwa):
    """
    Create a notebook if it does not exist
    """
    if kwa['d']:
        pdb.set_trace()
    nb_desc = NSTypes.Notebook(name=kwa['NAME'])


# -----------------------------------------------------------------------------
@dispatch.on('list_notes')
def et_list_notes(**kwa):
    """
    Can we get a list of notes?
    """
    if kwa['d']:
        pdb.set_trace()
    client = get_authorized_client('full')
    note_store = client.get_note_store()
    flt = NoteFilter(words="")
    spec = NotesMetadataResultSpec(includeTitle=True)
    md_list = note_store.findNotesMetadata(flt, 0, 250, spec)

    for note in md_list.notes:
        print(note.title)
        print("   {}".format(note.guid))

    
# -----------------------------------------------------------------------------
@dispatch.on('list_notebooks')
def et_list_notebooks(**kwa):
    """
    See what we can learn about notebooks
    """
    if kwa['d']:
        pdb.set_trace()
    client = get_authorized_client()
    note_store = client.get_note_store()
    nb_list = note_store.listNotebooks()
    for nb in nb_list:
        print("Name: {}".format(nb.name))
        print("    GUID: {}".format(nb.guid))
        print("    default = {}".format(nb.defaultNotebook))
        print("    service created: {}".format(ymdhms(nb.serviceCreated / 1000)))
        print("    service updated: {}".format(ymdhms(nb.serviceUpdated / 1000)))
        print("    in this notebook, you can:")
        rst = nb.restrictions
        for item in dir(rst):
            if item.startswith('no'):
                action = item.replace('no', '')
                if getattr(rst, item):
                    permission = "no"
                else:
                    permission = "yes"
                print("        {}: {}".format(action, permission))


# -----------------------------------------------------------------------------
@dispatch.on('get_token')
def et_get_token(**kwa):
    """
    This will re-authorize pyenote for access to my sandbox account
    """
    if kwa['d']:
        pdb.set_trace()
    ##
    # Create an instance of EvernoteClient using your API
    # key (consumer key and consumer secret)
    ##
    (key, secret) = get_consumer('full')
    client = EvernoteClient(
        consumer_key = key,
        consumer_secret = secret,
        sandbox = True
        )

    ##
    # Provide the URL where the Evernote Cloud API should 
    # redirect the user after the request token has been
    # generated. In this example, localhost is used; note
    # that in this example, we're copying the URLs manually
    # and that, in production, this URL will need to 
    # automatically parse the response and send the user
    # to the next step in the flow.
    ##
    request_token = client.get_request_token('http://integrel.org')

    ##
    # Prompt the user to open the request URL in their browser
    ##
    print "Paste this URL in your browser and login"
    print
    print '\t'+client.get_authorize_url(request_token)
    print
    print '-------'

    ##
    # Have the user paste the resulting URL so we can pull it
    # apart
    ##
    print "Paste the URL after login here:"
    authurl = raw_input()

    ##
    # Parse the URL to get the OAuth verifier
    ##
    vals = parse_query_string(authurl)

    ##
    # Use the OAuth verifier and the values from request_token
    # to built the request for our authentication token, then
    # ask for it.
    ##
    auth_token = client.get_access_token(
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        vals['oauth_verifier']
        )

    print "Your auth token is: {}".format(auth_token)
    

# -----------------------------------------------------------------------------
def ymdhms(when):
    """
    Return epoch time *when* in format yyyy.mmdd HH:MM:SS
    """
    return time.strftime("%Y.%m%d %H:%M:%S", time.localtime(when))


# -----------------------------------------------------------------------------
def get_auth_token(access_level=None):
    """
    Look up and return the auth token from the 'cred' file
    """
    if access_level is None:
        access_level = 'basic'
    if not hasattr(get_auth_token, 'token'):
        cfg = ConfigParser()
        cfg.read('cred')
        token = cfg.get(access_level, 'token')
        if 5 < len(token):
            get_auth_token.token = token
        else:
            sys.exit("Could not find the auth token")
    return get_auth_token.token    
    
    
# -----------------------------------------------------------------------------
def get_authorized_client(access_level=None):
    """
    Look up the auth token in file 'cred' and use it to get a valid authorized
    evernote client. If successful, return the client, otherwise exit with an
    error message.
    """
    if access_level is None:
        access_level = 'basic'
    client = None
    auth_token = get_auth_token(access_level)
    client = EvernoteClient(token=auth_token)
    if client:
        return client
    else:
        sys.exit("Auth failed. Maybe we need to renew the auth token?")
    

# -----------------------------------------------------------------------------
def get_consumer(access_level):
    """
    Look up and return a consumer key and secret from the 'cred' file.
    *access_level* should be 'full' or 'basic'.
    """
    cfg = ConfigParser()
    cfg.read('cred')
    return(cfg.get(access_level, 'key'), cfg.get(access_level, 'secret'))

    
# -----------------------------------------------------------------------------
def parse_query_string(authorize_url):
    uargs = authorize_url.split('?')
    vals = {}
    if len(uargs) == 1:
        raise Exception('Invalid Authorization URL')
    for pair in uargs[1].split('&'):
        key, value = pair.split('=', 1)
        vals[key] = value
    return vals


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    dispatch(__doc__)
