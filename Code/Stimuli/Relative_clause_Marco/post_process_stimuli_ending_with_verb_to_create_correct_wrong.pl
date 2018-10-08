#!/usr/bin/perl -w

while (<>) {
    chomp;
    @F = split "\t",$_;
    $id++;
    print join("\t",($F[1],"correct",$F[2],"id".$id)),"\n";
    $F[1]=~s/ [^ ]+$//;
    print join("\t",($F[1]." ".$F[$#F],"wrong",$F[2],"id".$id)),"\n";
}
