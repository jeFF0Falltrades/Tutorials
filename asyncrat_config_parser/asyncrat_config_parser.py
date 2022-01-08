#!/usr/bin/python3
#
# asyncrat_config_parser.py
#
# Author: jeFF0Falltrades
#
# A configuration parser for the AsyncRAT malware family
# written in pure Python (3.x).
#
# Be aware that this parser was written as part of a tutorial to be used with
# the associated video, and prioritizes explicitness and clarity over
# performance.
#
# Feel free to slice it, dice it, and use it however it best works
# for you IAW with the license below.
#
# Please submit Issues and Pull Requests for bugs to the project homepage below.
#
# Feel free to also reach out to me on Twitter @jeFF0Falltrades with any
# feedback or issues.
#
# Homepage with Video Tutorial:
# https://github.com/jeFF0Falltrades/Tutorials/tree/master/asyncrat_config_parser
#
# YARA rule to find samples:
# https://github.com/jeFF0Falltrades/YARA-Signatures/blob/master/Broadbased/asyncrat.yar
#
#
# MIT License
#
# Copyright (c) 2022 Jeff Archer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from argparse import ArgumentParser
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from json import dumps
from logging import basicConfig, DEBUG, exception, getLogger, WARNING
from re import DOTALL, findall, search

logger = getLogger(__name__)


# An importable parser class which encompasses all operations for parsing and
# decrypting (unobfuscated) AsyncRAT payload configurations
class AsyncRATParser:

    OPCODE_RET = b'\x2a'
    PATTERN_CLR_METADATA_START = b'\x42\x53\x4a\x42'
    PATTERN_CONFIG_START = b'((?:\x72.{9}){9})'
    PATTERN_PARSED_RVAS = b'\x72(.{4})\x80(.{4})'
    RVA_STRINGS_BASE = 0x04000000
    RVA_US_BASE = 0x70000000
    STREAM_IDENTIFIER_STORAGE = b'#~'
    STREAM_IDENTIFIER_STRINGS = b'#Strings'
    STREAM_IDENTIFIER_US = b'#US'
    TABLE_FIELD = 'Field'

    # This map assists in calculating offsets for Field and FieldRVA entries.
    #
    # These calculations require knowing:
    #     1. The size of a row in the specified table (hardcoded here)
    #     2. The number of rows in the table (calculated in get_table_map())
    #
    # We have only hardcoded in row sizes through the FieldRVA table because
    # this is the last table we need for our parser to function.
    #
    # We still include the remaining tables because we will need to check if
    # these are present to calculate the offset to a table in get_table_start().
    #
    # If you are interested in generalizing this map to examine other tables,
    # I recommend checking out dnSpy's algorithm for calculating table row size
    # for the remaining tables here:
    #
    # https://github.com/dnSpy/dnSpy/blob/2b6dcfaf602fb8ca6462b8b6237fdfc0c74ad994/dnSpy/dnSpy/Hex/Files/DotNet/DotNetTableSizes.cs
    MAP_TABLE = {
        'Module': {
            'row_size': 10
        },
        'TypeRef': {
            'row_size': 6
        },
        'TypeDef': {
            'row_size': 14
        },
        'FieldPtr': {
            'row_size': 2
        },
        'Field': {
            'row_size': 6
        },
        'MethodPtr': {
            'row_size': 2
        },
        'Method': {
            'row_size': 14
        },
        'ParamPtr': {
            'row_size': 2
        },
        'Param': {
            'row_size': 6
        },
        'InterfaceImpl': {
            'row_size': 4
        },
        'MemberRef': {
            'row_size': 6
        },
        'Constant': {
            'row_size': 6
        },
        'CustomAttribute': {
            'row_size': 6
        },
        'FieldMarshal': {
            'row_size': 4
        },
        'DeclSecurity': {
            'row_size': 6
        },
        'ClassLayout': {
            'row_size': 8
        },
        'FieldLayout': {
            'row_size': 6
        },
        'StandAloneSig': {
            'row_size': 2
        },
        'EventMap': {
            'row_size': 4
        },
        'EventPtr': {
            'row_size': 2
        },
        'Event': {
            'row_size': 6
        },
        'PropertyMap': {
            'row_size': 4
        },
        'PropertyPtr': {
            'row_size': 2
        },
        'Property': {
            'row_size': 6
        },
        'MethodSemantics': {
            'row_size': 6
        },
        'MethodImpl': {
            'row_size': 6
        },
        'ModuleRef': {
            'row_size': 2
        },
        'TypeSpec': {
            'row_size': 2
        },
        'ImplMap': {
            'row_size': 8
        },
        'FieldRVA': {
            'row_size': 6
        },
        'ENCLog': {},
        'ENCMap': {},
        'Assembly': {},
        'AssemblyProcessor': {},
        'AssemblyOS': {},
        'AssemblyRef': {},
        'AssemblyRefProcessor': {},
        'AssemblyRefOS': {},
        'File': {},
        'ExportedType': {},
        'ManifestResource': {},
        'NestedClass': {},
        'GenericParam': {},
        'MethodSpec': {},
        'GenericParamConstraint': {},
        'Reserved 2D': {},
        'Reserved 2E': {},
        'Reserved 2F': {},
        'Document': {},
        'MethodDebugInformation': {},
        'LocalScope': {},
        'LocalVariable': {},
        'LocalConstant': {},
        'ImportScope': {},
        'StateMachineMethod': {},
        'CustomDebugInformation': {},
        'Reserved 38': {},
        'Reserved 39': {},
        'Reserved 3A': {},
        'Reserved 3B': {},
        'Reserved 3C': {},
        'Reserved 3D': {},
        'Reserved 3E': {},
        'Reserved 3F': {}
    }

    # This nested class encapsulates all operations around parsing AES
    # decryption data from the file (e.g. key, salt, iterations, sizes) and
    # exposes a decrypt() method that our parent parser can use.
    #
    # TBF, it is not necessary to encapsulate these into an inner class like
    # this, but I think it helps organize the code a bit better.
    class ASyncRATAESDecryptor:
        OPCODE_LDSTR = b'\x72'
        OPCODE_LDTOKEN = b'\xd0'
        PATTERN_AES_KEY = b'\x7e(.\x00\x00\x04)\x73'
        PATTERN_AES_KEY_AND_BLOCK_SIZE = b'\x07\x20(.{4})\x6f.{4}\x07\x20(.{4})'
        PATTERN_AES_METADATA = b'\x73.{4}\x7a\x03\x7e(.{4})'
        PATTERN_AES_SALT_INIT = b'\x80%b\x2a'
        SECTION_IDENTIFIER_TEXT = b'.text'
        TABLE_FIELD_RVA = 'FieldRVA'

        # We pass our parser in as parent_parser so that we can access all of
        # its attributes and methods from our inner class via self.parent
        def __init__(self, parent_parser):
            self.parent = parent_parser
            self.aes_metadata_flag = self.get_aes_metadata_flag()
            self.key_size, self.block_size = self.get_aes_key_and_block_size()
            self.iterations = self.get_aes_iterations()
            self.salt = self.get_aes_salt()
            # Call this last as we need the above attributes to derive the key
            self.key = self.get_aes_key()

        # Given an initialization vector and ciphertext, creates a Cipher
        # object with the AES key and specified IV and decrypts the ciphertext
        def decrypt(self, iv, ciphertext):
            logger.debug(
                f'Decrypting {ciphertext} with key {self.key} and IV {iv}...')
            aes_cipher = Cipher(AES(self.key), CBC(iv))
            decryptor = aes_cipher.decryptor()
            # Use a PKCS7 unpadder to remove padding from decrypted value
            # https://cryptography.io/en/latest/hazmat/primitives/padding/
            unpadder = PKCS7(self.block_size).unpadder()
            try:
                padded_text = decryptor.update(
                    ciphertext) + decryptor.finalize()
                unpadded_text = unpadder.update(
                    padded_text) + unpadder.finalize()
            except Exception as e:
                raise self.parent.ASyncRATParserError(
                    f'Error decrypting ciphertext {ciphertext} with IV {iv} and key {self.key}'
                ) from e
            logger.debug(f'Decryption result: {unpadded_text}')
            return unpadded_text

        # Given a field ID from the Field table, returns the relative virtual
        # address of the field, e.g.:
        #
        # Field RVA: 0x0400001D
        # Field ID = 0x1D
        # FieldRVA Entry for Field ID: 0x1D : 0x2050
        # Final RVA: 0x2050
        def field_id_to_field_rva(self, id):
            fieldrva_table_start = self.parent.get_table_start(
                self.TABLE_FIELD_RVA)
            field_rva = None
            matched = False
            # Start at the beginning of the FieldRVA table
            cur_offset = fieldrva_table_start
            for x in range(
                    self.parent.table_map[self.TABLE_FIELD_RVA]['num_rows']):
                try:
                    field_id = self.parent.bytes_to_int(
                        self.parent.data[cur_offset + 4:cur_offset + 6])
                    field_rva = self.parent.bytes_to_int(
                        self.parent.data[cur_offset:cur_offset + 4])
                    # Break if our matching ID is found in this row
                    if field_id == id:
                        matched = True
                        break
                    # Otherwise, keep moving through the table
                    cur_offset += self.parent.table_map[
                        self.TABLE_FIELD_RVA]['row_size']
                except Exception as e:
                    raise self.parent.ASyncRATParserError(
                        f'Error parsing FieldRVA corresponding to ID {id}'
                    ) from e
            # If we never found our match, raise an exception
            if not matched:
                raise self.parent.ASyncRATParserError(
                    f'Could not find FieldRVA corresponding to ID {id}')
            return field_rva

        # Given an RVA from the FieldRVA table, calculates the file offset of
        # the field value by subtracting the relative virtual address of the
        # .text section and adding the file offset of the .text section, e.g.
        #
        # Field RVA: 0x2050
        # Text section RVA: 0x2000
        # Text section file offset: 0x0200
        # Field offset = 0x2050 - 0x2000 + 0x0200
        #             = 0x0250
        def field_rva_to_offset(self, field_rva):
            text_section_metadata_offset = self.parent.data.find(
                self.SECTION_IDENTIFIER_TEXT)
            text_section_rva = self.parent.data[
                text_section_metadata_offset +
                12:text_section_metadata_offset + 16]
            text_section_offset = self.parent.data[
                text_section_metadata_offset +
                20:text_section_metadata_offset + 24]
            field_offset = field_rva - self.parent.bytes_to_int(
                text_section_rva) + self.parent.bytes_to_int(
                    text_section_offset)
            return field_offset

        # Extracts the AES iteration number from the payload
        def get_aes_iterations(self):
            logger.debug('Extracting AES iterations...')
            iterations_offset_start = self.aes_metadata_flag.end() + 1
            iterations_val_packed = self.parent.data[
                iterations_offset_start:iterations_offset_start + 2]
            iterations = self.parent.bytes_to_int(iterations_val_packed)
            logger.debug(f'Found AES iteration number of {iterations}')
            return iterations

        # Identifies the initialization of the AES256 object in the payload by
        # looking for the following ops:
        #
        # newobj	instance void [mscorlib]System.ArgumentException...
        # throw
        # ldarg.1
        # ldsfld	uint8[] Client.Algorithm.Aes256::Salt
        def get_aes_metadata_flag(self):
            logger.debug('Extracting AES metadata flag...')
            # Important to use DOTALL here (and with all regex ops to be safe)
            # as we are working with bytes, and if we do not set this, and the
            # byte sequence contains a byte that equates to a newline
            # (\n or 0x0A), the search will fail
            md_flag_offset = search(self.PATTERN_AES_METADATA,
                                    self.parent.data, DOTALL)
            if md_flag_offset is None:
                raise self.parent.ASyncRATParserError(
                    'Could not identify AES metadata flag')
            logger.debug(
                f'AES metadata flag found at offset {hex(md_flag_offset.start())}'
            )
            return md_flag_offset

        # Extracts the AES key from the payload using a regex pattern which
        # looks for the initialization of the key - specifically, the following
        # ops:
        #
        # ldsfld    string Client.Settings::Key
        # newobj    instance void Client.Algorithm.Aes256::.ctor(string)
        def get_aes_key(self):
            logger.debug('Extracting encoded AES key value...')
            hit = search(self.PATTERN_AES_KEY, self.parent.data, DOTALL)
            if hit is None:
                raise self.parent.ASyncRATParserError(
                    'Could not find AES key pattern')

            # Since we already have a map of all fields, and have translated
            # config values (including Key) into translated_config, to find the
            # key value, we take the RVA of the key, subtract the #Strings
            # stream base RVA, and then subtract 1 to get the key's index in
            # the field map.
            #
            # We then take the key field name from the field map, and look up
            # its value in our translated config, e.g.:
            #
            # Key RVA: 0x04000007
            # Key Field Map Index = 0x04000007 - 0x04000000 - 1 = 6
            # Key Field Name Value = fields_map[6]
            # Key Value = translated_config[fields_map[6]]
            key_field_offset = self.parent.bytes_to_int(
                hit.groups()[0]) - self.parent.RVA_STRINGS_BASE - 1
            key_field_name = self.parent.fields_map[key_field_offset][0]
            key_val = self.parent.translated_config[key_field_name]
            logger.debug(f'AES encoded key value found: {key_val}')
            try:
                passphrase = b64decode(key_val)
            except Exception as e:
                raise self.parent.ASyncRATParserError(
                    f'Error decoding key value {key_val}') from e
            logger.debug(f'AES passphrase found: {passphrase}')
            kdf = PBKDF2HMAC(SHA1(),
                             length=self.key_size,
                             salt=self.salt,
                             iterations=self.iterations)
            try:
                key = kdf.derive(passphrase)
            except Exception as e:
                raise self.parent.ASyncRATParserError(
                    f'Error deriving key from passphrase {passphrase}') from e
            logger.debug(f'AES key derived: {key.hex()}')
            return key

        # Extracts the AES key and block size from the payload
        def get_aes_key_and_block_size(self):
            logger.debug('Extracting AES key and block size...')
            hit = search(self.PATTERN_AES_KEY_AND_BLOCK_SIZE, self.parent.data,
                         DOTALL)
            if hit is None:
                raise self.parent.ASyncRATParserError(
                    f'Could not extract AES key or block size')
            # Convert key size from bits to bytes by dividing by 8
            # Note use of // instead of / to ensure integer output, not float
            key_size = self.parent.bytes_to_int(hit.groups()[0]) // 8
            block_size = self.parent.bytes_to_int(hit.groups()[1])
            logger.debug(
                f'Found key size {key_size} and block size {block_size}')
            return key_size, block_size

        # Extracts the AES salt from the payload, accounting for both hardcoded
        # salt byte arrays, and salts derived from hardcoded strings
        def get_aes_salt(self):
            logger.debug('Extracting AES salt value...')
            # The Salt RVA was captured in our metadata flag pattern
            aes_salt_rva = self.aes_metadata_flag.groups()[0]
            # Use % to insert our salt RVA into our match pattern
            # This pattern will then find the salt initialization ops,
            # specifically:
            #
            # stsfld	uint8[] Client.Algorithm.Aes256::Salt
            # ret
            aes_salt_initialization = self.parent.data.find(
                self.PATTERN_AES_SALT_INIT % aes_salt_rva)
            if aes_salt_initialization == -1:
                raise self.parent.ASyncRATParserError(
                    'Could not identify AES salt initialization')

            # Look at opcode used to initialize the salt to decide how to
            # proceed on extracting the salt value (start of pattern - 10 bytes)
            salt_op_offset = aes_salt_initialization - 10
            # Need to use bytes([int]) here to properly convert from int to byte
            # string for our comparison below
            salt_op = bytes([self.parent.data[salt_op_offset]])

            # Get the salt RVA from the 4 bytes following the initialization op
            salt_strings_rva_packed = self.parent.data[salt_op_offset +
                                                       1:salt_op_offset + 5]
            salt_strings_rva = self.parent.bytes_to_int(
                salt_strings_rva_packed)

            # If the op is a ldstr op, just get the bytes value of the string
            # being used to initialize the salt
            if salt_op == self.OPCODE_LDSTR:
                salt_encoded = self.parent.us_rva_to_us_val(salt_strings_rva)
                # We use decode_bytes() here to get the salt string without any
                # null bytes (because it's stored as UTF-16LE), then convert it
                # back to bytes
                salt = self.parent.decode_bytes(salt_encoded).encode()
            # If the op is a ldtoken operation, we need to get the salt byte
            # array value from the FieldRVA table
            elif salt_op == self.OPCODE_LDTOKEN:
                salt = self.get_aes_salt_ldtoken_method(
                    salt_strings_rva, salt_op_offset)
            else:
                raise self.parent.ASyncRATParserError(
                    f'Unknown salt opcode found: {salt_op.hex()}')
            logger.debug(f'Found salt value: {salt.hex()}')
            return salt

        # Derives the AES salt by loading the RVA of the salt from
        # the FieldRVA table, converting it to a file offset, and
        # reading the salt value from that offset
        def get_aes_salt_ldtoken_method(self, salt_strings_rva,
                                        salt_op_offset):
            salt_size = self.parent.data[salt_op_offset - 7]
            # Salt field ID = Salt strings RVA - #Strings RVA base
            salt_field_id = salt_strings_rva - self.parent.RVA_STRINGS_BASE
            salt_field_rva = self.field_id_to_field_rva(salt_field_id)
            salt_offset = self.field_rva_to_offset(salt_field_rva)
            salt_value = self.parent.data[salt_offset:salt_offset + salt_size]
            return salt_value

    # Custom exception class to provide detailed exceptions from the parser
    class ASyncRATParserError(Exception):
        pass

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.get_file_data(file_path)
        self.table_map = self.get_table_map()
        self.fields_map = self.get_fields_map()
        self.config_addr_map = self.get_config_address_map()
        self.translated_config = self.get_translated_config()
        self.aes_decryptor = self.ASyncRATAESDecryptor(self)
        self.config = self.decrypt_config()

    # Converts a bytes object to an int object using the specified byte order
    # (little-endian by default)
    def bytes_to_int(self, bytes, order='little'):
        try:
            result = int.from_bytes(bytes, byteorder=order)
        except Exception as e:
            raise self.ASyncRATParserError(
                f'Error parsing int from value: {bytes}') from e
        return result

    # Decodes a bytes object to a Unicode string, using UTF-16LE for byte values
    # with null bytes still embedded in them, and UTF-8 for all other values
    def decode_bytes(self, bytes):
        result = None
        try:
            if b'\x00' in bytes:
                result = bytes.decode('utf-16le')
            else:
                result = bytes.decode('utf-8')
        except Exception as e:
            raise self.ASyncRATParserError(
                f'Error decoding bytes object to Unicode: {bytes}') from e
        return result

    # Given a translated config containing config field names and encrypted
    # and/or base64-encoded field values, decodes and decrypts encrypted values
    # and returns the decrypted config
    def decrypt_config(self):
        logger.debug('Decrypting config...')
        decrypted_config = {}
        for k, v in self.translated_config.items():
            # We convert config field names and values from bytes to Unicode
            # strings for compatibility with JSON output
            decoded_k = self.decode_bytes(k)
            b64_exception = False
            decrypted_config[decoded_k] = self.decode_bytes(v)

            # Leave empty strings as they are
            if len(v) == 0:
                continue
            # Check if base64-encoded string
            try:
                decoded_val = b64decode(v)
            except Exception:
                b64_exception = True
            # If it was not base64-encoded, or if it is less than our min length
            # for ciphertext, leave the value as it is
            if b64_exception or len(decoded_val) < 48:
                continue
            # Otherwise, extract the IV from the 16 bytes after the HMAC
            # (first 32 bytes) and the ciphertext from the rest of the data
            # after the IV, and run the decryption
            (iv, ciphertext) = decoded_val[32:48], decoded_val[48:]
            decrypted_config[decoded_k] = self.decode_bytes(
                self.aes_decryptor.decrypt(iv, ciphertext))
            logger.debug(
                f'Key: {decoded_k}, Value: {decrypted_config[decoded_k]}')
        logger.debug('Successfully decrypted config')
        return decrypted_config

    # Searches for the AsyncRAT configuration section in the Settings module,
    # and attempts to extract the RVAs of the config field names and values
    #
    # Specifically, looks for ldstr used >= 9 times in a row
    def get_config_address_map(self):
        logger.debug('Extracting the config address map...')
        config_mappings = []
        hit = search(self.PATTERN_CONFIG_START, self.data, DOTALL)
        if hit is None:
            raise self.ASyncRATParserError('Could not find start of config')
        config_start = hit.start()
        # Configuration ends with ret operation, so we get string using the ret
        # opcode (0x2A) as our terminating char
        parsed_ops = self.get_string_from_offset(config_start, self.OPCODE_RET)
        # Split the field name RVAs from the field value RVAs in our parsed ops
        parsed_rvas = findall(self.PATTERN_PARSED_RVAS, parsed_ops, DOTALL)
        for (us_rva, string_rva) in parsed_rvas:
            config_value_rva = self.bytes_to_int(us_rva)
            config_name_rva = self.bytes_to_int(string_rva)
            logger.debug(
                f'Found config item: ({hex(config_value_rva)}, {hex(config_name_rva)})'
            )
            config_mappings.append((config_value_rva, config_name_rva))
        logger.debug('Successfully extracted config address map')
        return config_mappings

    # Extracts the Field table of the assembly, mapping the value of each
    # field from the #Strings stream to its offset in the Field table
    def get_fields_map(self):
        logger.debug('Extracting fields map...')
        fields_map = []
        fields_start = self.get_table_start(self.TABLE_FIELD)
        strings_start = self.get_stream_start(self.STREAM_IDENTIFIER_STRINGS)
        # Start at the beginning of the Field table
        cur_offset = fields_start
        for x in range(self.table_map[self.TABLE_FIELD]['num_rows']):
            try:
                field_offset = self.bytes_to_int(self.data[cur_offset +
                                                           2:cur_offset + 4])
                field_value = self.get_string_from_offset(strings_start +
                                                          field_offset)
                # Proceed to next row
                cur_offset += self.table_map[self.TABLE_FIELD]['row_size']
            except Exception as e:
                raise self.ASyncRATParserError(
                    'Error parsing Field table') from e
            logger.debug(f'Found field: {hex(field_offset)}, {field_value}')
            fields_map.append((field_value, field_offset))
        logger.debug('Successfully extracted fields map')
        return fields_map

    # Given a file path, reads in and returns binary contents from that path
    def get_file_data(self, file_path):
        logger.debug(f'Reading contents from: {file_path}')
        try:
            with open(file_path, 'rb') as fp:
                data = fp.read()
        except Exception as e:
            raise self.ASyncRATParserError(
                f'Error reading from path: {file_path}') from e
        logger.debug(f'Successfully read data')
        return data

    # Extracts the m_maskvalid value from the Tables Stream
    def get_mask_valid(self):
        logger.debug('Extracting m_maskvalid value...')
        storage_stream_offset = self.get_stream_start(
            self.STREAM_IDENTIFIER_STORAGE)
        mask_valid_offset = storage_stream_offset + 8
        mask_valid = self.bytes_to_int(
            self.data[mask_valid_offset:mask_valid_offset + 8])
        logger.debug(f'Extracted m_maskvalid: {hex(mask_valid)}')
        return mask_valid

    # Finds the start of the Common Language Runtime (CLR) metadata header
    # using the metadata start flag (0x424a5342)
    def get_metadata_header_offset(self):
        hit = self.data.find(self.PATTERN_CLR_METADATA_START)
        if hit == -1:
            raise self.ASyncRATParserError(
                'Could not find start of CLR metadata header')
        return hit

    # Given a stream identifier (e.g. #Strings or #US), finds the file offset
    # of the start of the stream
    def get_stream_start(self, stream_identifier):
        metadata_header_offset = self.get_metadata_header_offset()
        hit = self.data.find(stream_identifier)
        if hit == -1:
            raise self.ASyncRATParserError(
                f'Could not find offset of stream {stream_identifier}')
        stream_offset = self.bytes_to_int(self.data[hit - 8:hit - 4])
        return metadata_header_offset + stream_offset

    # Given a string offset and, optionally, a delimiter (default terminating
    # null byte), extracts a string from the offset
    def get_string_from_offset(self, str_offset, delimiter=b'\0'):
        try:
            result = self.data[str_offset:].partition(delimiter)[0]
        except Exception as e:
            raise self.ASyncRATParserError(
                f'Could not extract string value from offset {hex(str_offset)} with delimiter {delimiter}'
            ) from e
        return result

    # Creates a copy of the table map template above and populates it with
    # extracted table data from the payload, including tables present and
    # number of rows per table
    def get_table_map(self):
        logger.debug('Extracting table map...')
        mask_valid = self.get_mask_valid()
        # Ensure we use copy() here because, if not, every newly instantiated
        # AsyncRATParser object will have the same table map, and changes to
        # one will impact all others
        table_map = self.MAP_TABLE.copy()
        storage_stream_offset = self.get_stream_start(
            self.STREAM_IDENTIFIER_STORAGE)
        # Table row counts start 24 bytes after storage stream start
        table_start = storage_stream_offset + 24
        cur_offset = table_start
        try:
            for table in table_map:
                # m_maskvalid tells us which tables are present in this
                # particular assembly, with each table receiving one bit in the
                # mask. If this bit is set to 1, the table is present.
                #
                # So to check for table presence, we use the bitwise formula:
                #
                # Table Present = m_maskvalid AND (2^table index)
                if mask_valid & (2**list(table_map.keys()).index(table)):
                    row_count_packed = self.data[cur_offset:cur_offset + 4]
                    row_count = self.bytes_to_int(row_count_packed)
                    table_map[table]['num_rows'] = row_count
                    logger.debug(f'Found {row_count} rows for table {table}')
                    cur_offset += 4
                else:
                    table_map[table]['num_rows'] = 0
        except Exception as e:
            raise self.ASyncRATParserError(
                'Could not get counts of rows from tables') from e
        logger.debug('Successfully extracted table map')
        return table_map

    # Given the name of a table in the Tables Stream, finds the offset pointing
    # to the start of that table
    def get_table_start(self, table_name):
        storage_stream_offset = self.get_stream_start(
            self.STREAM_IDENTIFIER_STORAGE)
        # Table Start = Table Stream Start + 4 bytes for the row size of each
        #               table present in the assembly
        #             = (24 + Storage stream start) + (4 * each table present
        #               in the assembly)
        tables_start_offset = storage_stream_offset + 24 + (4 * len([
            table for table in self.table_map
            if self.table_map[table]['num_rows'] > 0
        ]))

        table_offset = tables_start_offset
        for table in self.table_map:
            # Break if we have found our table
            if table == table_name:
                break
            # If we no longer find 'row_size', we are past the point we should
            # be, at least for our parser, as that means we've passed the
            # FieldRVA table
            elif 'row_size' not in self.table_map[table]:
                raise self.ASyncRATParserError('Invalid table offset found')
            # Increment by (row size * number of rows in current table) bytes
            table_offset += self.table_map[table]['row_size'] * self.table_map[
                table]['num_rows']
        return table_offset

    # Translates encrypted config addresses to their values from their RVAs
    def get_translated_config(self):
        logger.debug('Translating configuration addresses to values...')
        translated_config = {}
        for (us_rva, strings_rva) in self.config_addr_map:
            try:
                field_name = self.strings_rva_to_strings_val(strings_rva)
                field_value = self.us_rva_to_us_val(us_rva)
                logger.debug(
                    f'Found config value: {field_name} = {field_value}')
                translated_config[field_name] = field_value
            except Exception as e:
                raise self.ASyncRATParserError(
                    f'Error translating RVAs {us_rva} and {strings_rva}'
                ) from e
        logger.debug('Successfully translated configuration')
        return translated_config

    # Returns a JSON dump of metadata and the decrypted configuration for a
    # payload
    def report(self):
        result_dict = {
            'file_path': self.file_path,
            'aes_key': self.aes_decryptor.key.hex(),
            'aes_salt': self.aes_decryptor.salt.hex(),
            'config': self.config
        }
        return dumps(result_dict)

    # Given an RVA from the #Strings stream, extracts the value of the string
    # at that RVA
    def strings_rva_to_strings_val(self, strings_rva):
        strings_start = self.get_stream_start(self.STREAM_IDENTIFIER_STRINGS)
        # Index of value in fields_map = RVA - #Strings base RVA - 1, e.g.:
        #
        # RVA: 0x04000001
        # Index = 0x04000001 - 0x04000000 - 1 = 0
        val_index = strings_rva - self.RVA_STRINGS_BASE - 1
        # Get offset from #Strings stream start from fields map and add it to
        # #Strings stream base to get the file offset of the string
        try:
            val_offset = self.fields_map[val_index][1] + strings_start
        except Exception as e:
            raise self.ASyncRATParserError(
                f'Could not retrieve string from RVA {strings_rva}') from e
        strings_val = self.get_string_from_offset(val_offset)
        return strings_val

    # Given an RVA from the #US stream, extracts the value of the string
    # at that RVA
    def us_rva_to_us_val(self, us_rva):
        us_start = self.get_stream_start(self.STREAM_IDENTIFIER_US)
        # Strings in the #US stream are prefaced with 1-2 length bytes
        #
        # If the length of the string is >= 128 bytes, 2 bytes will be used
        # to indicate length, and the first byte's most significant bit will be
        # set.
        #
        # So we first check if the first length byte & 0x80 (1000 0000) is 1.
        #
        # If so, then this indicates we are dealing with a long string, and we
        # grab the size from 2 length bytes instead of 1.
        #
        # If not, then we can assume there is only 1 length byte to read from
        # and then skip over it to get to the string
        length_byte_offset = us_rva - self.RVA_US_BASE + us_start
        if int(self.data[length_byte_offset]) & 0x80:
            val_offset = 2
            # Notice we use big-endianness here, and also that we subtract the
            # most significant bit of the two length bytes (0x8000 or 1000 0000
            # 0000 0000) serving as a flag
            val_size = self.bytes_to_int(
                self.data[length_byte_offset:length_byte_offset + 2],
                'big') - 0x8000
        else:
            val_offset = 1
            val_size = self.data[length_byte_offset]
        val_offset += length_byte_offset
        # Subtract 1 to account for null terminator at the end of the string
        us_val = self.data[val_offset:val_offset + val_size - 1]
        return us_val


if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument(
        'file_paths',
        nargs='+',
        help='One or more AsyncRAT payload file paths (deobfuscated)')
    ap.add_argument('-d',
                    '--debug',
                    action='store_true',
                    help='Enable debug logging')
    args = ap.parse_args()
    if args.debug:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=WARNING)
    for fp in args.file_paths:
        try:
            print(AsyncRATParser(fp).report())
        except Exception as e:
            exception(f'Exception occurred for {fp}', exc_info=True)
            continue
