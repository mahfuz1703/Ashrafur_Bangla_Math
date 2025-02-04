import re

from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Fix MathJax formatting in the dataset'

    def handle(self, *args, **kwargs):
        # Function to fix incorrect MathJax format
        def fix_mathjax(text):
            # pattern = r'\$\$(.*?)\$\$'
            pattern_dollar = r'\$\$(.*?)\$\$'

            # pattern2 = r'\[\s*(.*?)\s*\]'
            pattern_square = r'\[\s*(.*?)\s*\]'

            if re.search(pattern_dollar, text):  # Check if text matches $$...$$ pattern
                return re.sub(pattern_dollar, r'\\[ \1 \\]', text)
            elif re.search(pattern_square, text):  # Check if text matches [ ... ] pattern
                return re.sub(pattern_square, r'\\[ \1 \\]', text)
            
            return text
        
        # def escape_backslashes(text):
        #     return text.replace("\\", "\\\\")
        

        input_text = r"[3 \times 3 \times 3 \times 3 \times 3 = 3^5]"
        output_text = fix_mathjax(input_text)

        print("Orginal text = ", input_text)
        print("\nConverted Text: ", output_text)



# # Load dataset (CSV or Database)
# df = pd.read_csv("your_dataset.csv")  # Replace with your file path

# # Apply formatting fix to both 'Problem' and 'Solution' columns
# tqdm.pandas()
# df["Problem"] = df["Problem"].progress_apply()
# df["Solution"] = df["Solution"].progress_apply()

# # Save corrected dataset
# df.to_csv("corrected_dataset.csv", index=False)
