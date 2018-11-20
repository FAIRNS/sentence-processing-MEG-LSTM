#!/usr/bin/perl -w

# usage:
# perl ./compute_unigram_baseline.pl freq_file linzen_gold_file > out_file
#
# where
#
# freq_file contains words and frequencies in tab-delimited format
# linzen_gold_file is a gold file in the Linzen agreement task format
#
# the out_file will contain each pair of correct/wrong forms from the
# gold file with the corresponding frequencies, and a last #-prefixed
# line with the unigram baseline accuracy
#
# NB1: if a target form is not in the frequency file, its frequency is
# set to 0, and a warning is sent to STDERR

$freq_file_name = shift;
$linzen_gold_file_name = shift;

open FQ,$freq_file_name;
while (<FQ>) {
    chomp;
    ($w,$f) = split "[\t ]+",$_;
    $freq_of{$w} = $f;
}
close FQ;

$hits = 0;

open GOLD,$linzen_gold_file_name;
while (<GOLD>) {
    chomp;
    @F = split "[\t ]+",$_;
    $correct_w = $F[1];
    $wrong_w = $F[2];
    if (!defined($freq_of{$correct_w})) {
	print STDERR "$correct_w not in frequency list\n";
	$correct_fq = 0;
    }
    else {
	$correct_fq = $freq_of{$correct_w};
    }
    if (!defined($freq_of{$wrong_w})) {
	print STDERR "$wrong_w not in frequency list\n";
	$wrong_fq = 0;
    }
    else {
	$wrong_fq = $freq_of{$wrong_w};
    }
    print join ("\t",($correct_w,$correct_fq,$wrong_w,$wrong_fq)),"\n";
    $tot++;
    if ($correct_fq > $wrong_fq) {
	$hits++;
    }
    elsif ($correct_fq == $wrong_fq) {
	# if frequencies are equal, toss a coin
	if (int(rand(2))) {
	    $hits++;
	}
    }
}
close GOLD;

$acc = $hits/$tot;
print "# $acc\n";

    

	
