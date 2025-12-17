#!/usr/bin/env python3
#  Python version of a very basic variant calling pipeline
import os
import argparse
import subprocess

# A beginner's effort at automating variant calling
# three familiar steps:
# bwa mem ref.fa reads1 reads2 > sample.sam  ALIGN the files
# samtools sort sample.sam > sample-s.sam SORT the alignment
# bcftools mpileup -Ou -f ref.fa sample-s.sam | bcftools call -vmO v -o sample.vcf CALL variants

# As a newb at coding, I took the barebones example from class and built from there
# I used google-fu and a focus on the end goal to get most of the way through
# When I got seriously stuck I used chatGPT to figure out the logic and order of operations with all the '"[{]}]" symmbols

# The output of the copy/pasteable table of VCF data was ok, but a little weak.
# so I spent many hours trying to get an automated parameter sweep loop established
# Only 2 variables are included in this one!

# create ArgumentParser object
args = argparse.ArgumentParser(prog='Very Basic Variant Calling',
                               description="Align, Sort, Call: Output", epilog='i ate too many paint chips')

args.add_argument('-i', '--input_sample_name', type=str,
                  required=True, help='Base sample name')

parsed = args.parse_args()

subprocess.Popen("echo " + parsed.input_sample_name +
                 ' reads to align sort pile and call', stderr=subprocess.PIPE, shell=True)
# Align
subprocess.run(
    'bwa mem /home/spingus/tiny-test-data/genomes/Hsapiens/hg19/bwa/hg19.fa mt_1.fq.gz mt_2.fq.gz > mt_a.sam', shell=True)
# Sort
subprocess.run('samtools sort mt_a.sam > mt_s.sam', shell=True)
# Call
subprocess.run('bcftools mpileup -Ou -f /home/spingus/tiny-test-data/genomes/Hsapiens/hg19/seq/hg19.fa mt_s.sam | bcftools call -vmO v -o mt_v.vcf', shell=True)
# Make sure the files are viable
subprocess.run(
    'samtools quickcheck *.sam && echo bitchin || echo FAIL!ZOMGWTFBBQ', shell=True)
# just a makeshift header for the table
print("CHROM", "POS", "REF", "ALT", "FREQ", "GT", "PL")
# All the tasty datas printed out in a table
subprocess.run(
    "bcftools query -f '%CHROM %POS %REF %ALT %AN %AC{0} [\t%GT\t%PL]\n' mt_v.vcf | awk '{printf \"%s %s %s %s %f %s %s\\n\",$1,$2,$3,$4,$6/$5,$7,$8}'", shell=True)

# Getting out of my depth with loops and output

# establish a framework for the various user inputs


def parameter_sweep(parameter_type):
    for file in os.listdir('.'):
        if file.startswith('mtv') and file.endswith('.sam'):
            # trying to be tidy
            os.remove(file)
# the inputs, only two for this version, and the action, a parameter sweep with a defined range
# IDK how to make it accept only uppercase inputs!
    if parameter_type.upper() == "W":
        for i in range(1, 26):
            i_str = str(i).zfill(2)
            command = f'bwa mem -W {i_str} /home/spingus/tiny-test-data/genomes/Hsapiens/hg19/bwa/hg19.fa mt_1.fq.gz  mt_2.fq.gz > mtvariable{i_str}.sam'
            subprocess.run(command, shell=True)
    elif parameter_type.upper() == "B":
        for i in range(1, 26):
            i_str = str(i).zfill(2)
            command = f'bwa mem -B {i_str} /home/spingus/tiny-test-data/genomes/Hsapiens/hg19/bwa/hg19.fa mt_1.fq.gz  mt_2.fq.gz > mtvariable{i_str}.sam'
            subprocess.run(command, shell=True)
    else:
        print("Invalid parameter type. Please enter 'W' or 'B'.")


while True:
    response = input("Would you like to play a game? (y/n): ")

    if response.lower() == "y":
        while True:
            parameter_response = input(
                "ParameterSweeper: Enter parameter(W/B): ")
            parameter_sweep(parameter_response)
            average_values = []
# output the average values across the variable range
            for file in os.listdir('.'):
                if file.startswith('mtv') and file.endswith('.sam'):
                    print(file.replace("mtvariable", "var").replace(".sam", ""))
                    with open(file, 'r') as f:
                        total = 0
                        count = 0
                        for line in f:
                            if not line.startswith('@'):
                                fields = line.split('\t')
                                if len(fields) >= 5:
                                    total += int(fields[4])
                                    count += 1
                        if count > 0:
                            average = total / count
                            average_values.append(average)
                            print(average)

            break
    elif response.lower() == "n":
        print("Bai!")
        break
    else:
        print("Invalid response. Please enter 'y' or 'n'.")
