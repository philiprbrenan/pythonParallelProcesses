#!/usr/bin/perl -I/home/phil/perl/cpan/DataTableText/lib/ -I/home/phil/perl/cpan/GitHubCrud/lib/
#-------------------------------------------------------------------------------
# Push Process Python in Parallel
# Philip R Brenan at gmail dot com, Appa Apps Ltd Inc., 2025
#-------------------------------------------------------------------------------
use v5.34;
use warnings FATAL => qw(all);
use strict;
use Carp;
use Data::Dump qw(dump);
use Data::Table::Text qw(:all);
use GitHub::Crud qw(:all);

my $repo = q(pythonParallelProcesses);                                          # Repo
my $home = fpd q(/home/phil/z/python/), $repo;                                  # Home folder
my $user = q(philiprbrenan);                                                    # User
my $wf   = q(.github/workflows/main.yml);                                       # Work flow on Ubuntu

push my @files, searchDirectoryTreesForMatchingFiles($home, qw(.pl .py .md));   # Files to upload

pushToGitHub($user, $repo, $home, @files);                                      # Upload each selected file if it has changed

if (1)                                                                          # Write workflow
 {my $d = dateTimeStamp;
  my $y = <<"END";
# Test $d

name: Test
run-name: $repo

on:
  push:
    paths:
      - '**/main.yml'

jobs:

  test:
    permissions: write-all
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout\@v4
      with:
        ref: 'main'

    - name: Run in parallel
      run: |
        python3 pythonParallelProcesses.py
END

  my $f = writeFileUsingSavedToken $user, $repo, $wf, $y;                       # Upload workflow
  lll "$f  Ubuntu work flow for $repo";
 }
