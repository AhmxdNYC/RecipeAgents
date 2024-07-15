HALLUCINATION_GRADER_PROMPT = """You are a meticulous reviewer tasked with ensuring the factual accuracy of a generated meal plan. 
Your goal is to verify each statement and sentence in the generated content against the provided reference documents. 
Please provide 'true' or 'false' for every statement and sentence, indicating whether it is supported by the information in the documents.

Instructions:
1. Carefully read through the generated meal plan.
2. For each statement or sentence, determine if it is factually accurate based on the provided documents.
3. Respond with 'true' if the statement is supported by the documents, or 'false' if it is not.

Generated Meal Plan:
{generated}

Reference Documents:
{content}"""