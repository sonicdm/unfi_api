from unfi_api import settings
import os
from typing import List, Union
from pathlib import Path
class UnfiApiConfig:
    username: str = settings.config.get('username')
    password: str = settings.config.get('password')
    username: str = username if username else os.environ.get('UNFI_USERNAME')
    password: str = password if password else os.environ.get('UNFI_PASSWORD')
    query_output_path: str = Path(settings.config['query_output_path'])
    image_output_path: str = Path(settings.config['image_output_path'])
    abbreviations_path: str = Path(settings.config['abbreviations_path'])
    beautiful_soup_parser: str = "html.parser"
    max_threads: int = settings.config['max_threads']
    log_level: str = settings.config['log_level']
    log_path: str = Path(settings.config['log_path'])
    
    @classmethod
    def set_log_level(cls, level: Union[str,int]):
        """
        Set logging level
        choose from: CRITICAL, ERROR, WARNING, INFO, DEBUG
        """
        if level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG",
                     50,40,30,20,10,0]:
            cls.log_level = level
        else:
            raise ValueError("Invalid log level")
        
    @classmethod
    def set_log_path(cls, path: Union[str,Path]):
        """
        Set logging path
        """
        cls.log_path = Path(path)
        
    @classmethod
    def set_query_output_path(cls, path: Union[str,Path]):
        """
        Set query output path
        """
        cls.query_output_path = Path(path)
        
    @classmethod
    def set_image_output_path(cls, path: Union[str,Path]):
        """
        Set image output path
        """
        cls.image_output_path = Path(path)
        
    @classmethod
    def set_abbreviations_path(cls, path: Union[str,Path]):
        """
        Set abbreviations path
        """
        cls.abbreviations_path = Path(path)
    
    @classmethod
    def set_beautiful_soup_parser(cls, parser: Union[str,Path]):
        """
        Set beautiful soup parser
        """
        cls.beautiful_soup_parser = parser
        
    @classmethod
    def set_max_threads(cls, threads: int):
        """
        Set maximum number of threads
        """
        cls.max_threads = threads