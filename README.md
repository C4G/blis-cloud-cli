# blis-cloud-cli

A tool for managing cloud installations of [BLIS](http://blis.cc.gatech.edu/index.php).

## Proposal

Installing BLIS ([installation guide here](https://c4g.github.io/BLIS)) on a cloud server is a little difficult.
There is a [bootstrap script](https://github.com/C4G/BLIS/blob/master/docker/bootstrap.sh) that can automate some of the process, but it cannot recover
if there is a problem.

Additionally, when there is a problem with the installation of BLIS on a cloud server, there are limited tools available for debugging it, and the
technical knowledge of the operator is varied.

For these reasons, I want to create a new version of the BLIS installation and management tool to simplify this process.

## Proposed Features & Requirements

### Language

The BLIS cloud tool will be written in Python due to its widespread use and ease of development.

### Installation

The tool should be installed with a system-level package manager. Possibilities are creating a Debian package, or perhaps a Python package that can be installed with
`pip install`.

### BLIS Installation Mode

There should be a command (eg. `blis install`) that replaces the current bootstrap script and performs all the necessary steps to install BLIS, prompting the user for input
only if necessary.

### BLIS Diagnostic Mode

There should be a command (eg. `blis doctor`) that will perform a BLIS diagnostic test to ensure it is running properly. This should check for example:

- Whether or not the BLIS and database containers are running
- Whether the BLIS container is responding on port 80
- Whether the database container is healthy
- Whether there are any major errors in the BLIS log

A report should be generated that can be copy-and-pasted or otherwise sent to the BLIS team if there is a problem with these criteria.

### BLIS Migration Mode

The tool should assist country directors with migrating labs to the cloud instance. This behavior still needs to be thought out and designed.
