
[Project management](../Project%20management.md)

# Contribute to SEAPATH

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to the SEAPATH project. These are mostly guidelines, sometimes rules. Use your best judgment, and feel free to propose changes to this document.

# Code of Conduct

This project applies the [LF Energy Code of Conduct](https://wiki.lfenergy.org/display/HOME/Code+of+Conduct). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project's Technical Steering Committee [SEAPATH-TSC@lists.lfenergy.org](mailto:SEAPATH-TSC@lists.lfenergy.org).

# How to contribute

There are many ways to contribute:

### Getting involved in the technical meetings

- By participating in the TSC meeting passively and/or actively so that you can provide technical advice, understand what the project priorities are, and identify contributions you could make. You can know when the next TSC meeting take place and eventually subscribe to the mailing list [here](https://zoom-lfx.platform.linuxfoundation.org/meetings/seapath).

### Developing

- Develop new features
- Correct bugs
- All contributions are valuables (ex : typos or rephrasing)
- See the [contributions guidelines](#code-contribution-guidelines-github) below

### Promoting the project

- Give talks on your experience on SEAPATH
- Add your page to the [Use cases on SEAPATH](../Who%20is%20using%20SEAPATH%20_.md) wiki page

### Reporting problems

- Find bugs and open GitHub issues
- Provide feedback on already opened pull requests
- New features or improvements/corrections to the project directly on [GitHub](https://github.com/seapath)

### Improving the documentation

- Write new wiki pages or improve the existing ones. Anyone can modify this wiki. You will need a Linux Foundation ID (created at <https://identity.linuxfoundation.org/> ) to contribute. In the upper right of this page, select Log In to contribute.
- Ask questions on the [mailing list](https://lists.lfenergy.org/g/SEAPATH) or on the [Slack channel](https://slack.lfenergy.org) when documentation is not clear or non-existent
- Add confluence comments on wiki pages
- Write troubleshooting guides about the problem you encountered

### Integrating new hardware and software

- Test SEAPATH on the hardware you have
- Integrate your software on SEAPATH (vIED)
- Share new tools around SEAPATH ecosystem (ex: IEC 61850 management tools)

# Code contribution guidelines (GitHub)

The code of the project is available [here](https://github.com/seapath)

## License and Developer Certificate of Origin

By contributing to the SEAPATH project, you accept and agree to the following terms and conditions for your present and future contributions submitted to SEAPATH.

All contributions to this project are licensed under the license stipulated at the corresponding sub-repository. Except where otherwise explicitly indicated, SEAPATH is an open source project licensed under the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

The project requires the use of the [Developer Certificate of Origin (DCO)](https://developercertificate.org/). The DCO is a legally binding statement asserting that you have the right to submit your contribution and to license it under the project's applicable license.

Contributors sign-off that they adhere to the term of the DCO by adding a `Signed-off-by` line to commit messages. The DCO sign-off must be attached to every contribution made by every contributor.

Here is an example `Signed-off-by` line, that indicates the contributor accepts the DCO:

```java
This is my commit message.

Signed-off-by: Name Surname <name.surname@entity.com>
```

You can write it manually but Git even has a -s command line option to append this automatically to your commit message:

```java
$ git commit -s -m 'This is my commit message'
```

Note that checks will be performed during the integration in order to require that commits in a Pull Request contain valid `Signed-off-by` lines.

## Style guides

- Follow the code style of the project, including indentation

## Git workflow guidelines

- Create a personal fork of the project on GitHub
- Clone the fork on your local machine
- Make sure to pull upstream changes into your local repository
- Implement/fix your feature, comment your code if needed
- Make sure to split your commit
- Squash intermediary commits (fixes, WIP, …) with git's interactive rebase
- Each commit should only add one feature
- Use two separate commits when adding a package and enabling it
- Make sure that your commit message is consistent with the git history
- Prefix the commit title by the area touch  ex: images/seapath-host-common.inc: add STONITH plugins
- Separate subject from body with a blank line
- Limit the subject line to 50 characters
- Use the imperative mood in the subject line
- Wrap the body at 72 characters
- Use the body to explain what and why vs. how
- Sign off your commit
- Push your branch to your fork on GitHub
- From your fork open a pull request

More details can be found [there](https://www.git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project#_commit_guidelines).

## Testing

- Run tests on the hardware you want to install the distribution and ensure that no regression are seen (ex: cukinia)
- Provide the hardware specification
- Write or adapt tests as needed
- When appicable a cukinia test must be provided for each new functionality

## Documentation

- Add or change the documentation as needed.

## English language convention

The convention for all the project's documents, including code documentation, website, is to write American English. A list of spelling differences between British and American English is available [here](https://www.britishcouncilfoundation.id/en/english/articles/british-and-american-english).
