import sys
import os
import pytest
from PIL import Image
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from python.ai.receipt_analyzer import ReceiptAnalyzer
from pdf2image import convert_from_path

@pytest.fixture
def analyzer():
    analyzer = ReceiptAnalyzer()
    yield analyzer

@pytest.mark.order(1)
def test_analyze_image(analyzer):
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data" , "documents","scontrino.png")
    print(file_path) #TODO debug
    image = Image.open(file_path)    

    result_file_path = analyzer.analyze_image(file_path=file_path)
    result_image = analyzer.analyze_image(image=image)
    
    assert isinstance(result_file_path,dict) #given the file path we must receive a dict
    assert isinstance(result_image,dict)  #given an image we must receive a dict

@pytest.mark.order(2)
def test_analyze_pdf(analyzer):
    
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"data" , "documents","dev-example.pdf")
    print(file_path) #TODO debug
    
    results = analyzer.analyze_pdf(file_path)
    
    images = convert_from_path(file_path)
    assert len(results) == len(images) #The function must release a num of results dict equal to num of pages 
    assert isinstance(results,list) #Results must be a list of dictionary


if __name__ == "__main__":
    pytest.main([__file__])