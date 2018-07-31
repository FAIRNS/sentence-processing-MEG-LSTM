#!/usr/bin/perl -w

# This script generate N random sentences for each possible
# combination of singular and plural assignments to a list of
# templates. When the "complete" flag is set to 1, the script
# generates full sentences (up to and including the object of the main
# verb, if the latter is transitive).

# The script is used as follows:

# ./generate_relatives.pl COMPLETE_FLAG N template1 (template2 ...)

# For example:

# ./generate_relatives.pl 0 1 simple objrel objrel_that

# generates 2 simple sentences, 4 sentences with an object relative
# with that-deletion and 4 sentences with an object relative with
# overt that (all up to the main verb, since the COMPLETE_FLAG is set
# to 0). The simple construction when generated without an object
# contains only one element that can independently select a number
# (the subject noun, that determines the noun of the verb), which
# leads to generating two sentenced varying in the subject number
# feature . The other constructions contain two elements that can
# independently take singular or plural form (e.g., in the case of
# objrel: "the SUBJ_main the SUBJ_rel likes admires", the number of
# the subject and object are independent), and consequently feature 4
# possible combinations of number assignments (singular/singular,
# singular/plural, plural/singular, plural/plural). Note that the
# following command would generate 60 sentences:

# ./generate_relatives.pl 0 5 simple objrel objrel_that

# Overall, given N, N*F sentences will be generated, where F is the
# number of possible combinations of independent features for each
# target construction.

# IMPORTANT: In the interest of time, this script in the current
# version does not support "complete" versions of all constructions
# and the flag will be ignored: your mileage might vary.

# These are the possible templates, each illustrated with an example
# for the case when the COMPLETE_FLAG is set to 0 (sentence stops at
# the main clause).

# simple: The carpenter admires
# conjunction: The carpenter admires and encourages 
# objrel: The carpenter the women admire encourages
# objrel_that: The carpenter that the women admire encourages
# subjrel_that: The carpenter that admires the women encourages
# double_subjrel_that: The carpenter that admires the women that greet the girl encourages
# simple_adv: The carpenter definitely admires the women
# objrel_adv: The carpenter the women admire definitely encourages
# objrel_that_adv: The carpenter that the women admire definitely encourages
# subjrel_that_adv: the carpenter that admires the women definitely encourages
# frame_simple: The girl believes the carpenter admires the women
# frame_objrel: The girl believes the carpenter the women admire encourages
# frame_objrel_that: The girl believes the carpenter that the women admire encourages
# frame_subjrel_that: The girl believes the carpenter that admires the women encourages
# frame_simple_adv: The girl believes the carpenter definitely admires the women
# frame_objrel_adv: The girl believes the carpenter the women admire definitely encourages
# frame_objrel_that_adv: The girl believes the carpenter that the women admire definitely encourages
# frame_subjrel_that_adv: The girl believes the carpenter that admires the women definitely encourages
# frame_that_simple: The girl believes that the carpenter admires the women
# frame_that_objrel: The girl believes that the carpenter the women admire encourages
# frame_that_objrel_that: The girl believes that the carpenter that the women admire encourages
# frame_that_subjrel_that: The girl believes that the carpenter that admires the women encourages
# frame_that_simple_adv: The girl believes that the carpenter definitely admires the women
# frame_that_objrel_adv: The girl believes that the carpenter the women admire definitely encourages
# frame_that_objrel_that_adv: The girl believes that the carpenter that the women admire definitely encourages
# frame_that_subjrel_that_adv: The girl believes that the carpenter that admires the women definitely encourages

# NB: for the time being, conjunction and double_subjrel_that do not
# support the frame_* and *_adv contexts!

# Note that the printed sentences are made of randomly picked
# elements, and that they are unique.  Moreover, no noun or verb lemma
# occurs more than once in the same sentence. If N is larger than the
# maximum number of distinct sentences that can be generated
# respecting these constraints, the script will run forever (and I
# can't be bothered checking for that, sorry).

# Sentences and supporting information are printed one-per-line, in
# the following tab-delimited format:

# template sentence number1 number2 (number3 (number4)?)? alternate1 (alternate2 (alternate3)?)?

# where the template is from the list above, the words in the sentence
# are space-delimited, numberX is the number (singular/plural) of the
# nth element in the sentence whose number does not depend on a
# previous element, and alternateX is the alternate form for any verb
# in the sentence (singular for plurals, and vice versa).

# For example, for a (complete) frame_simple sentence, the output would
# look as follows:

# frame_simple	The poets believe the farmers admire the singer	plural	plural	singular	believes	admires

# where the first "plural" refer to "poets" (and "believe"), the
# second to "farmers" (and "admire") and "singular" refers to
# "singer".

# Keep in mind that the printed number information changes from
# template to template. For example, the third number ("singular")
# refers to the final object noun in the example above, but to the
# relative subject (and verb) in the 0-complete sentence below:

# frame_objrel_that	The boys believe the poets that the farmer knows avoid	plural	plural	singular	believes	know	avoids

# Note also in this example featuring a long-distance dependency that
# the second number code ("plural") applies to "poets" and "avoid",
# where the latter actually occurs after the words instantiating the
# third number code ("singular": "farmer" and "knows").

@{$nouns{"singular"}}=("athlete",
		       "aunt",
		       "boy",
		       "carpenter",
		       "doctor",
		       "farmer",
		       "father",
		       "friend",
		       "girl",
		       "guy",
		       "kid",
		       "lawyer",
		       "man",
		       "mother",
		       "poet",
		       "singer",
		       "teacher",
		       "uncle",
		       "victim",
		       "woman");
@{$nouns{"plural"}}=("athletes",
		     "aunts",
		     "boys",
		     "carpenters",
		     "doctors",
		     "farmers",
		     "fathers",
		     "friends",
		     "girls",
		     "guys",
		     "kids",
		     "lawyers",
		     "men",
		     "mothers",
		     "poets",
		     "singers",
		     "teachers",
		     "uncles",
		     "victims",
		     "women");
@{$verbs{"singular"}}=("admires",
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
		       "understands");
@{$verbs{"plural"}}=("admire",
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
		     "understand");
@{$matrix_verbs{"singular"}}=("believes",
			      "says",
			      "thinks");
@{$matrix_verbs{"plural"}}=("believe",
			    "say",
			    "think");
@determiners_begin=("The");
@determiners_inner=("the");
@adverbs=("probably",
	  "definitely",
          "certainly");

$i=0;
while ($i<=$#{$nouns{"singular"}}) {
    $stem = $nouns{"singular"}[$i];
    $stem_of{$nouns{"singular"}[$i]} = $stem;
    $stem_of{$nouns{"plural"}[$i]} = $stem;
    $i++;
}

$i=0;
while ($i<=$#{$verbs{"singular"}}) {
    $stem = $verbs{"singular"}[$i];
    $stem_of{$verbs{"singular"}[$i]} = $stem;
    $stem_of{$verbs{"plural"}[$i]} = $stem;
    $i++;
}

sub other_number {
    my $correct_number = shift;
    if ($correct_number eq "singular") {
	return "plural";
    }
    else {
	return "singular";
    }
}

sub generate_simple {
    my $complete_flag = shift;
    my $number_subj = shift;
    my $number_obj = shift;
    my $adv = shift;
    my $embedded = shift;
    my $other_number_subj = other_number($number_subj);
    
    # pick random begin det
    if ($embedded) {
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
    }
    else {
	push @words,$determiners_begin[int(rand(scalar(@determiners_begin)))];
    }
    # pick random subj noun with stem not in bucket, add stem to bucket
    while (1) {
    	my $noun = $nouns{$number_subj}[int(rand(scalar(@{$nouns{$number_subj}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # if requested, produce adverb
    if ($adv) {
	push @words,$adverbs[int(rand(scalar(@adverbs)))];
    }
    # pick random verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number_subj}})));
    	my $verb = $verbs{$number_subj}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
	    push @alternates,$verbs{$other_number_subj}[$random_index];
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
    # if requested, complete sentence
    if ($complete_flag) {
	# determiner for object
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
	# pick random obj noun with stem not in bucket, add stem to bucket
	while (1) {
	    my $noun = $nouns{$number_obj}[int(rand(scalar(@{$nouns{$number_obj}})))];
	    if (!defined($seen_bucket{$stem_of{$noun}})) {
		push @words,$noun;
		$seen_bucket{$stem_of{$noun}} = 1;
		last;
	    }
	}
    }
}


sub generate_conjunction {
    my $number = shift;
    my $adv = shift;
    my $embedded = shift;
    my $other_number = other_number($number);
    
    # pick random begin det
    if ($embedded) {
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
    }
    else {
	push @words,$determiners_begin[int(rand(scalar(@determiners_begin)))];
    }
    # pick random subj noun with stem not in bucket, add stem to bucket
    while (1) {
    	my $noun = $nouns{$number}[int(rand(scalar(@{$nouns{$number}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # if requested, produce adverb
    if ($adv) {
	push @words,$adverbs[int(rand(scalar(@adverbs)))];
    }
    # pick random first verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number}})));
    	my $verb = $verbs{$number}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
    # and
    push @words,"and";
    # pick random first verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number}})));
    	my $verb = $verbs{$number}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
	    push @alternates,$verbs{$other_number}[$random_index];
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
}

sub generate_matrix {
    my $number = shift;
    my $that = shift;
    my $other_number = other_number($number);

    # pick random begin det
    push @words,$determiners_begin[int(rand(scalar(@determiners_begin)))];

    # pick random noun not in bucket, add to bucket
    while (1) {
    	my $noun = $nouns{$number}[int(rand(scalar(@{$nouns{$number}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # pick random matrixverb
    my $random_index = int(rand(scalar(@{$matrix_verbs{$number}})));
    my $verb = $matrix_verbs{$number}[$random_index];
    push @words,$verb;
    push @alternates,$matrix_verbs{$other_number}[$random_index];

    # if that, add that
    if ($that) {
	push @words,"that";
    }
}

# BACKUP, DELETE AFTER DEBUGGING
# sub generate_subj_rel {
#     my $complete_flag = shift;
#     my $number_main_subj = shift;
#     my $number_rel_obj = shift;
#     my $number_main_obj = shift;
#     my $adv = shift;
#     my $embedded = shift;
#     my $other_number_main_subj = other_number($number_main_obj);

#     # pick random begin det
#     if ($embedded) {
# 	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
#     }
#     else {
# 	push @words,$determiners_begin[int(rand(scalar(@determiners_begin)))];
#     }

#     # pick random main subj noun with stem not in bucket, add stem to bucket
#     while (1) {
#     	my $noun = $nouns{$number_main_subj}[int(rand(scalar(@{$nouns{$number_main_subj}})))];
#     	if (!defined($seen_bucket{$stem_of{$noun}})) {
#     	    push @words,$noun;
#     	    $seen_bucket{$stem_of{$noun}} = 1;
#     	    last;
#     	}
#     }
#     # that is mandatory in subject relatives
#     push @words,"that";
#     # pick random verb not in bucket, add to bucket
#     while (1) {
# 	my $random_index = int(rand(scalar(@{$verbs{$number_main_subj}})));
#     	my $verb = $verbs{$number_main_subj}[$random_index];
#     	if (!defined($seen_bucket{$stem_of{$verb}})) {
#     	    push @words,$verb;
# 	    push @alternates,$verbs{$other_number_main_subj}[$random_index];
#     	    $seen_bucket{$stem_of{$verb}} = 1;
#     	    last;
#     	}
#     }
#     # determiner for object
#     push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
#     # pick random obj noun with stem not in bucket, add stem to bucket
#     while (1) {
#     	my $noun = $nouns{$number_rel_obj}[int(rand(scalar(@{$nouns{$number_rel_obj}})))];
#     	if (!defined($seen_bucket{$stem_of{$noun}})) {
#     	    push @words,$noun;
#     	    $seen_bucket{$stem_of{$noun}} = 1;
#     	    last;
#     	}
#     }
#     # if requested, produce adverb
#     if ($adv) {
# 	push @words,$adverbs[int(rand(scalar(@adverbs)))];
#     }
#     # pick random main verb not in bucket, add to bucket
#     while (1) {
# 	my $random_index = int(rand(scalar(@{$verbs{$number_main_subj}})));
#     	my $verb = $verbs{$number_main_subj}[$random_index];
#     	if (!defined($seen_bucket{$stem_of{$verb}})) {
#     	    push @words,$verb;
# 	    push @alternates,$verbs{$other_number_main_subj}[$random_index];
#     	    $seen_bucket{$stem_of{$verb}} = 1;
#     	    last;
#     	}
#     }
#     if ($complete_flag) {
# 	# determiner for object
# 	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
# 	# pick random obj noun with stem not in bucket, add stem to bucket
# 	while (1) {
# 	    my $noun = $nouns{$number_main_obj}[int(rand(scalar(@{$nouns{$number_main_obj}})))];
# 	    if (!defined($seen_bucket{$stem_of{$noun}})) {
# 		push @words,$noun;
# 		$seen_bucket{$stem_of{$noun}} = 1;
# 		last;
# 	    }
# 	}
#     }
# }

sub generate_subj_rel {
    my $complete_flag = shift;
    my $number_main_subj = shift;
    my $number_outer_rel_obj = shift;
    my $number_inner_rel_obj = shift;
    my $number_main_obj = shift;
    my $adv = shift;
    my $embedded = shift;
    my $other_number_main_subj = other_number($number_main_subj);
    my $other_number_outer_rel_obj = other_number($number_outer_rel_obj);
    my $double_flag = 1;
    if ($number_inner_rel_obj eq "NONE") {
	undef($double_flag);
    }
    
    # pick random begin det
    if ($embedded) {
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
    }
    else {
	push @words,$determiners_begin[int(rand(scalar(@determiners_begin)))];
    }

    # pick random main subj noun with stem not in bucket, add stem to bucket
    while (1) {
    	my $noun = $nouns{$number_main_subj}[int(rand(scalar(@{$nouns{$number_main_subj}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # that is mandatory in subject relatives
    push @words,"that";
    # pick random verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number_main_subj}})));
    	my $verb = $verbs{$number_main_subj}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
	    push @alternates,$verbs{$other_number_main_subj}[$random_index];
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
    # determiner for object
    push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
    # pick random obj noun with stem not in bucket, add stem to bucket
    while (1) {
    	my $noun = $nouns{$number_outer_rel_obj}[int(rand(scalar(@{$nouns{$number_outer_rel_obj}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # if this is a double relative, produce another embedded relative depending on the outer relative object
    if ($double_flag) {
	# that is mandatory in subject relatives
	push @words,"that";
	# pick random verb not in bucket, add to bucket
	while (1) {
	    my $random_index = int(rand(scalar(@{$verbs{$number_outer_rel_obj}})));
	    my $verb = $verbs{$number_outer_rel_obj}[$random_index];
	    if (!defined($seen_bucket{$stem_of{$verb}})) {
		push @words,$verb;
		push @alternates,$verbs{$other_number_outer_rel_obj}[$random_index];
		$seen_bucket{$stem_of{$verb}} = 1;
		last;
	    }
	}
	# determiner for object
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
	# pick random obj noun with stem not in bucket, add stem to bucket
	while (1) {
	    my $noun = $nouns{$number_inner_rel_obj}[int(rand(scalar(@{$nouns{$number_inner_rel_obj}})))];
	    if (!defined($seen_bucket{$stem_of{$noun}})) {
		push @words,$noun;
		$seen_bucket{$stem_of{$noun}} = 1;
		last;
	    }
	}
    }
    
    # if requested, produce adverb
    if ($adv) {
	push @words,$adverbs[int(rand(scalar(@adverbs)))];
    }
    # pick random main verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number_main_subj}})));
    	my $verb = $verbs{$number_main_subj}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
	    push @alternates,$verbs{$other_number_main_subj}[$random_index];
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
    if ($complete_flag) {
	# determiner for object
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
	# pick random obj noun with stem not in bucket, add stem to bucket
	while (1) {
	    my $noun = $nouns{$number_main_obj}[int(rand(scalar(@{$nouns{$number_main_obj}})))];
	    if (!defined($seen_bucket{$stem_of{$noun}})) {
		push @words,$noun;
		$seen_bucket{$stem_of{$noun}} = 1;
		last;
	    }
	}
    }
}

sub generate_obj_rel {
    my $complete_flag = shift;
    my $number_main_subj = shift;
    my $number_rel_subj = shift;
    my $number_main_obj = shift;
    my $that = shift;
    my $adv = shift;
    my $embedded = shift;
    my $other_number_main_subj = other_number($number_main_subj);
    my $other_number_rel_subj = other_number($number_rel_subj);
    
    # pick random begin det
    if ($embedded) {
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
    }
    else {
	push @words,$determiners_begin[int(rand(scalar(@determiners_begin)))];
    }

    # pick random main subj noun with stem not in bucket, add stem to bucket
    while (1) {
    	my $noun = $nouns{$number_main_subj}[int(rand(scalar(@{$nouns{$number_main_subj}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # add that if requested
    if ($that) {
	push @words,"that";
    }
    # determiner for rel noun
    push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
    # pick random rel subj noun with stem not in bucket, add stem to bucket
    while (1) {
    	my $noun = $nouns{$number_rel_subj}[int(rand(scalar(@{$nouns{$number_rel_subj}})))];
    	if (!defined($seen_bucket{$stem_of{$noun}})) {
    	    push @words,$noun;
    	    $seen_bucket{$stem_of{$noun}} = 1;
    	    last;
    	}
    }
    # pick random rel verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number_rel_subj}})));
    	my $verb = $verbs{$number_rel_subj}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
	    push @alternates,$verbs{$other_number_rel_subj}[$random_index];
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
    # if requested, produce adverb
    if ($adv) {
	push @words,$adverbs[int(rand(scalar(@adverbs)))];
    }
    # pick random main verb not in bucket, add to bucket
    while (1) {
	my $random_index = int(rand(scalar(@{$verbs{$number_main_subj}})));
    	my $verb = $verbs{$number_main_subj}[$random_index];
    	if (!defined($seen_bucket{$stem_of{$verb}})) {
    	    push @words,$verb;
	    push @alternates,$verbs{$other_number_main_subj}[$random_index];
    	    $seen_bucket{$stem_of{$verb}} = 1;
    	    last;
    	}
    }
    # if we asked for complete sentence, add main sentence object
    # determiner for noun
    if ($complete_flag) {
	push @words,$determiners_inner[int(rand(scalar(@determiners_inner)))];
	# pick random main obj noun with stem not in bucket, add stem to bucket
	while (1) {
	    my $noun = $nouns{$number_main_obj}[int(rand(scalar(@{$nouns{$number_main_obj}})))];
	    if (!defined($seen_bucket{$stem_of{$noun}})) {
		push @words,$noun;
		$seen_bucket{$stem_of{$noun}} = 1;
		last;
	    }
	}
    }
}


### MAIN ###

$complete_flag = shift;
$sentence_count = shift;

while ($structure = shift) {
    $requested_structures{$structure} = 1;
}

for $structure (sort (keys %requested_structures)) {
    if ($structure eq "simple") {
	my $adv = 0;
	my $embedded = 0;
	foreach my $number_subj ("singular","plural") {
	    if ($complete_flag) {
		@numbers_obj = ("singular","plural");
	    }
	    else {
		@numbers_obj = ("singular"); # dummy!
	    }
	    foreach my $number_obj (@numbers_obj) {
		%sentences = ();
		while (scalar(keys (%sentences)) < $sentence_count) {
		    @words = ();
		    @alternates = ();
		    %seen_bucket = ();
		    generate_simple($complete_flag,$number_subj,$number_obj,$adv,$embedded);
		    if ($complete_flag) {
			$sentences{join ("\t",($structure, join(" ",@words), $number_subj, $number_obj, @alternates))} = 1;
		    }
		    else {
			$sentences{join ("\t",($structure, join(" ",@words), $number_subj, @alternates))} = 1;
		    }
		}
		foreach $sentence (sort (keys(%sentences))) {
		    print $sentence,"\n";
		}
	    }
	}
    }
    elsif ($structure eq "conjunction") {
	my $adv = 0;
	my $embedded = 0;
	foreach my $number ("singular","plural") {
	    %sentences = ();
	    while (scalar(keys (%sentences)) < $sentence_count) {
		@words = ();
		@alternates = ();
		%seen_bucket = ();
		generate_conjunction($number,$adv,$embedded);
		$sentences{join ("\t",($structure, join(" ",@words), $number, @alternates))} = 1;
	    }
	    foreach $sentence (sort (keys(%sentences))) {
		print $sentence,"\n";
	    }
	}
    }
    elsif ($structure eq "objrel") {
	my $that = 0;
	my $adv = 0;
	my $embedded = 0;
	foreach my $number_main_subj ("singular","plural") {
	    foreach my $number_rel_subj ("singular","plural") {
		if ($complete_flag) {
		    @numbers_main_obj = ("singular","plural");
		}
		else {
		    @numbers_main_obj = ("singular"); # dummy!
		}
		foreach my $number_main_obj (@numbers_main_obj) {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_obj_rel($complete_flag,$number_main_subj,$number_rel_subj,$number_main_obj,$that,$adv,$embedded);
			if ($complete_flag) {
			    $sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_rel_subj, $number_main_obj,@alternates))} = 1;
			}
			else{
			    $sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_rel_subj, @alternates))} = 1;
			}
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "objrel_that") {
	my $that = 1;
	my $adv = 0;
	my $embedded = 0;
	foreach my $number_main_subj ("singular","plural") {
	    foreach my $number_rel_subj ("singular","plural") {
		if ($complete_flag) {
		    @numbers_main_obj = ("singular","plural");
		}
		else {
		    @numbers_main_obj = ("singular"); # dummy!
		}
		foreach my $number_main_obj (@numbers_main_obj) {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_obj_rel($complete_flag,$number_main_subj,$number_rel_subj,$number_main_obj,$that,$adv,$embedded);
			if ($complete_flag) {
			    $sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_rel_subj, $number_main_obj,@alternates))} = 1;
			}
			else{
			    $sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_rel_subj, @alternates))} = 1;
			}
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "subjrel_that") {
	my $adv = 0;
	my $embedded = 0;
	my $dummy_number_inner_rel_obj = "NONE"; # this would be used for double relatives
	foreach my $number_main_subj ("singular","plural") {
	    foreach my $number_rel_obj ("singular","plural") {
		if ($complete_flag) {
		    @numbers_main_obj = ("singular","plural");
		}
		else {
		    @numbers_main_obj = ("singular"); # dummy!
		}
		foreach my $number_main_obj (@numbers_main_obj) {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_subj_rel($complete_flag,$number_main_subj,$number_rel_obj, $dummy_number_inner_rel_obj,$number_main_obj,$adv,$embedded);
			if ($complete_flag) {
			    $sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_rel_obj, $number_main_obj,@alternates))} = 1;
			}
			else{
			    $sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_rel_obj, @alternates))} = 1;
			}
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "double_subjrel_that") {
	my $adv = 0;
	my $embedded = 0;
	foreach my $number_main_subj ("singular","plural") {
	    foreach my $number_outer_rel_obj ("singular","plural") {
		foreach my $number_inner_rel_obj ("singular","plural") {
		    if ($complete_flag) {
			@numbers_main_obj = ("singular","plural");
		    }
		    else {
			@numbers_main_obj = ("singular"); # dummy!
		    }
		    foreach my $number_main_obj (@numbers_main_obj) {
			%sentences = ();
			while (scalar(keys (%sentences)) < $sentence_count) {
			    @words = ();
			    @alternates = ();
			    %seen_bucket = ();
			    generate_subj_rel($complete_flag,$number_main_subj,$number_outer_rel_obj,$number_inner_rel_obj,$number_main_obj,$adv,$embedded);
			    if ($complete_flag) {
				$sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_outer_rel_obj, $number_inner_rel_obj, $number_main_obj,@alternates))} = 1;
			    }
			    else{
				$sentences{join ("\t",($structure, join(" ",@words), $number_main_subj, $number_outer_rel_obj, $number_inner_rel_obj, @alternates))} = 1;
			    }
			}
			foreach $sentence (sort (keys(%sentences))) {
			    print $sentence,"\n";
			}
		    }
		}
	    }
	}
    }
    elsif ($structure eq "simple_adv") {
	my $adv = 1;
	my $embedded = 0;
	foreach my $number_subj ("singular","plural") {
	    foreach my $number_obj ("singular","plural") {
		%sentences = ();
		while (scalar(keys (%sentences)) < $sentence_count) {
		    @words = ();
		    @alternates = ();
		    %seen_bucket = ();
		    generate_simple($number_subj,$number_obj,$adv,$embedded);
		    $sentences{join ("\t",($structure, join(" ",@words), $number_subj, $number_obj, @alternates))} = 1;
		}
		foreach $sentence (sort (keys(%sentences))) {
		    print $sentence,"\n";
		}
	    }
	}
    }
    elsif ($structure eq "objrel_adv") {
	my $that = 0;
	my $adv = 1;
	my $embedded = 0;
	foreach my $number_main ("singular","plural") {
	    foreach my $number_rel ("singular","plural") {
		%sentences = ();
		while (scalar(keys (%sentences)) < $sentence_count) {
		    @words = ();
		    @alternates = ();
		    %seen_bucket = ();
		    generate_obj_rel($number_main,$number_rel,$that,$adv,$embedded);
		    $sentences{join ("\t",($structure, join(" ",@words), $number_main, $number_rel, @alternates))} = 1;
		}
		foreach $sentence (sort (keys(%sentences))) {
		    print $sentence,"\n";
		}
	    }
	}
    }
    elsif ($structure eq "objrel_that_adv") {
	my $that = 1;
	my $adv = 1;
	my $embedded = 0;
	foreach my $number_main ("singular","plural") {
	    foreach my $number_rel ("singular","plural") {
		%sentences = ();
		while (scalar(keys (%sentences)) < $sentence_count) {
		    @words = ();
		    @alternates = ();
		    %seen_bucket = ();
		    generate_obj_rel($number_main,$number_rel,$that,$adv,$embedded);
		    $sentences{join ("\t",($structure, join(" ",@words), $number_main, $number_rel, @alternates))} = 1;
		}
		foreach $sentence (sort (keys(%sentences))) {
		    print $sentence,"\n";
		}
	    }
	}
    }
    elsif ($structure eq "subjrel_that_adv") {
	my $adv = 1;
	my $embedded = 0;
	foreach my $number_main ("singular","plural") {
	    foreach my $number_rel_obj ("singular","plural") {
		%sentences = ();
		while (scalar(keys (%sentences)) < $sentence_count) {
		    @words = ();
		    @alternates = ();
		    %seen_bucket = ();
		    generate_subj_rel($number_main,$number_rel_obj,$adv,$embedded);
		    $sentences{join ("\t",($structure, join(" ",@words), $number_main, $number_rel_obj, @alternates))} = 1;
		}
		foreach $sentence (sort (keys(%sentences))) {
		    print $sentence,"\n";
		}
	    }
	}
    }
    elsif ($structure eq "frame_simple") {
	my $that_frame = 0;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_subj ("singular","plural") {
		foreach my $number_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_simple($number_subj,$number_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_subj, $number_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_objrel") {
	my $that_frame = 0;
	my $that_rel = 0;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_objrel_that") {
	my $that_frame = 0;
	my $that_rel = 1;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_subjrel_that") {
	my $that_frame = 0;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_subj_rel($number_main,$number_rel_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_simple_adv") {
	my $that_frame = 0;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_subj ("singular","plural") {
		foreach my $number_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_simple($number_subj,$number_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_subj, $number_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_objrel_adv") {
	my $that_frame = 0;
	my $that_rel = 0;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_objrel_that_adv") {
	my $that_frame = 0;
	my $that_rel = 1;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_subjrel_that_adv") {
	my $that_frame = 0;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_subj_rel($number_main,$number_rel_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_simple") {
	my $that_frame = 1;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_subj ("singular","plural") {
		foreach my $number_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_simple($number_subj,$number_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_subj, $number_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_objrel") {
	my $that_frame = 1;
	my $that_rel = 0;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_objrel_that") {
	my $that_frame = 1;
	my $that_rel = 1;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_subjrel_that") {
	my $that_frame = 1;
	my $adv = 0;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_subj_rel($number_main,$number_rel_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_simple_adv") {
	my $that_frame = 1;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_subj ("singular","plural") {
		foreach my $number_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_simple($number_subj,$number_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_subj, $number_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_objrel_adv") {
	my $that_frame = 1;
	my $that_rel = 0;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_objrel_that_adv") {
	my $that_frame = 1;
	my $that_rel = 1;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_obj_rel($number_main,$number_rel,$that_rel,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    elsif ($structure eq "frame_that_subjrel_that_adv") {
	my $that_frame = 1;
	my $adv = 1;
	my $embedded = 1;
	foreach my $matrix_number ("singular","plural") {
	    foreach my $number_main ("singular","plural") {
		foreach my $number_rel_obj ("singular","plural") {
		    %sentences = ();
		    while (scalar(keys (%sentences)) < $sentence_count) {
			@words = ();
			@alternates = ();
			%seen_bucket = ();
			generate_matrix($matrix_number,$that_frame);
			generate_subj_rel($number_main,$number_rel_obj,$adv,$embedded);
			$sentences{join ("\t",($structure, join(" ",@words), $matrix_number, $number_main, $number_rel_obj, @alternates))} = 1;
		    }
		    foreach $sentence (sort (keys(%sentences))) {
			print $sentence,"\n";
		    }
		}
	    }
	}
    }
    else {
	die "structure $structure not recognized\n";
    }
}