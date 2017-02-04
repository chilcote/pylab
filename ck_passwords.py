#!/usr/bin/python
#ref: https://gist.github.com/pudquick/8d3dedc337161b187a8a1c9564c83463

# For an alternative method, check out:
# https://gist.github.com/pudquick/3ff4278c609ce223ebb4fc300c5edd0f

from Foundation import NSBundle, NSClassFromString
SafariShared = NSBundle.bundleWithPath_('/System/Library/PrivateFrameworks/SafariShared.framework')
loaded = SafariShared.load()
WBSPasswordGeneration = NSClassFromString('WBSPasswordGeneration')
CKRecord              = NSClassFromString('CKRecord')

def generate_password(requirements=None):
    rec = CKRecord.alloc().initWithRecordType_('pudquick_passwordgen')
    if requirements is not None:
        # dictionary of values to set passed in
        rec.setValuesForKeysWithDictionary_(requirements)
    password = WBSPasswordGeneration.generatedPasswordMatchingRequirements_(rec)
    # Do a little cleanup, since we don't actually want to save any CloudKit records
    del rec
    return password

# Example usage
# >>> generate_password()
# u'hhs-o7X-kaZ-ngw'
# Returns an iCloud Keychain suggested password in the style seen here:
# https://support.apple.com/library/APPLE/APPLECARE_ALLGEOS/Product_Help/en_US/PUBLIC_USERS/PL124/S0700_CloudKeychain.png

# Alternatively, you can define various keys in a dictionary and pass it in
# >>> r = {
# >>>      'PasswordMinLength': 20,
# >>>      'PasswordMaxLength': 20, # These keys only seem to force length if you set them both to the same value
# >>>      'PasswordRequiredCharacters': ['abc','123','!@#$', 'XYZ'],
# >>>      'PasswordAllowedCharacters': "abc123!@#$XYZ", # allowed characters has to be set if you're requiring sets
# >>>      'PasswordFirstCharacterCandidates': '1a',
# >>>     }
# u'11b1c#Z31Y2!b#Z$ZZ#X'

print generate_password()
