#!/usr/bin/perl -w

use List::Util qw(shuffle);

$sentence_slot = shift;
$adj_slots_string = shift;
$adj_file = shift;
$sentence_file = shift;

@adj_slots = split ":",$adj_slots_string;

open ADJS,$adj_file;
while (<ADJS>) {
    chomp;
    push @adjectives,$_;
}
close ADJS;

if ($#adjectives < $#adj_slots) {
    die "$#adjectives provided but $#adj_slots requested\n";
}

open SENTS,$sentence_file;
while (<SENTS>) {
    chomp;
    @F = split "\t",$_;
    @words = split " ",$F[$sentence_slot];
    $i = 0;
    @edited_sentence = ();
    my @shuffled_adjs = shuffle @adjectives;
    foreach $adj_slot (@adj_slots) {
	while ($i < $adj_slot) {
	    push @edited_sentence,$words[$i];
	    $i++;
	}
	push @edited_sentence,shift @shuffled_adjs;
    }
    while ($i<=$#words) {
	push @edited_sentence,$words[$i];
	$i++;
    }
    $F[$sentence_slot] = join " ",@edited_sentence;
    print join("\t",@F),"\n";
}
close SENTS;
