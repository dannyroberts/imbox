from imbox.imap import ImapTransport
from imbox.parser import parse_email
from imbox.query import build_search_query


class Session(object):

    def __init__(self, hostname, ssl=True):
        self.server = ImapTransport(hostname, ssl=ssl)
        self.connection = None

    def login(self, username, password):
        self.connection = self.server.connect(username, password)

    def logout(self):
        self.connection.logout()

    def _get_uids(self, **kwargs):
        query = build_search_query(**kwargs)

        message, data = self.connection.uid('search', None, query)
        return data[0].split()

    def fetch_by_uid(self, uid):
        message, data = self.connection.uid('fetch', uid, '(BODY.PEEK[])')
        raw_email = data[0][1]

        email_object = parse_email(raw_email)

        return email_object

    def mark_seen(self, uid):
        self.connection.uid('STORE', uid, '+FLAGS', '\\Seen')

    def delete(self, uid):
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
        self.connection.expunge()

    def copy(self, uid, destination_folder):
        return self.connection.uid('COPY', uid, destination_folder)

    def move(self, uid, destination_folder):
        if self.copy(uid, destination_folder):
            self.delete(uid)

    def messages(self, unread=False, sent_from=False, sent_to=False,
                 date__gt=False, date__lt=False, folder=False):

        if folder:
            self.connection.select(folder)

        uids = self._get_uids(
            unread=unread,
            sent_from=sent_from,
            sent_to=sent_to,
            date__gt=date__gt,
            date__lt=date__lt,
        )

        for uid in uids:
            yield (uid, self.fetch_by_uid(uid))
