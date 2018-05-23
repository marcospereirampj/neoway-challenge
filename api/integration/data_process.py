# -*- coding: utf-8 -*-

import hashlib


class DataRestore:

    def restore(self, input_file_path):
        """
        Read a file, process and return dict with values.

        :param input_file_path: File path
        :return: True if successful restore
        """
        is_header = True
        headers = []

        try:
            # Read largest files
            with open(input_file_path, 'r') as file_object:
                for line in file_object:
                    if is_header:
                        headers = self._process_header(line)
                        is_header = False
                    else:
                        self._update_datebase(self._process_line(line, headers))
        except Exception as err:
            return "Failed to process file: {}.".format(err)

        return "File successfully processed."

    def _update_datebase(self, data):
        print(data)
        return

    def _process_header(self, line):
        """
        Process de header read from CSV file.

        :param line: header line.
        :return: values.
        """
        return [i.strip() for i in line.split(';')]

    def _process_line(self, line, headers):
        """
        Process a line read from CSV file.

        :param line: line from CSV file.
        :param headers: keys for result dict
        :return: values
        """
        fields = [i.strip() for i in line.split(';')]

        if len(headers) == len(fields):
            result = {}
            keys = []

            for item, field_name in enumerate(headers):
                result[field_name] = fields[item]
                keys.append(str(fields[item]))

            result['hash_object'] = self._create_hash_line(keys)

            return result

        return None

    def _create_hash_line(self, keys):
        """
        Create a hash identification for line

        :param keys: keys for hash generation.
        :return: hash
        """

        hash = hashlib.sha256(''.join(keys).encode('utf-8'))
        return hash.hexdigest()
