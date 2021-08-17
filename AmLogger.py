#! python
"""
#
# Date :		Today is 2021-05-02
# Creator :		This script Created by amqq.ir
# Info :		This is a lightweight and minimal class to handle logs and simple to use
# Requirement :	This script can be run on all os
#
# be happy :)
#
"""


class AmLogger:
    _datetime = __import__('datetime')

    class _TextTools:
        INFO_COLOR = '\033[96m'
        SUCCESS_COLOR = '\033[92m'
        SCRIPT_TEXT_COLOR = '\033[95m'
        WARNING_COLOR = '\033[93m'
        ERROR_COLOR = '\033[91m'
        NONE_COLOR = '\033[0m'
        BOLD_TEXT = '\033[1m'
        UNDERLINE_TEXT = '\033[4m'

    def __init__(self, colored_logs=True, save_logs=False, log_file="am_logger.log"):
        self.__colored_logs = colored_logs
        self.__save_logs = save_logs
        self.__log_file = log_file

    def Error(self, error_text):
        if self.__colored_logs:
            print(f"{self._TextTools.ERROR_COLOR} {self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
                  f" {error_text} {self._TextTools.NONE_COLOR}")
        else:
            print(
                f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _ERROR_ {error_text}")
        if self.__save_logs:
            self.__SaveLogs(f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _ERROR_ {error_text} \n")

    def Warning(self, warning_text):
        if self.__colored_logs:
            print(f"{self._TextTools.WARNING_COLOR} {self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
                  f" {warning_text} {self._TextTools.NONE_COLOR}")
        else:
            print(
                f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _WARNING_ {warning_text}")
        if self.__save_logs:
            self.__SaveLogs(f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _WARNING_ {warning_text} \n")

    def Info(self, info_text):
        if self.__colored_logs:
            print(f"{self._TextTools.INFO_COLOR} {self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
                  f" {info_text} {self._TextTools.NONE_COLOR}")
        else:
            print(
                f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _INFO_ {info_text}")
        if self.__save_logs:
            self.__SaveLogs(f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _INFO_ {info_text} \n")

    def Success(self, success_text):
        if self.__colored_logs:
            print(f"{self._TextTools.SUCCESS_COLOR} {self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')}"
                  f" {success_text} {self._TextTools.NONE_COLOR}")
        else:
            print(
                f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _SUCCESS_ {success_text}")
        if self.__save_logs:
            self.__SaveLogs(f"{self._datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S')} _SUCCESS_ {success_text} \n")

    def ScriptSays(self, script_text):
        if self.__colored_logs:
            print(f"{self._TextTools.SCRIPT_TEXT_COLOR} {script_text} {self._TextTools.NONE_COLOR}")
        else:
            print(f"SCRIPT : {script_text}")

    def __SaveLogs(self, log_text):
        with open(self.__log_file, "a") as Log_File:
            Log_File.write(log_text)
