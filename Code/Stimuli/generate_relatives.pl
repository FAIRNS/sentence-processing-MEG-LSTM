#!/usr/bin/perl -w

@nouns_singular=("aunt",
		 "boy",
		 "father",
		 "friend",
		 "girl",
		 "guy",
		 "kid",
		 "man",
		 "mother",
		 "uncle",
		 "woman");
@nouns_plural=("aunts",
	       "boys",
	       "fathers",
	       "friends",
	       "girls",
	       "guys",
	       "kids",
	       "men",
	       "mothers",
	       "uncles",
	       "women");
@verbs_singular=("admires",
		 "avoids",
		 "celebrates",
		 "confuses",
		 "criticizes",
		 "discourages",
		 "encourages",
		 "engages",
		 "fears",
		 "fights",
		 "greets",
		 "hates",
		 "helps",
		 "inspires",
		 "knows",
		 "likes",
		 "loves",
		 "meets",
		 "misses",
		 "mocks",
		 "observes",
		 "praises",
		 "remembers",
		 "respects",
		 "scares",
		 "stimulates",
		 "touches",
		 "understands",
		 "upsets",
		 "values",
		 "visits",
		 "welcomes");
@verbs_plural=("admire",
	       "avoid",
	       "celebrate",
	       "confuse",
	       "criticize",
	       "discourage",
	       "encourage",
	       "engage",
	       "fear",
	       "fight",
	       "greet",
	       "hate",
	       "help",
	       "inspire",
	       "know",
	       "like",
	       "love",
	       "meet",
	       "miss",
	       "mock",
	       "observe",
	       "praise",
	       "remember",
	       "respect",
	       "scare",
	       "stimulate",
	       "touch",
	       "understand",
	       "upset",
	       "value",
	       "visit",
	       "welcome");
@determiners_begin=("The",
		    "Some");
@determiners_inner=("the",
		    "some");
@adverbs=("probably",
	  "definitely");

$i=0;
while ($i<=$#nouns_singular) {
    $stem = $nouns_singular[$i];
    $stem_of{$nouns_singular[$i]} = $stem;
    $stem_of{$nouns_plural[$i]} = $stem;
    $i++;
}

$i=0;
while ($i<=$#verbs_singular) {
    $stem = $verbs_singular[$i];
    $stem_of{$verbs_singular[$i]} = $stem;
    $stem_of{$verbs_plural[$i]} = $stem;
    $i++;
}

# generating object relative clauses

# NP_i that NP_j V_j adv V_i and V_i

# NP_sing that NP_sing V_sing adv V_sing and V_sing

$type = "obj sing sing";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_singular) {
	foreach $inner_determiner (@determiners_inner) {
	    foreach $relative_noun (@nouns_singular) {
		if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
		    next;
		}
		foreach $relative_verb (@verbs_singular) {
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_singular) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_singular) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $inner_determiner,
						 $relative_noun,
						 $relative_verb,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}

# NP_plur that NP_plur V_plur adv V_plur and V_plur

$type = "obj plur plur";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_plural) {
	foreach $inner_determiner (@determiners_inner) {
	    foreach $relative_noun (@nouns_plural) {
		if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
		    next;
		}
		foreach $relative_verb (@verbs_plural) {
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_plural) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_plural) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $inner_determiner,
						 $relative_noun,
						 $relative_verb,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}

# NP_sing that NP_plur V_plur adv V_sing and V_sing

$type = "obj sing plur";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_singular) {
	foreach $inner_determiner (@determiners_inner) {
	    foreach $relative_noun (@nouns_plural) {
		if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
		    next;
		}
		foreach $relative_verb (@verbs_plural) {
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_singular) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_singular) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $inner_determiner,
						 $relative_noun,
						 $relative_verb,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}

# NP_plur that NP_sing V_sing adv V_plur and V_plur

$type = "obj plur sing";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_plural) {
	foreach $inner_determiner (@determiners_inner) {
	    foreach $relative_noun (@nouns_singular) {
		if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
		    next;
		}
		foreach $relative_verb (@verbs_singular) {
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_plural) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_plural) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $inner_determiner,
						 $relative_noun,
						 $relative_verb,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}


# generating subject relative clauses

# NP_i that V_i NP_j adv V_i and V_i

# NP_sing that V_sing NP_sing adv V_sing and V_sing

$type = "subj sing sing";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_singular) {
	foreach $relative_verb (@verbs_singular) {
	    foreach $inner_determiner (@determiners_inner) {
		foreach $relative_noun (@nouns_singular) {
		    if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
			next;
		    }
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_singular) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_singular) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $relative_verb,
						 $inner_determiner,
						 $relative_noun,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}

# NP_sing that V_sing NP_plur adv V_sing and V_sing

$type = "subj sing plur";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_singular) {
	foreach $relative_verb (@verbs_singular) {
	    foreach $inner_determiner (@determiners_inner) {
		foreach $relative_noun (@nouns_plural) {
		    if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
			next;
		    }
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_singular) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_singular) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $relative_verb,
						 $inner_determiner,
						 $relative_noun,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}

# NP_plur that V_plur NP_sing adv V_plur and V_plur

$type = "subj plur sing";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_plural) {
	foreach $relative_verb (@verbs_plural) {
	    foreach $inner_determiner (@determiners_inner) {
		foreach $relative_noun (@nouns_singular) {
		    if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
			next;
		    }
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_plural) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_plural) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $relative_verb,
						 $inner_determiner,
						 $relative_noun,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}

# NP_plur that V_plur NP_plur adv V_plur and V_plur

$type = "subj plur plur";

foreach $initial_determiner (@determiners_begin) {
    foreach $main_noun (@nouns_plural) {
	foreach $relative_verb (@verbs_plural) {
	    foreach $inner_determiner (@determiners_inner) {
		foreach $relative_noun (@nouns_plural) {
		    if ($stem_of{$relative_noun} eq $stem_of{$main_noun}) {
			next;
		    }
		    foreach $adverb (@adverbs) {
			foreach $main_verb_1 (@verbs_plural) {
			    if ($stem_of{$relative_verb} eq $stem_of{$main_verb_1}) {
				next;
			    }
			    foreach $main_verb_2 (@verbs_plural) {
				if ($stem_of{$relative_verb} eq $stem_of{$main_verb_2} ||
				    $stem_of{$main_verb_1} eq $stem_of{$main_verb_2}) {
				    next;
				}
				print join (" ",($type,
						 $initial_determiner,
						 $main_noun,
						 "that",
						 $relative_verb,
						 $inner_determiner,
						 $relative_noun,
						 $adverb,
						 $main_verb_1,
						 "and",
						 $main_verb_2)
				    ),"\n";
			    }
			}
		    }
		}
	    }
	}
    }
}
