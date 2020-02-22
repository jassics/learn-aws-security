#!/usr/bin/perl 
use strict;
use warnings;
use JSON qw( decode_json );
use Data::Dumper;

my $region = 'us-east-1';

# instances
my $jsoni = `aws --output json --region=$region ec2 describe-instances`;

print "Got instances...\n\n";

my $decoded   = decode_json($jsoni);
my %hash_ip   = ();
my @reserv    = @{ $decoded->{'Reservations'} };

# saving security group attached to each public IP
foreach my $f ( @reserv ) {
    my @instances = @{ $f->{'Instances'} };
    foreach my $g ( @instances ) {	
	    my $publicip = $g->{'PublicIpAddress'};
	    my @secgrp = @{ $g->{'SecurityGroups'} };

	    foreach my $h ( @secgrp ) {
	      my $secg = $h->{'GroupName'};

	      $hash_ip{$secg}   = "$publicip, $secg " if($publicip);
	    }
    }
}

# Security group
my $jsonsg  = `aws --output=json --region=$region ec2 describe-security-groups`;
$decoded = decode_json($jsonsg);
my @secgrp  = @{ $decoded->{'SecurityGroups'} };

foreach my $f ( @secgrp ) {
    my $desc  = $f->{"Description"};
    my $group = $f->{"GroupName"};
    my @ipperm = @{ $f->{'IpPermissions'} };

    foreach my $g ( @ipperm ) {	
	    my $toport   = $g->{'ToPort'};
	    my $fromport = $g->{'FromPort'};
	    my $proto    = $g->{'IpProtocol'};
	    my @cidr     = @{ $g->{'IpRanges'} };

	    foreach my $h ( @cidr ) {
	      my $cidr = $h->{'CidrIp'};

	      if ($cidr =~ m!0\.0\.0\.0/0!) {
		      if (defined $hash_ip{$group}) {
		        my $ips = $hash_ip{$group};
		        chomp($ips);
		        print "Group Name : $group\n";
		        print "Description: $desc\n";
		        print "Used for these hosts: ".$ips."\n";
           
		        if ($proto eq "-1") { 
			        print "any IP traffic, from source $cidr\n";
		        } else {
			        if ($fromport ne $toport) {
			          print "dst ports $fromport:$toport/$proto, from source $cidr\n";
			        } else {
			          print "dst ports $fromport/$proto, from source $cidr\n";
			        }
		        }
		        print "\n";
          } 
        }	
      }
	    
    }
}

