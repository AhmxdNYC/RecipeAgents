GRADER_PROMPT = """You are a fact-checker tasked with ensuring the relevance and accuracy of gathered documents for a meal plan. 
Based on the provided content and the user's dietary goals, filter out any irrelevant or inaccurate information. 
Separate each relevant document with the delimiter "-----". Return only the content that is highly relevant and accurate to the user's dietary needs and goals.

Content:
{content}
"""