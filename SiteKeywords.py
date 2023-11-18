class SiteKeywords(object):
    def __init__(self):
        self.site_keywords = dict()

    def add_keywords_for_site(self, site, keywords):
        if site not in self.site_keywords:
            self.site_keywords[site] = []
        self.site_keywords[site].extend(keywords)

    def get_sites_for_keyword(self, keyword):
        sites = [site for site, keywords in self.site_keywords.items() if keyword in keywords]
        return sites
