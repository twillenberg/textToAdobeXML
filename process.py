#!/usr/bin/python3

import csv
import os.path
import hashlib
import random

# This script converts a structured text file into an XML file that can be read by Adobe Illustrator.
# Adobe Illustrator uses the file to auto-generate "Certificates of Particiaption" for training course participants.
# The conversion process involves the following files:
#   participants.txt > hashes.txt > dataset.xml
# Each row of the "participants.txt" file should be structured as follows:
#   FullName, EmailAddress

# If the files hashes.txt or dataset.xml exist, remove them as it is output from a previous iteration.
if os.path.isfile('hashes.txt'):
    os.remove('hashes.txt')
if os.path.isfile('dataset.xml'):
    os.remove('dataset.xml')

# Create a file handle for an output file to write to.
fileHashes = open('hashes.txt','w')

# Open the input file for reading of the names and seeds.
with open('participants.txt', 'r') as fileParticipants:
    # Read in a line from the text file.
    reader = csv.reader(fileParticipants, dialect='excel', delimiter=",")

    for row in reader:
        fullName = row[0]
        emailAddress = row[1]
        # Create a random 10-digit seed number for each row and append it.
        seed = round(random.random()*10000000000)
        
        # String input to the has function according the recipe.
        rawInput = fullName + ": " + str(seed) + "\n"
        # Convert the raw input into a bytes.
        byteInput = bytes(rawInput, 'utf-8')
        # Create a new empty hash object.
        hashInput = hashlib.new('sha256')
        # Feed the bytes to the hash function.
        hashInput.update(byteInput)

        # Write out the new line with the hashdigest included.
        fileHashes.write(fullName + ', ' + emailAddress + ', ' + hashInput.hexdigest() + '\n')

# Close the files read from and written to.
fileParticipants.close()
fileHashes.close()

if os.path.isfile('dataset.xml'):
    os.remove('dataset.xml')

# Create a file handle for an output file to write to.
fileDataset = open('dataset.xml','w')

# Create the XML file header.
header = '''\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20001102//EN" "http://www.w3.org/TR/2000/CR-SVG-20001102/DTD/svg-20001102.dtd" [
    <!ENTITY ns_graphs "http://ns.adobe.com/Graphs/1.0/">
    <!ENTITY ns_vars "http://ns.adobe.com/Variables/1.0/">
    <!ENTITY ns_imrep "http://ns.adobe.com/ImageReplacement/1.0/">
    <!ENTITY ns_custom "http://ns.adobe.com/GenericCustomNamespace/1.0/">
    <!ENTITY ns_flows "http://ns.adobe.com/Flows/1.0/">
<!ENTITY ns_extend "http://ns.adobe.com/Extensibility/1.0/">
]>
<svg>
    <variableSets  xmlns="&ns_vars;">
        <variableSet locked="none" varSetName="binding1">
            <variables>
                <variable varName="fullName" trait="textcontent" category="&ns_flows;"></variable>
                <variable varName="emailAddress" trait="textcontent" category="&ns_flows;"></variable>
                <variable varName="hash" trait="textcontent" category="&ns_flows;"></variable>
            </variables>
            <v:sampleDataSets  xmlns:v="&ns_vars;" xmlns="&ns_custom;">
'''

# Write out the header row.
fileDataset.write(header)

# Open the input file for reading names and seeds.
with open('hashes.txt', 'r') as fileHashes:
    # Read in a line from the text file.
    reader = csv.reader(fileHashes, dialect='excel', delimiter=',')

    for row in reader:
        fullName = row[0]
        emailAddress = row[1].lstrip()
        hashValue = row[2].lstrip()

        rowContents = f"""\
                <v:sampleDataSet dataSetName="{fullName}">
                    <fullName>
                        <p>{fullName}</p>
                    </fullName>
                    <emailAddress>
                        <p>{emailAddress}</p>
                    </emailAddress>
                    <hash>
                        <p>{hashValue}</p>
                    </hash>
                </v:sampleDataSet>
"""
        # Write out the new line with the hashdigest included.
        fileDataset.write(rowContents)
    

    footer = '''\
            </v:sampleDataSets>
        </variableSet>
    </variableSets>
</svg>
'''
    fileDataset.write(footer)
    fileHashes.close()

# Close the files read from and written to.
fileDataset.close()

if os.path.isfile('hashes.txt'):
    os.remove('hashes.txt')

if os.path.isfile('participants.txt'):
    os.remove('participants.txt')
