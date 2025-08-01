import re
from transformers import pipeline
from pdf2image import convert_from_path
from PIL import Image
class ReceiptAnalyzer():

    def __init__(self):
        self.image_analyzer = pipeline("image-to-text", model="binery/donut_receipt_v1.20", trust_remote_code=True)

    def analyze_pdf(self,pdf_path:str) -> list[dict]:
        """Analze pdf by converting it into a list of images and analyze each image. Then add the results
        into a list and return it
        Args:
            pdf_path(str): The path of the pdf file
        Return:
            list[dict]: List of results obtained by analyzing each page of the pdf
        """

        images = convert_from_path(pdf_path)
        results = []
        for image in images:
            results.append(self.analyze_image(image))
        return results
        
    def analyze_image(self, file_path:str=None,image: Image = None) -> dict:
        """
        Analyze an image and format the results in a dictionary.
        If path is given it does ignore the image parameter
        Args:
            file_path (str): File path of the image to analyze.
            image (Image): image to analyze in Image PIL format 
        Returns:
            dict: Dictionary with extracted values:
            - invoice_number (str or None)
            - invoice_total (str or None)
            - items (list of dict):
                - description (str)
                - quantity (int)
                - total (float)
        """

        if file_path is not None:
           file_to_analyze = file_path
        elif image is not None:
            file_to_analyze = image
        else:
            raise TypeError("File path and image are both None. Specify at least one of this two parameter")
        
        result = self.image_analyzer(file_to_analyze)[0]['generated_text']
        
        # Extract main information
        invoice_no = re.search(r"<s_invoice_no>\s*(.*?)\s*</s_invoice_no>", result)
        invoice_total = re.search(r"<s_invoice_total>\s*(.*?)\s*</s_invoice_total>", result)

        # Extract line items
        line_items_raw = re.findall(
            r"<s_description>\s*(.*?)\s*</s_description>\s*<s_quantity>\s*(.*?)\s*</s_quantity>\s*<s_total>\s*(.*?)\s*</s_total>",
            result
        )

        # Build the final dictionary
        output = {
            "invoice_number": invoice_no.group(1) if invoice_no else None,
            "invoice_total": invoice_total.group(1) if invoice_total else None,
            "items": [
            {
                "description": desc,
                "quantity": int(qty),
                "total": float(total)
            }
            for desc, qty, total in line_items_raw
            ]
        }
        return output