#!/usr/bin/perl 
use JSON qw( decode_json );

# I am assuming that region is known and aws cli setup for aws configure is done
# Get the instance details
# And run security group check for CIDR 0.0.0.0/0 on those instances

my $region = 'us-east-1';

# instances
my $jsoni = `aws --output json --region=$region ec2 describe-instances`;
my $decoded = decode_json($jsoni);
my @reserv  = @{ $decoded->{'Reservations'} };

foreach my $f ( @reserv ) {
    my @instances = @{ $f->{'Instances'} };
    foreach my $g ( @instances ) {	
	    $platf    = $f->{"Platform"};    
	    $instid   = $g->{'InstanceId'};
	    $publicip = $g->{'PublicIpAddress'};
      
	    @secgrp   = @{ $g->{'SecurityGroups'} };

	    foreach my $h ( @secgrp ) {
	      $secg = $h->{'GroupName'};

	      $hash_ip{$secg}   = "$publicip,".$hash_ip{$secg};
	      $hash_inst{$secg} = "$instid,".$hash_inst{$secg};
	    }
    }
}

# Security group
my $jsonsg = `aws --output=json --region=$region ec2 describe-security-groups`;
$decoded = decode_json($jsonsg);
my @secgrp = @{ $decoded->{'SecurityGroups'} };

foreach my $f ( @secgrp ) {
    $desc=$f->{"Description"};
    $group=$f->{"GroupName"};
    
    my @ipperm = @{ $f->{'IpPermissions'} };

    foreach my $g ( @ipperm ) {	
	    $toport=$g->{'ToPort'};
	    $fromport=$g->{'FromPort'};
	    $proto=$g->{'IpProtocol'};

	    my @cidr = @{ $g->{'IpRanges'} };
	    foreach my $h ( @cidr ) {
	      $cidr=$h->{'CidrIp'};
	      if ($cidr=~m!0\.0\.0\.0/0!) {

		      if ($hash_ip{$group} ne "") {
		        $ips=$hash_ip{$group};
		        chop($ips);
		        print "Group Name : $group\n";
		        print "Description: $desc\n";
		        print "Used for these hosts: ".$ips."\n";
		      if ($proto==-1) { 
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


