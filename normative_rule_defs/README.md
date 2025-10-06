# Normative Rule Definition Files

This directory contains one normative rule definition file per adoc chapter file.
Each definition file has the same name as its corresponding adoc file with the extension changed from .adoc to .yaml.
See rv32.yaml for a good example of a definition file that includes additional informative comments.

Each definition file provides the information required to create the normative rules for
its corresponding adoc file. The adoc file contains tags (AKA AsciiDoc anchors with names with a "norm:" prefix) of text associated with normative rules.

In many cases there is a 1:1 mapping between normative rules and tags but not always (1:many, many:1, and many:many also exist). The definition files provide the mapping information to create normative rules from the tags.
The definition files also contain additional meta-data added to the normative rule definitions.

The Ruby script in docs-resources/tools/create_normative_rules.rb consumes these definition files along with
the extracted normative tags from the ISA manual chapters to create a file containing all normative rules
for all ISA manuals (priv & unpriv).

See the schemas in docs-resources/schemas for a machine-readable definition of the input and output file formats:
* File defs-schema.json is the format of the definition input file format (YAML).
* File norm-rules-schema.json is the format of the normative rule output file format (JSON).

Using Visual Studio Code to edit the definition YAML files is encouraged since it provides
live schema feedback.
