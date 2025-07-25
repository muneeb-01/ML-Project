import sys

def error_message_detail(error, error_detail:sys):
    _ , _ , exc_tb  =  error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = "Error occured in Python Script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,
        line_number,
        str(error)
    )

    return error_message


class Custom_Exception(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message) 
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message


# to check if our exception class is working 

# import logging
# from logger import logger

# if __name__ == "__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("Divided by zero")
#         raise Custom_Exception(e, sys)