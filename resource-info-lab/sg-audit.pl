#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
use POSIX 'strftime';

my $date = strftime '%Y-%m-%d-%H%M%S', localtime;

# Command line argument check
print "File needed: perl $0 file-name\n" and exit(0) if (scalar(@ARGV) != 1);
my $sg_list_file = $ARGV[0];
my %approved_ports = ();
# open sg list file
open (SGFILE, "<", "$sg_list_file") or die "Could not open $sg_list_file $!\n";

# open approved port list file
open (PORTLIST, "<", "approved-ports.list") or die "Could not open approved-ports.list $!\n";

# Approved port in hash %params
while (my $port = <PORTLIST>) {
  chomp $port;
  $approved_ports{$port} = 1 ;
}
close(PORTLIST);

# Read through SGFILE
my $document = do { local $/; <SGFILE> };
close (SGFILE);

# get each security group contents in an array. It should be equal to number of
# SG. Currently last one is not matching. will improve RegEx later.
my (@sg_match)= ($document =~ m/security group name:\s+(.*?)(?=security group name)/sig);

open SGAUDIT, ">", "sg-audit-$date.csv" or die "Couldn't open file. $!\n";
print SGAUDIT "Security GroupName, Security Group Id, Port No., CIDR, Reason\n";

# Port comparison with approved ports
for my $sg(@sg_match){
  my ($sgname) = ($sg =~ /(.*)/mig);
  my ($sgid)   = ($sg =~ /Security Group id: (.*)/mig);
  my ($region) = ($sg =~ /Region: (.*)/mig);

  my (@port_match) = ($sg =~ m/PORT: (.*)/mig);
  
  for my $port(@port_match){
    my ($ip) = ($sg =~ /PORT: $port\nIP ranges: (.*)/mig);

    # If unapproved port, print and also store in a hash
    print SGAUDIT "$sgname, $sgid, $region, $port, $ip, unapproved port\n" if( ($port!~/^(0|-1|1)$/)and !(exists $approved_ports{$port}) );
    print SGAUDIT "$sgname, $sgid, $region, $port, $ip, open to world \n" unless ( ($sgname =~ /default/i) or ($port =~/^(0|-1|1|80|443|1194|5432|5439|9001|27017)$/) or $ip!~/^0\.0\.0\.0/);
  }
}



