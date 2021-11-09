# Changelog
All notable changes in **salt-lint** are documented below.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.8.0] (2021-11-09)
### Fixed
- False positive when detecting missing spaces in Jinja variables when the Jinja statement is nested in literal braces ([#272](https://github.com/warpnet/salt-lint/pull/272)).
- Ensure a single missing quote in the file mode is also detected as incorrect quotation of a file mode ([#273](https://github.com/warpnet/salt-lint/pull/273)).
- Ignore non file mode arguments for the file mode quotation and leading zero checks ([#274](https://github.com/warpnet/salt-lint/pull/274)).

## [0.7.0] (2021-11-01)
### Added
- Add Python 3.10 support ([#265](https://github.com/warpnet/salt-lint/pull/265)).
- Add initial man page ([#270](https://github.com/warpnet/salt-lint/pull/270)).

### Fixed
- Close temporary file after writing to STDIN ([#263](https://github.com/warpnet/salt-lint/pull/263)).

## [0.6.1] (2021-06-01)
### Removed
- Remove rule 218 because of a false positive

## [0.6.0] (2021-06-01)
### Deprecated
- Drop Python 2.7 support ([#239](https://github.com/warpnet/salt-lint/pull/239)).

### Added
- Rule 216, 217 and 218 for catching common typographical errors ([#249](https://github.com/warpnet/salt-lint/pull/249)).

## [0.5.2] (2021-01-29)
### Fixed
- Append the contents of the `CHANGELOG.md` file to the long description of the package instead of the duplicate `README.md` contents ([#234](https://github.com/warpnet/salt-lint/pull/234)).
- Ignore Jinja specific rules in Jinja escaped blocks ([#236](https://github.com/warpnet/salt-lint/pull/236)).

## [0.5.1] (2021-01-19)
### Fixed
- Ensure all excluded paths from both the CLI and configuration are passed to the runner ([#231](https://github.com/warpnet/salt-lint/pull/231)).

## [0.5.0] (2021-01-17)
### Added
- Rule 213 to recommend using cmd.run together with onchanges ([#207](https://github.com/warpnet/salt-lint/pull/207)).
- Rule 214 to check SLS file with a period in the name (besides the suffix period) as they can not be referenced by Salt ([#209](https://github.com/warpnet/salt-lint/pull/209)).
- Rules 901-915 to check for deprecated states and state options ([#214](https://github.com/warpnet/salt-lint/pull/214)).
- This `CHANGELOG.md` file to be able to list all notable changes for each version of **salt-lint** ([#223](https://github.com/warpnet/salt-lint/pull/223)).

[Unreleased]: https://github.com/warpnet/salt-lint/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/warpnet/salt-lint/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/warpnet/salt-lint/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/warpnet/salt-lint/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/warpnet/salt-lint/compare/v0.5.2...v0.6.0
[0.5.2]: https://github.com/warpnet/salt-lint/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/warpnet/salt-lint/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/warpnet/salt-lint/compare/v0.4.2...v0.5.0
