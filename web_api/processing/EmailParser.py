import re
import base64
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
        text = self.parse_text(eml)
        text = self.strip_reply(text)
        values["text"] = self.strip_signature(text)
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
            return addr[start + 1:-1]

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

    def strip_reply(self, text):
        """
        Return a copy of `text` with any reply portion removed
        
        If there is no reply in text, then it is returned unchanged.
        """
        lines = text.split("\n")
        
        
        start_reply_lines = [index for index, line in
                             reversed(list(enumerate(lines)))
                        if self.start_reply_line_matches(line)]
        
        # Try matching the carrot-indented lines method (> replyReplyreply)
        carrot_lines = [index for index, line in enumerate(lines)
                        if line.startswith(">")]
        
        carrot_blocks = [block for block, has_carrot in
                         self.find_blocks(lines, lambda x: x.startswith(">"))
                         if has_carrot]
        
        # If both are present, then they are probably correlated
        if start_reply_lines and carrot_lines:
            # Remove nested reply start lines
            start_reply_lines = [x for x in start_reply_lines
                                 if not x in carrot_lines]
            
            valid_start_lines = [(i, y) for i in start_reply_lines
                                 for x, y in carrot_blocks
                                 if 0 < x - i <= 2]
            
            keep_lines = range(len(lines))
            
            for reply_block in valid_start_lines:
                for x in range(reply_block[0], reply_block[1]+1):
                    keep_lines.remove(x)
            
            lines = [line for index, line in enumerate(lines)
                     if index in keep_lines]
            
            return self.strip_reply("\n".join(lines))
        
        elif carrot_lines:
            keep_lines = range(len(lines))
            
            for reply_block in carrot_blocks:
                for x in range(reply_block[0], reply_block[1]+1):
                    keep_lines.remove(x)
            
            lines = [line for index, line in enumerate(lines)
                     if index in keep_lines]
            
            return self.strip_reply("\n".join(lines))
        
        elif start_reply_lines:
            keep_lines = range(len(lines))
            
            lines = [line for index, line in enumerate(lines)
                     if index < start_reply_lines[-1]]
            
            return self.strip_reply("\n".join(lines))
        
        return "\n".join(lines).strip()
        
    def strip_signature(self, text):
        lines = text.split("\n")
        
        
        special_char_lines = [i for i,line in enumerate(lines)
                         if re.match(r"[-_*=~]{2,}\s*$", line)]
        
        if special_char_lines:
            lines = lines[:special_char_lines[-1]]
            return self.strip_signature("\n".join(lines))
        
        # Now try some probabilistic matching
        score = 0
        
        text_blocks = [block for block, key in 
                       self.find_blocks(lines,
                                    lambda x: False if re.match("\s*$", x)
                                    else True)
                       if key]
        
        if not text_blocks:
            return text.strip()
        
        last_block = text_blocks[-1]
        last_lines = lines[last_block[0]: last_block[1]+1]
        words = []
        
        for line in last_lines:
            words.extend(line.split())
            
        alpha = [word.isalpha() for word in words]
        if alpha:
            capital_words_percent = (sum(word.istitle() for word in words)
                                       / float(len(alpha)))
            score += capital_words_percent
            
        rules = set(["phone", "room", "MIT", "city", "zip"])
        for line in last_lines:
            if "phone" in rules and re.search(r"\d{10,11}|\d{7}",
                                              re.sub(r"- \(\)", "", line)):
                score += 1
                rules.remove("phone")
                
            if "room" in rules and re.search(r"\d+-[GD]?\d{,3}", line):
                score += 1
                rules.remove("room")
            
            if "MIT" in rules and ("Institute" in line or "MIT" in line):
                score += 1.5
                rules.remove("MIT")
            
            if "city" in rules and "Cambridge" in line:
                score += 1
                rules.remove("city")
            
            if "zip" in rules and "02139" in line:
                score += 0.5
                rules.remove("zip")
                
            if not rules: break
        
        if score > 3:
            return self.strip_reply("\n".join(lines[:last_block[0]]
                                              + lines[last_block[1]+1:]))

        return text.strip()
    
    # Try matching the "On DAY, MON dd, ..." or "--Original Message--"
    # reply indicators
    def start_reply_line_matches(self, line):
        if line.startswith("On"): 
            # Require a year
            if not re.search(r"\d{4}", line):
                return False
            
            # Require a date
            if not re.search(r"\d{1,2}", line):
                return False
            return True
        
        if re.search(r"original message", line, re.IGNORECASE):
            return True
        
        return False
    
    def find_blocks(self, to_search, key_fn):
        found = None
        for index, value in enumerate(to_search):
            key = key_fn(value)
            if not found:
                found = ((index, index), key)
            if found[1] != key:
                yield found
                found = ((index, index), key)
            else:
                found = ((found[0][0], index), key)
        
        yield found
                    
