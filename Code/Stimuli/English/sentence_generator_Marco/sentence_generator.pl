#!/usr/bin/perl -w


sub read_rules_file{
    my $rules_file = shift;
    open V,$rules_file;
    while (<V>) {
	chomp;
	if (/^[\t \r]*$/) {
	    next;
	}
	if (/^\#/) {
	    next;
	}
	s/^[ \t]+//;
	s/[ \t\r]+$//;
	my @parts = split "[\|]",$_;
	$parts[0] =~ s/[ \t]+$//;
	my @production_elements = split "[\t ]+",$parts[0];
	$mother = $production_elements[0];
	if ($production_elements[1] =~ /^([^\*]+)\*([^\*]+)/) {
	    $production_elements[1] = $1;
	    $lemma_of{$production_elements[1]} = $2;
	}
	my $production = join " ",@production_elements[1..$#production_elements];
	push @{$productions_of{$mother}},$production; 
	if ($#parts==0) {
	    next;
	}
	$parts[1] =~ s/^[ \t]+//;
	$parts[1] =~ s/[ \t]+$//;
	@features_and_constraints = split "[\t ]+",$parts[1];
	for $item (@features_and_constraints) {
	    ($type,$content) = ($item =~ /^(.)(.*)$/);
	    if ($type eq "+") {
		push @{$features_of{$production}},$content;
	    }
	    elsif ($type eq "-") {
		push @{$constraints_of{$production}},$content;
	    }
	    elsif ($type eq "0") {
		push @{$constraint_removers_of{$production}},$content;
	    }
	    else {
		die "string $item is not a legal attribute\n";
	    }
	}	
    }
    close V;
}

sub check_constraints{
    my $candidate = shift;
    if (!($features_of{$candidate})) {
	return 1;
    }
    for my $feature (@{$features_of{$candidate}}) {
	if ($in_currently_active_constraints{$feature}) {
	    return 0;
	}
    }
    return 1;
}

sub update_constraints{
    my $element = shift;
    if (defined $constraints_of{$element}) {
	for my $constraint (@{$constraints_of{$element}}) {
	    $in_currently_active_constraints{$constraint} = 1;
	}
    }
    if (defined $constraint_removers_of{$element}) {
	for my $constraint (@{$constraint_removers_of{$element}}) {
	    delete $in_currently_active_constraints{$constraint};
	}
    }
}


sub validate_current_structure{
    my $current_structure = shift;
    %in_currently_active_constraints = ();
    my %seen_lemmas = ();
    my $is_valid = 1;
    @elements = split " ",$current_structure;
    for $element (@elements) {
	if ($element =~ /[\[\]]/) {
	    next;
	}
	if (my $lemma = $lemma_of{$element}) {
	    if ($seen_lemmas{$lemma}) {
		$is_valid = 0;
		last;
	    }
	    else {
		$seen_lemmas{$lemma} = 1;
	    }
	}
	if (!(check_constraints($element))) {
	    $is_valid = 0;
	    last;
	}
	update_constraints($element);
    }
    return $is_valid;
}

sub pick_production_of{
    my $constituent = shift;
    my @productions = @{$productions_of{$constituent}};
    $chosen_production= $productions[int(rand(scalar(@productions)))];
    return $chosen_production;
}


sub process_nodes{
    my $input_structure = shift;
    my @input_segments = split " ",$input_structure;
    @output_segments = ();
    foreach $input_segment (@input_segments) {
	
	if ($input_segment !~ /\@/ ) { # lexical item or brackets
	    
	    # possibly remove indices used to distinguish homonymous forms
	    if ($input_segment !~/[\[\]]/) {
		$input_segment =~ s/_.*$//;
	    }
	    push @output_segments,$input_segment;
	}
	else { # node
	    $selected_production = pick_production_of($input_segment);
	    $input_segment =~ s/\@//;
	    push @output_segments,"[_".$input_segment;
	    foreach $element (split " ",$selected_production) {
		push @output_segments,$element;
	    }
	    push @output_segments,"]";
	}
    }
    return join " ",@output_segments;
}

sub generate_full_tree{
    my $top_node = shift;
    my $current_structure = "";
    while (!($current_structure)) {
	$current_structure = process_nodes($top_node);
	while ($current_structure =~ /\@/) {
	    $current_structure = process_nodes($current_structure);
	}
	
	if (!(validate_current_structure($current_structure))) {
	    $current_structure = "";
	}
    }
    # remove token annotation
    $current_structure =~ s/([^\[])_[^ ]+/$1/g;
    return $current_structure;
}

sub annotate_and_print_sentence{
    my $input = shift;

    my $word_string = $input;
    $word_string =~ s/\[_[^ ]+//g;
    $word_string =~ s/\]//g;
    $word_string =~ s/^[ ]+//;
    $word_string =~ s/[ ]+$//;
    $word_string =~ s/[ ]+/ /g;
    
    my $structure = $input;
    $structure =~ s/\[_([^ ]+)[^\]\[]+\]/$1/g;
    my @segments = split " ",$structure;
    my $open_count = 0;
    my $adjacent_count = 0;
    my @open_counts = ();
    my @adjacent_counts = ();
    for $segment (@segments) {
	if ($segment =~ /\[/) {
	    $adjacent_count++;
	    next;
	}
	if ($segment =~ /\]/) {
	    $open_count--;
	    $adjacent_count++;
	    next;
	}
	$open_count++;
	push @open_counts,$open_count;
	push @adjacent_counts,$adjacent_count;
	$adjacent_count = 0;
    }
    push @adjacent_counts,$adjacent_count;
    print join (" | ",(ucfirst($word_string),$input,join(" ",@open_counts),join(" ",@adjacent_counts[1..$#adjacent_counts]))),"\n";
}

# MAIN

# input arguments
$target_sentence_count = shift;
$rules_file = shift;
$top_node = shift;

# globals
%lemma_of = ();    
%productions_of = ();
%constraints_of = ();
%features_of = ();
%constraint_removers_of = ();

print STDERR "reading rules file $rules_file\n";
    
read_rules_file($rules_file);

print STDERR "now generating sentences\n";

# $i = 0;
# while ($i<$target_sentence_count) {
#     print generate_full_tree($top_node),"\n";
#     $i++;
# }

%sentences = ();

while (scalar(keys(%sentences))<$target_sentence_count) {
    $sentences{generate_full_tree($top_node)} = 1;
}

print STDERR "now printing generated sentences\n";

for $sentence (keys(%sentences)) {
    annotate_and_print_sentence($sentence);
}

print STDERR "all done\n";




