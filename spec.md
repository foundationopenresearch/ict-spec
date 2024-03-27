# Interoperable Computational Tool

This document defines an Interoperable Computational Tool (ICT). The goal of this document is to enable the creation and dissemination of interoperable tools for image analysis, molecular modeling, genomics, bioinformatics, or any other scientific domain.

## Table of Contents

- [Overview](#overview)
  - [Example](#example)
- [Tool Packaging](#tool-packaging)
- [Metadata](#metadata)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Types and Formats](#types-and-formats)
  - [Ontology](#ontology)
- [User Interface](#user-interface)
  - [Basic Types](#basic-ui-types)
  - [Conditionals](#conditionals)
  - [Custom Types](#custom-ui-types)
- [Hardware Requirements](#hardware-requirements) [TODO]

## Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## Definitions

Unless specified otherwise in the documentation, all usage of the words/phrases listed [here](definitions.md) are explicitly defined in manner which may or may not adhere to conventional or colloquial definitions.

# Overview

An ICT refers to any analysis code packaged along with dependencies for the intent of dissemination and reusability. 

An ICT is defined by two components: the specification and the tool. The specification is a YAML file that defines all parameters and requirements for a user interface to execute a predetermined piece of analysis code. Metadata contained within this file applies common [FAIR principles](https://www.go-fair.org/fair-principles/) of interoperability and reusability to discrete pieces of analysis code. The tool is a packaged piece of analysis code, complete with any and all dependencies needed to run the code. Each ICT must contain both a specification file and associated tool to be considered a complete ICT. 

Analysis code should not be limited to any programming language, scientific domain, or use case. The ICT specification makes no requirements on the contents or scope of the analysis code, but provides some [best practices](best_practices.md), recommendations, and tips to make the most of the ICT specification.

### Example

```yaml
specVersion: 0.1.0
name: wipp/threshold
version: 1.1.1
container: wipp/wipp-thresh-plugin:1.1.1
entrypoint: ""
title: Thresholding Plugin
description: Thresholding methods from ImageJ
author: Mohammed Ouladi
repository: https://github.com/usnistgov/WIPP-thresholding-plugin
documentation: 
citation: 
hardware:
  cpu:
    type: 
    min: 100
  memory:
    min: 100M
  gpu:
    required: false
    type: 
    min: 
inputs:
- name: input
  required: true
  description: Input image collection to be processed by this plugin
  type: path
  format: 
    uri: http://edamontology.org/format_3727
    term: OME-TIFF
- name: thresholdtype
  required: true
  description: Algorithm type for thresholding
  type: string
  format:
    uri: http://edamontology.org/operation_image_thresholding
    term: plain text format
- name: thresholdvalue
  required: false
  description: Threshold value for manual setting
  type: number
  format: 
    uri:
    term:
outputs:
- name: output
  required: true
  description: Output data for the plugin
  type: path
  format: [image thresholding]
ui: 
- key: inputs.input
  title: "Image Collection: "
  description: "Pick a collection..."
  type: text
- key: inputs.thresholdtype
  title: "Threshold Type"
  description: "Pick a thresholdtype"
  type: select
  fields: [Manual, IJDefault, Huang, Huang2, Intermodes, IsoData, Li, MaxEntropy, Mean, MinErrorI, Minimum, Moments, Otsu, Percentile, RenyiEntropy, Shanbhag, Triangle, Yen]
- key: inputs.thresholdvalue
  title: Threshold Value
  description: 
  type: number
  condition: "inputs.thresholdtype=='Manual'"
```

# Tool Packaging

Each tool must be packaged as container image and hosted on a public or private image repository. The container must adhere to the [OCI Image Format](https://github.com/opencontainers/image-spec) and can be built using a number of different container engines, including (but not limited to): [Docker](https://www.docker.com/), [Podman](https://podman.io/), and [Apptainer](https://apptainer.org/). Each container image must contain all necessary dependencies required to run the analysis code contained within, including both manually added binaries/source code and dependencies installed by package managers during the container build process. Implementation of code within an image is left entirely to the plugin developer, but we provide some [guidelines](packaging_guidelines.md) and [best practices](best_practices.md) to help the development process.  

# Metadata

| Field | Description | Example |
| ----- | ----------- | ------: |
| specVersion | Version of ICT specification yaml schema | 0.1.0 |
| name | Unique identifier for ICT tool scoped on organization or user, should take the format `<organization/user>/<ICT name>` | wipp/threshold | 
| version | Version of ICT, [semantic versioning](https://semver.org/) is recommended | 1.1.1 |
| container | Direct link to hosted ICT container image, should take the format `<registry path>/<image repository>:<tag>`, registry path may be omitted and will default to Docker Hub | wipp/wipp-thresh-plugin:1.1.1 |
| entrypoint | Absolute path to initial script or command within packaged image | "" |
| title | (optional) Descriptive human-readable name, will default to `name` if omitted | Thresholding Plugin |
| description | (optional) Brief description of plugin | Thresholding methods from ImageJ |
| author | Comma separated list of authors, each author name should take the format `<first name> <last name>`| Mohammed Ouladi |
| contact | Email or link to point of contact (ie. GitHub user page) for questions or issues | mohammed.ouladi@labshare.org |
| repository | Url for public or private repository hosting source code | https://github.com/polusai/polus-plugins
| documentation | (optional) Url for hosted documentation about using or modifying the plugin | 
| citation | (optional) DOI link to relavent citation, plugin users should use this citation when using this plugin | 
<br>

# Inputs and Outputs

The inputs and outputs section of the ICT specification clearly defines all possible parameters available to configure on the ICT tool. These convey parameters passed directly to the ICT tool and should dictate exactly what the ICT tool is expecting.
<br><br>
| Field | Description | Example |
| ----- | ----------- | ------: |
| name | Unique input or output name for this plugin, case-sensitive match to corresponding variable expected by tool | thresholdtype |
| required | Boolean (true/false) value indicating whether this field needs an associated value | true |
| description | Short text description of expected value for field | Algorithm type for thresholding |
| type | Defines the parameter passed to the ICT tool based on broad categories of [basic types](#types-and-formats) | string |
| format | Defines the actual value(s) that the input/output parameter represents using an [ontology schema](#ontology) | ['image thresholding'] |
| defaultValue | Optionally defines the default value for each input/output | true |
<br>

## Types and Formats

The basic types broadly categorize the format of the parameter passed to the ICT tool. Each parameter is passed to the ICT tool as a command line argument and the basic types represent the format of those arguments.
<br><br>
| Type | Description | Example |
| ---- | ----------- | ------: |
| string | The most basic parameter type, effectively any set of characters | IJDefault |
| number | Any numeric characters, with no distinction between integers and floats | 2.0 |
| array | List of arbitrary string values using the convention of comma-separated values between square brackets | [1, next, 'and,2'] | 
| boolean | Limited to `true` and `false` values | true |
| path | String value that represents a file or directory path using Unix conventions | path/to/file/or/directory | 
<br>

The format defined by the `type` may be different from the representative format defined in the `format` field. For example, a tool may expect a JPEG image as an input. The tool is not configured, however, to accept a JPEG binary directly as a command line parameter, instead, the tool expects the input parameter to reference a file path to a JPEG image. In this case, the `type` of this input is `path`, while the `format` is `JPEG`. Appropriately defined `format` fields are used to ensure interoperability and findability for the ICT. When chaining two plugins together in sequence, the outputs of one plugin may be safely passed to the inputs of the second plugin based on matching or corresponding `format` fields. This functionality is not explicitly a part of the ICT and instead relies on the implementation and validation handled by ICT consumers -- user interface applications. The `format` field also relies heavily on a common [ontology](#ontology) -- a set of concepts and categories within a domain with explicitly defined properties and relationships to other items within the set. While the ICT is heavily reliant on a consistent and comprehensive ontology, the maintenance of such an ontology is not within the scope of the ICT. 

## Ontology

A comprehensive ontology plays a vital role in ensuring interoperability between ICTs. In order to safely pass parameters between ICTs in a workflow, or across workflows, the `format` field needs to draw from a predefined dictionary of terms and naming conventions. This dictionary serves as the source of truth and a reference for defining relationships, understanding context, and validating interoperability. The ICT specification relies on an open source ontology of bioscientific data analysis and data management, [EDAM](http://edamontology.org/). The EDAM ontology is well-established especially in regards to computational biology and genomics/proteomics bioinformatics concepts. The ontology is also easily extensible and significant progress has been made with the [EDAM-bioimaging](https://github.com/edamontology/edam-bioimaging), focused on adding bioimage analysis, informatics, and topics to the ontology.

When defining the `format` fields in an ICT, there are a number of conditions and caveats to keep in mind. Inputs and outputs can be loosely categorized as data and metadata. Data parameters typically fit nicely into a specific file format, for example for image data, common formats include: PNG, JPEG, TIF. These formats define how information within a file is encoded and may also define syntax within that file. Well defined data parameters are essential for enabling interoperability between plugins and should be selected with care. When defining the `format` of a data parameter, is it useful to think of the functionality embedded within the plugin tool. For example, with output parameters, what is the format of the file that the plugin tool is writing. Input data parameters can be more complex, as depending on the functionality of the plugin tool, multiple formats may be accepted. For example, a plugin tool could accept similar file formats that represent the same data (ie. CSV and Parquet) or handle format conversion as the first step within the plugin. 

Metadata parameters are usually more ambiguous and are often not sufficiently defined by a file format. Many metadata input parameters define settings or configuration values for a plugin, either as a simple numerical or string value or a more complex text file. In cases where a file format can be applied to a metadata parameter, such as JSON or YAML format text file, the file format gives little context or information about the metadata parameter. In most cases, the `format` field for metadata parameters is better served by context or semantic based ontology definitions rather than strict formats. Take the image thresholding plugin [specification](#example) for example. The input parameter `thresholdingtype` enables the user to select from a list of different thresholding algorithms. Strictly using file format for the `format` field for the `thresholdingtype` would provide no context and offers no support for interoperability. A more effective and useful definition from our ontology would be `image thresholding`, which connotes the operation being modified by this input parameter. These context based ontology definitions in the `format` field of the ICT specification can enable interoperability between plugins in a more limited or situation-specific capability. Settings and configuration style parameters are more commonly used as manual user input, rather than direct output from a previous plugin. These metadata parameters, however, play an important role in the findability of plugins, allowing users to rely on the same comprehensive ontology to categorize and filter across a list of relevant plugins. 

# User Interface

Each input and output parameter defined in the ICT specifications must have a corresponding user interface (UI) configuration in the `ui` section of the specification file. This UI configuration will provide meaningful guidelines and standards for any specific UI application or platform that works with or uses ICTs. The standardization provided by the UI configuration section enables portability of the ICT across different organizations, institutes, or facilities. Any UI implementation can use ICTs given that they follow a loose set of guidelines, specifically related to [basic UI types](#basic-ui-types) and handling [conditionals](#conditionals).
<br><br>
| Field | Description | Example |
| ----- | ----------- | ------: |
| key | Identifier to connect UI configuration to specific parameter, should take the form `<inputs or outputs>.<parameter name>` | inputs.thresholdvalue |
| title | User friendly label used in UI | "Thresholding Value" |
| description | Short user friendly instructions for selecting appropriate parameter | "Enter a threshold value" |
| type | Defines the expected user interface based on a set of [basic UI types](#basic-ui-types) | number |
| customType | Optional label for a [non-standard](#custom-ui-types) expected user interface | |
| condition | [Conditional statement](#conditionals) that resolves to a boolean value based on UI configuration and selected value, used to dictate relationship between parameters | "inputs.thresholdtype=='Manual'" |
| options | Basic UI type specific options | 
<br>

## Basic UI Types

The basic UI types define a set of interactive controls that enable users to control and configure ICT parameters. To enable compatibility across different applications and platforms the UI configurations of the ICT specification need to adhere to a standard set of basic UI types. The basic types cover most generic use cases across a broad range of input and output parameters. While any particular UI application is free to implement each type as they see fit, all applications and platforms that use ICTs must support each of the basic UI types. By dictating the control types and options, but not any implemention details, each UI application has degree of flexibility to implement UI that adheres to the ICT requirements without sacrificing client requirements or platform integrations. This also reduces the burden and amount of work for existing UI applications solutions to integrate with the ICT specification. The `path` type best highlights the utility of this flexibility across UI implementations. Taken at face value, the `path` type is simply a formatted string and in simple applications, can be implemented as a basic text input box. An integrated platform solution, on the other hand, may have all relevant files or data stored in aggregated and cataloged data lake. This implementation of the `path` type can be much complex, allowing users to find relevant files or data using metadata based filters, searches, and autocomplete functionalities. Finally, a desktop application designed for local execution may choose to implement the `path` type using a local file browser for files or data stored on the client machine.
<br><br>
| Type | Description | Options |
| ---- | ----------- | ------- |
| text | Any arbitrary length string | `default`: prefilled value <br> `regex`: regular expression for validation <br> `toolbar`: boolean value to add text formatting toolbar | 
| number | Any numerical value | `default`: prefilled value <br> `integer`: boolean value to force integers only <br> `range`: minimum and maximum range as a tuple |
| checkbox | Boolean operator, checked for `true` unchecked for `false | `default`: prefilled value, either `true` or `false` |
| select | Single string value from a set of options | `fields`: required array of options <br> `optional`: leave blank by default |
| multiselect | One or more string values from a set of options | `fields`: required array of options <br> `optional` leave blank by default <br> `limit`: maximum number of selections |
| color | Color values passed as RGB color values | `fields`: array of preset RGB selections |
| datetime | Standardized date and time values | `format`: datetime format using [W3C conventions](https://www.w3.org/TR/NOTE-datetime) |
| path | Absolute or relative path to file/directory using Unix conventions | `ext`: array of allowed file extensions |
| file | User uploaded binary data | `ext`: array of allowed file extensions <br> `limit`: maximum number of uploaded files <br> `size`: total file size limit |
<br>

## Conditionals

Given the complexity that an ICT with several input and output parameters can introduce, it is useful to have some way to configure logical relationships in the UI flow. The `condition` field in the UI configuration enables the ICT to dictate relationships between input/output parameters and simplify the user experience for consumers of the ICT. Commonly, certain input parameters are only valid given specific configurations of other input parameters. For example, in the ICT defined above the `thresholdvalue` input parameter only applies when a specific `thresholdtype` is selected. The `condition` field should be populated by a conditional statement that evaluates to a boolean value. References to other input or output parameters should use the unique `key` for each parameter and one of the following operators:
<br><br>
| Operator | Definition |
| :------: | ---------- |
| `==` | equal to |
| `!+` | not equal |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |
| `&&` | and operator to combine two or more conditional expressions |
| `\|\|` | or operator to combine two or more conditional expressions |
| `?` | ternary operator for if/then expressions |
<br>

Like other aspects of the user interface definition, evaluation and usage of the `condition` field is handled individually by applications or platforms that consume ICTs and their workflows. In general, `true` should indicate that the parameter is used, while `false` should indicate that the paramter is not applicable. Multiple conditional expressions can be chained together to define more complex relationships between different parameters. Finally, the ternary operator enables an additional layer of customizability, allowing the ICT to define a default value for a particular paramater, instead of marking it off as not applicable. This can be useful in specific situations where the value of other parameters may restrict the value of a particular parameter that can be left blank.

To provide additional support for conditional logic, each input or output parameter can be overloaded with multiple UI configurations. When combined with appropriate conditionals, this enables the ICT developer to create more complex and customizable user logic for interacting with ICT inputs and outputs. As shown in the example snippet below, an overloaded UI configuration of a `select` type could provide different selection options based on the parameter of a different field.

```yaml
ui: 
- key: inputs.first_parameter
  type: checkbox
- key: inputs.second_parameter
  type: select
  fields: ['option1', 'option2', 'option3']
  condition: "inputs.first_parameter==true"
- key: inputs.second_parameter
  type: select
  fields: ['option1', 'option3']
  condition: "inputs.first_parameter==false"
```

## Custom UI Types

Even with the limited scope provided by the basic UI types, different applications that use ICTs may have vastly different implementations to support each type. To provide further extensibility and ease adoption of the ICT, each parameter object has an optional `customType` field. Contrary to the required `type` field, which must be populated from a standardized list of basic UI types, the `customType` field can be any arbitrary string label. Naming conventions and uniqueness are not enforced, but each custom type should be descriptive with the intent to be reusable. Custom types are intended to enhance the user experience when using a specific application, making the parameter easier to interact with or providing application-specific integrations. Each parameter should still be functional using just the basic UI type and custom types should not require any additional configurations options, besides the ones already provided for the basic types. 

A simple example of a useful custom type is an extension of the `select` type to support image-based selection options, instead of text-based ones. While the basic `select` type is functional and allows the user to select a parameter from an array of string options, adding images to each selection can provide the user with visual examples.

# Hardware Requirements

Hardware requirements are an optional component of the ICT specification that provide increased portability and reproducibility. This section covers three (3) aspects of analysis related hardware: CPU, memory, and GPU. By default, when no hardware requirements section is included, the ICT is assumed to work on any standard x86_64 machine without a dedicated graphics card.
<br><br>
| Field | Description | Example |
| ----- | ----------- | ------- |
| cpu.type | Any non-standard or specific processor limitations. | arm64 |
| cpu.min | Minimum requirement for CPU allocation where 1 CPU unit is equivalent to 1 physical CPU core or 1 virtual core. | 100m |
| cpu.recommended | Recommended requirement for CPU allocation for optimal performance. | 200m |
| memory.min | Minimum requirement for memory allocation, measured in bytes. | 129Mi |
| memory.recommended | Recommended requirement for memory allocation for optimal performance. | 200 Mi |
| gpu.enabled | Boolean value indicating if the plugin is optimized for GPU. | false |
| gpu.required | Boolean value indicating if the plugin requires a GPU to run. | false |
| gpu.type | Any identifying label for GPU hardware specificity. | cuda11 |
<br>

 Usage and intepretation of the hardware requirements are left to the discretion of each application or platform implementation that consumes ICTs. Hardware `recommended` fields are intended for facility administrators that may want to set strict limits in a distributed or shared environment, while still enabling optimal performance. Hardware `type` fields should be as generic or unrestricting as possible to enable portability. Plugin developers should make an effort to ensure that their code will work in many, if not most, environments. 
