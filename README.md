# open-xpd-uuid-lib
A library of common functions used when creating and managing open-xpd-uuid, 
a common, globally-unique name space (uuid) for Product Declarations, including HPDs and EPDs, 
to help users find all environmental and health information related to a single product.
# Open xPD UUID (short readable GUIDs)
`open-xpd-uuid` is a string that consists of 8 or 10 (8+2) alpha-numeric characters and any number of dashes. 
For example: `123ABCED`, `123ABCEDAR`, `ASB21M01`, `avbDK93S`, `-AB-11-cc-Ll---`.
GUIDs that consists of the following characters `1234567890ABCDEFGHJKMNPRQRSTUVWXYZ` (`L` and `O` are not mentioned) 
are called "canonical". For example: `12345678`, `ABCDEFG1`, `123ABCEDAR`.
GUIDs that consists of 10 characters represent 8-character guid with appended 2-character checksum.
Checksum allows to detect 1-character entry errors and character swaps, and most other errors.
## Character treatment
* `-` or dash - is ignored
* `L` or `l` or `I` or `i` - is treated as `1`
* `O` or `o` - is treated as `0`(zero)
 
# Install
`pip install open-xpd-uuid-lib`

# Supported versions
The library supports `python 3.6` and higher.

# Usage
## Generate short readable GUID
```pycon
>>> from cqd import open_xpd_uuid
>>> open_xpd_uuid.generate()
'JKGEE5PN'
```
## Generate short readable GUID starting with specific characters set (prefix)
```pycon
>>> from cqd import open_xpd_uuid
>>> open_xpd_uuid.generate('CQD')
'CQD55PG0'
```
## Sanitize short readable GUIDs
Use `sanitize` to replace ambiguous chars(_0,o,O,1,L,l,I,i_) with correct ones and remove dashes(_-_).
This function is useful to turn guid received from a user into a canonical one.

For example: `as-b2-lm-oL` -> `ASB21M01`
```pycon
>>> from cqd import open_xpd_uuid
>>> open_xpd_uuid.sanitize('as-b2-lm-oL')
'ASB21M01'
```
## Validate short readable GUID
Use `validate` to validate short readable GUID and get error description if the GUID is not valid.
`validate` __accepts only__ "canonical" GUIDs: use `sanitize` function to make them "canonical".
```pycon
>>> from cqd import open_xpd_uuid
>>> sanitized_guid = open_xpd_uuid.sanitize('as-b2-lm-oL')
>>> sanitized_guid
'ASB21M01'
>>> open_xpd_uuid.validate(sanitized_guid)
# no exception - the `sanitized_guid` is valid

>>> try:
...     open_xpd_uuid.validate('as-b2-lm-oL')
... except open_xpd_uuid.GuidValidationError as e:
...     print(e)
...     
`guid` length must be 8 characters long
```

## Generate and use checksum
```pycon
>>> from cqd import open_xpd_uuid
>>> guid = open_xpd_uuid.generate()
'JKGEE5PN'
>>> checksum = open_xpd_uuid.checksum(guid)
'ME'
>>> guid_with_checksum = guid + checksum
'JKGEE5PNME'
>>> short_link = 'cqd.io/e/' + guid_with_checksum
'cqd.io/e/JKGEE5PNME'
```
