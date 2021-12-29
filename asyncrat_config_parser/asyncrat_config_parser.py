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
# Feel free to also reach out to me on Twitter @jeFF0Falltrades with any
# feedback or issues.
#
# Homepage with Video Tutorial:
# https://github.com/jeFF0Falltrades/Game-Patches/tree/master/asyncrat_config_parser
#
# YARA rule to find samples:
# https://github.com/jeFF0Falltrades/YARA-Signatures/blob/master/Broadbased/asyncrat.yar
#
#
# MIT License
#
# Copyright (c) 2021 Jeff Archer
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
from logging import basicConfig, DEBUG, getLogger
from re import DOTALL, findall, search
from traceback import format_exc

logger = getLogger(__name__)


# An importable parser class which encompasses all operations for parsing and
# decrypting (unobfuscated) AsyncRAT payload configurations
class AsyncRATParser:

    AES_BLOCK_SIZE = 128
    AES_ITERATIONS = 50000
    AES_KEY_LENGTH = 32
    AES_SALT_LENGTH = 32
    BYTE_ORDER = 'little'
    OPCODE_LDSTR = b'\x72'
    OPCODE_RET = b'\x2a'
    PATTERN_CONFIG_START = b'((?:\x72.{9}){9})'
    PATTERN_AES_KEY = b'\x7e(.\x00\x00\x04)\x73'
    PATTERN_METADATA_START = b'\x42\x53\x4a\x42'
    PATTERN_PARSED_RVAS = b'\x72(.{4})\x80(.{4})'
    PATTERN_PRE_SALT_RVA = b'\x8d.{4}\x25\xd0'
    RVA_STRINGS_BASE = 0x04000000
    RVA_US_BASE = 0x70000000
    SECTION_IDENTIFIER_TEXT = b'.text'
    STREAM_IDENTIFIER_STORAGE = b'#~'
    STREAM_IDENTIFIER_STRINGS = b'#Strings'
    STREAM_IDENTIFIER_US = b'#US'
    TABLE_FIELDS = 'Field'
    TABLE_FIELD_RVA = 'FieldRVA'

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
    # in general here:
    #
    # https://github.com/dnSpy/dnSpy/blob/2b6dcfaf602fb8ca6462b8b6237fdfc0c74ad994/dnSpy/dnSpy/Hex/Files/DotNet/DotNetTableSizes.cs
    TABLE_MAP = {
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

    # Custom exception class for parser exceptions
    class ASyncRATParserError(Exception):
        pass

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.get_file_data(file_path)
        self.table_map = self.get_table_map()
        self.fields_map = self.get_fields_map()
        self.config_addr_map = self.get_config_address_map()
        self.translated_config = self.get_translated_config()
        self.aes_salt = self.get_aes_salt()
        self.aes_key = self.get_aes_key()
        self.config = self.decrypt_config()

    # Given an initialization vector and ciphertext, creates a Cipher object
    # with the AES key and IV and decrypts the ciphertext
    def aes_decrypt(self, iv, ciphertext):
        logger.debug(
            f'Decrypting {ciphertext} with key {self.aes_key} and IV {iv}...')
        aes_cipher = Cipher(AES(self.aes_key), CBC(iv))
        decryptor = aes_cipher.decryptor()
        # Use a PKCS7 unpadder to remove padding from decrypted value
        # https://cryptography.io/en/latest/hazmat/primitives/padding/
        unpadder = PKCS7(self.AES_BLOCK_SIZE).unpadder()
        try:
            padded_text = decryptor.update(ciphertext) + decryptor.finalize()
            unpadded_text = unpadder.update(padded_text) + unpadder.finalize()
        except:
            raise self.ASyncRATParserError(
                f'Error decrypting ciphertext {ciphertext} with IV {iv} and key {self.aes_key}'
            )
        logger.debug(f'Decryption result: {unpadded_text}')
        return unpadded_text

    # Given the RVA for the AES salt from the FieldRVA table, calculates the
    # file offset of the salt value by subtracting the relative virtual address
    # of the .text section and adding the offset of the .text section, e.g.
    #
    # Salt RVA: 0x2050
    # Text section RVA: 0x2000
    # Text section offset: 0x0200
    # Salt offset = 0x2050 - 0x2000 + 0x0200
    #             = 0x0250
    def aes_salt_rva_to_offset(self, salt_rva):
        text_section_metadata_offset = self.data.find(
            self.SECTION_IDENTIFIER_TEXT)
        text_section_rva = self.data[text_section_metadata_offset +
                                     12:text_section_metadata_offset + 16]
        text_section_offset = self.data[text_section_metadata_offset +
                                        20:text_section_metadata_offset + 24]
        salt_translated_offset = salt_rva - self.bytes_to_int(
            text_section_rva) + self.bytes_to_int(text_section_offset)
        return salt_translated_offset

    # Converts a bytes object to an int object using the specified byteorder
    # (little-endian by default)
    def bytes_to_int(self, bytes, order=None):
        if order is None:
            order = self.BYTE_ORDER
        try:
            result = int.from_bytes(bytes, byteorder=order)
        except:
            raise self.ASyncRATParserError(
                f'Error parsing int from value: {bytes}')
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
        except:
            raise self.ASyncRATParserError(
                f'Error decoding bytes object to Unicode: {bytes}')
        return result

    # Given a translated config containing config field names and encrypted
    # and/or base64-encoded field values, decodes and decrypts encrypted fields
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
            except:
                b64_exception = True
            # If it was not base64-encoded, or if it is less than our min length
            # for ciphertext, leave the value as it is
            if b64_exception or len(decoded_val) < 48:
                continue
            # Otherwise, extract the IV from the 16 bytes after the HMAC
            # and the ciphertext from the rest of the data after the IV
            (iv, ciphertext) = decoded_val[32:48], decoded_val[48:]
            decrypted_config[decoded_k] = self.decode_bytes(
                self.aes_decrypt(iv, ciphertext))
            logger.debug(
                f'Key: {decoded_k}, Value: {decrypted_config[decoded_k]}')
        return decrypted_config

    # Given a field ID from the fields table, returns the relative virtual
    # address of the field, e.g.:
    #
    # Field RVA: 0x0400001D
    # Field ID = 0x1D
    # FieldRVA Entry for Field ID: 0x1D : 0x2050
    # Final RVA: 0x2050
    def field_id_to_field_rva(self, id):
        fieldrva_table_start = self.get_table_start(self.TABLE_FIELD_RVA)
        field_rva = None
        cur_offset = fieldrva_table_start
        for x in range(self.table_map[self.TABLE_FIELD_RVA]['num_rows']):
            field_id = self.bytes_to_int(self.data[cur_offset + 4:cur_offset +
                                                   6])
            field_rva = self.bytes_to_int(self.data[cur_offset:cur_offset + 4])
            if field_id == id:
                break
            cur_offset += self.table_map[self.TABLE_FIELD_RVA]['row_size']
        if field_rva is None:
            raise self.ASyncRATParserError(
                f'Could not find FieldRVA corresponding to ID {id}')
        return field_rva

    # Extracts the AES key from the payload using a regex pattern which looks
    # for the initialization of the key - specifically, the following ops:
    #
    # ldsfld	string Client.Settings::Key
    # newobj	instance void Client.Algorithm.Aes256::.ctor(string)
    def get_aes_key(self):
        logger.debug('Extracting encoded AES key value...')
        # Important to use DOTALL here (with all regexes to be safe) as because
        # we are working with bytes, if we do not set this, and the byte
        # sequence contains a special character (\n, \r, etc.), the search
        # will fail
        hit = search(self.PATTERN_AES_KEY, self.data, DOTALL)
        if hit is None:
            raise self.ASyncRATParserError('Could not find AES key pattern')

        # Since we already have a map of all fields, and have translated their
        # names into translated_config, to find the key value we take the RVA
        # of the key, subtract the #Strings stream base RVA, and then subtract
        # 1 to get the key's value in the field map, e.g.:
        #
        # Key RVA: 0x04000007
        # Key Field Map Index = 0x04000007 - 0x04000000 - 1
        # Key Field Name Value = fields_map[6]
        # Key Value = translated_config[fields_map[6]]
        key_field_offset = self.bytes_to_int(
            hit.groups()[0]) - self.RVA_STRINGS_BASE - 1
        key_val = self.translated_config[self.fields_map[key_field_offset][0]]
        logger.debug(f'AES encoded key value found: {key_val}')
        try:
            passphrase = b64decode(key_val)
        except:
            raise self.ASyncRATParserError(
                f'Error decoding key value {key_val}')
        logger.debug(f'AES passphrase found: {passphrase}')
        kdf = PBKDF2HMAC(SHA1(),
                         length=self.AES_KEY_LENGTH,
                         salt=self.aes_salt,
                         iterations=self.AES_ITERATIONS)
        try:
            key = kdf.derive(passphrase)
        except:
            raise self.ASyncRATParserError(
                f'Error deriving key from passphrase {passphrase}')
        logger.debug(f'AES key derived: {key.hex()}')
        return key

    # Extracts the AES salt from the payload using a regex pattern which looks
    # for the operations occurring directly before the initialization of the
    # salt byte array - specifically, the following ops:
    #
    # newarr	[mscorlib]System.Byte
    # dup
    # ldtoken	valuetype '<PrivateImplementationDetails>'...
    def get_aes_salt(self):
        logger.debug('Extracting AES salt value...')
        pre_offset = search(self.PATTERN_PRE_SALT_RVA, self.data, DOTALL)
        if pre_offset is None:
            raise self.ASyncRATParserError('Could not identify AES salt')

        # Salt RVA is in the last 4 bytes after the end of the ops in the regex
        salt_field_rva = self.data[pre_offset.end():pre_offset.end() + 4]
        salt_field_id = self.bytes_to_int(
            salt_field_rva) - self.RVA_STRINGS_BASE

        # Translate Field identifier to FieldRVA using FieldRVA table
        salt_field_rva = self.field_id_to_field_rva(salt_field_id)
        # Calculate file offset by finding location relative to .text section
        salt_offset = self.aes_salt_rva_to_offset(salt_field_rva)

        salt_value = self.data[salt_offset:salt_offset + self.AES_SALT_LENGTH]
        logger.debug(f'Found AES salt value: {salt_value.hex()}')
        return salt_value

    # Searches for the AsyncRAT configuration section in the Settings module,
    # and attempts to extract the RVAs of the config field names and values
    def get_config_address_map(self):
        logger.debug('Extracting the config address map...')
        config_mappings = []
        hit = search(self.PATTERN_CONFIG_START, self.data, DOTALL)
        if hit is None:
            raise self.ASyncRATParserError('Could not find start of config')
        config_start = hit.start()
        parsed_ops = self.get_string_from_offset(config_start, self.OPCODE_RET)
        parsed_rvas = findall(self.PATTERN_PARSED_RVAS, parsed_ops, DOTALL)
        for (us_rva, string_rva) in parsed_rvas:
            config_value_rva = self.bytes_to_int(us_rva)
            config_name_rva = self.bytes_to_int(string_rva)
            logger.debug(
                f'Found config item: ({config_value_rva}, {config_name_rva})')
            config_mappings.append((config_value_rva, config_name_rva))
        logger.debug('Successfully extracted config address map')
        return config_mappings

    # Extracts the Field table of the assembly, mapping the value of each
    # field from the #Strings stream to its offset in the Field table
    def get_fields_map(self):
        logger.debug('Extracting the fields map...')
        fields_map = []
        fields_start = self.get_table_start(self.TABLE_FIELDS)
        strings_start = self.get_stream_start(self.STREAM_IDENTIFIER_STRINGS)
        cur_offset = fields_start
        for x in range(self.table_map[self.TABLE_FIELDS]['num_rows']):
            try:
                field_offset = self.bytes_to_int(self.data[cur_offset +
                                                           2:cur_offset + 4])
                field_value = self.get_string_from_offset(strings_start +
                                                          field_offset)
                cur_offset += self.table_map[self.TABLE_FIELDS]['row_size']
            except:
                raise self.ASyncRATParserError(
                    'Error parsing Fields table\nCheck for obfuscation')
            logger.debug(f'Found field: {field_offset}, {field_value}')
            fields_map.append((field_value, field_offset))
        logger.debug('Successfully extracted fields map')
        return fields_map

    # Given a file path, reads in and stores binary contents from that path
    def get_file_data(self, file_path):
        logger.debug(f'Reading contents from: {file_path}')
        try:
            with open(file_path, 'rb') as fp:
                data = fp.read()
        except:
            raise self.ASyncRATParserError(
                f'Error reading from path: {file_path}')
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
        hit = self.data.find(self.PATTERN_METADATA_START)
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
        except:
            raise self.ASyncRATParserError(
                f'Could not extract string value from offset {str_offset} with delimiter {delimiter}'
            )
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
        table_map = self.TABLE_MAP.copy()
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
                    row_count_unpacked = self.bytes_to_int(row_count_packed)
                    table_map[table]['num_rows'] = row_count_unpacked
                    logger.debug(
                        f'Found {row_count_unpacked} rows for table {table}')
                    cur_offset += 4
                else:
                    table_map[table]['num_rows'] = 0
        except:
            raise self.ASyncRATParserError(
                'Could not get counts of rows from tables')
        logger.debug('Successfully extracted table map')
        return table_map

    # Given the name of a table in the Tables Stream, finds the offset pointing
    # to the start of that table
    def get_table_start(self, table_name):
        storage_stream_offset = self.get_stream_start(
            self.STREAM_IDENTIFIER_STORAGE)
        # Table Start = Table Stream Start + 4 bytes for the row size of each
        # table present in the assembly
        #             = (24 + storage stream start) + (4 * each table present in the assembly)
        tables_start_offset = storage_stream_offset + 24 + (4 * len([
            table for table in self.table_map
            if self.table_map[table]['num_rows'] > 0
        ]))

        table_offset = tables_start_offset
        for table in self.table_map:
            # Break if we have found our table
            if table == table_name:
                break
            # If we no longer find 'row_size', we are passed the point we should
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
            except:
                raise self.ASyncRATParserError(
                    f'Error translating RVAs {us_rva} and {strings_rva}')
        logger.debug('Successfully translated configuration')
        return translated_config

    # Returns a JSON dump of metadata and the decrypted configuration for a
    # payload
    def report(self):
        result_dict = {
            'file_path': self.file_path,
            'aes_key': self.aes_key.hex(),
            'aes_salt': self.aes_salt.hex(),
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
        except:
            return None
        strings_val = self.get_string_from_offset(val_offset)
        return strings_val

    # Given an RVA from the #US stream, extracts the value of the string
    # at that RVA
    def us_rva_to_us_val(self, us_rva):
        us_start = self.get_stream_start(self.STREAM_IDENTIFIER_US)
        # Strings in the #US stream are prefaced with 1-2 length bytes
        # If the length of the string is >= 128 bytes, 2 bytes will be used
        # to indicate length, and the first byte's most significant bit will be
        # set.
        #
        # So we first check if the first length byte & 0x80 (1000 0000) is 1.
        #
        # If so, then this indicates we are dealing with a long string, and we
        # grab the size from the 2 length bytes
        #
        # If not, then we can assume there is only 1 length byte to read from
        # and then skip over to get to the string
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
    for fp in args.file_paths:
        try:
            print(AsyncRATParser(fp).report())
        except:
            print(f'Exception occurred for {fp}')
            print(format_exc())
            continue
