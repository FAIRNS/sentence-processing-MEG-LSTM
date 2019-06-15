#!/usr/bin/perl -w

$out_prefix = shift;

while (<>) {
    chomp;
    @F = split "\t",$_;
    @sentence = split " ",$F[0];
    $target = $sentence[$#sentence];
    $number = $F[1];
    $seen_number{$number} = 1;
    $id = $F[3];
    if ($F[2] eq "correct") {
	$sentence_of{$id} = $F[0];
	$correct_target_of{$id} = $target;
	$target_index_of{$id} = $#sentence;
	$number_of{$id} = $number;
    }
    else {
	$wrong_target_of{$id} = $target;
    }
}

foreach $number (keys %seen_number){
    $fh = "TEXT_".$number;
    open $fh,">${out_prefix}_${number}_sentences.text";
    $fh = "GOLD_".$number;
    open $fh,">${out_prefix}_${number}_sentences.gold";
}
foreach $id (keys %sentence_of) {
    $fh = "TEXT_".$number_of{$id};
    print $fh  $sentence_of{$id},"\n";
    $fh = "GOLD_".$number_of{$id};
    print $fh join("\t",($target_index_of{$id},$correct_target_of{$id},$wrong_target_of{$id},"0")),"\n";
}
foreach $number (keys %seen_number){
    $fh = "TEXT_".$number;
    close $fh;
    $fh = "GOLD_".$number;
    close $fh;
}
