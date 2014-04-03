import re
import email.parser

class EmailParser(object):
    """
    A class for parsing emails from text into a set of common fields
    """

    def __init__(self):
        super(EmailParser, self).__init__()
        self.parser = email.parser.Parser()
        self.email_pattern = re.compile(r'([a-z0-9-]|\"(?!@\")*\")+@([a-z0-9-]+\.)+[a-z]+')

    def parse(self, text):
        eml = self.parser.parsestr(text)
        values = {}
        values["from"] = self.parse_from(eml["From"])
        values["subject"] = self.parse_subject(eml["Subject"])
        values["text"] = self.parse_text(eml)
        return values

    def parse_from(self, addr):
        """
        Parse the value of the From field as an email address

        Returns something like "somebody@somewhere.tld"
        """
        
        addr = addr.lower()
        
        if self.email_pattern.match(addr):
            return addr

        
        if re.search(r"<.*>", addr):
            start = addr.rfind("<")
            return addr[start+1:-1]

        raise Exception("Error parsing '%s' as an email address" % addr)

    def parse_subject(self, addr):
        """
        Parse the subject line, removing the [Reuse] tag
        """
        return re.sub(r"\s*\[reuse\]\s*", " ", addr, 0, re.IGNORECASE).strip()
        
    def parse_text(self, eml):
        """
        Parse the body of an email.message.Message object

        This is done by applying some reasonable heuristics, like
        "if an item is not multipart, return the entire body"
        """
        
        to_return = None
        
        payload = eml.get_payload()
        
        if not eml.is_multipart():
            return payload.strip()
        else:
            important_parts = [x for x in payload
                               if x.get_payload() and x["Content-Type"]]
            
            if len(payload) == 1:
                to_return = payload[0]
            elif all((x["Content-Type"].lower().startswith("text/plain")
                    for x in important_parts)):
                to_return = max((x for x in payload), key=lambda x:len(x.get_payload()))

        if to_return:
            if to_return["Content-Transfer-Encoding"] == "base64":
                return base64.decodestring(to_return.get_payload())
            else:
                return to_return.get_payload().strip()
        
        raise Exception("can't parse email")
