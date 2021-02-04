file_name = 'singular_plural_verbs.txt'

verbs_singular = ["admires",
			   "approves",
			   "avoids",
			   "confuses",
			   "criticizes",
			   "discourages",
			   "encourages",
			   "engages",
			   "greets",
			   "inspires",
			   "knows",
			   "observes",
			   "remembers",
			   "stimulates",
			   "understands", "believes",
				  "says",
				  "thinks"]

verbs_plural = ["admire",
			 "approve",
			 "avoid",
			 "confuse",
			 "criticize",
			 "discourage",
			 "encourage",
			 "engage",
			 "greet",
			 "inspire",
			 "know",
			 "observe",
			 "remember",
			 "stimulate",
			 "understand", "believe",
				"say",
				"think"]


import itertools
with open(file_name, 'w') as f:
    for v1,v2 in itertools.izip_longest(verbs_singular,verbs_plural, fillvalue=''):
        f.write('%s\t%s\n' % (v1, v2))
