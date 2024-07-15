import json
import os
from graph import AgentState , model 
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import GRADER_PROMPT

def grader_node(state: AgentState, use_saved_data: bool = True):
    directory = os.environ.get("GENERATED_DATA_DIR", "../tests/relevent_docs_save")
    filename = os.path.join(directory, "relevent_content.json")
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Use saved data if available
    if use_saved_data and os.path.exists(filename):
        print("From saved data!")
        with open(filename, 'r') as file:
            saved_data = json.load(file)
            return {"content": saved_data["content"]}
        
    content = "\n\n".join(state['content'] or [])
    messages = [
        SystemMessage(content=GRADER_PROMPT.format(content=content)),
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    
    # Split the response content by delimiter
    relevant_content = response.content.split('-----')
    
    # Ensure the relevant content is meaningful
    relevant_content = [doc.strip() for doc in relevant_content if len(doc.strip()) > 20]
    
    # If insufficient relevant content, trigger re-research
    print("content", content)
    print('-------------------')
    print("relevant_content", relevant_content)
    print('-------------------')
    print(len(state['content']), len(relevant_content))
    if len(relevant_content) <= len(state['content']) * 0.40:  # Example threshold: 40% relevant content
        return "research_plan"
    
    # Update state with filtered content
    state["content"] = relevant_content
    
    # Saving
    with open(filename, 'w') as file:
        json.dump({"content": relevant_content}, file)
    
    return "generate"



# Decides whether to generate new documents or research existing ones based on having enough relevant content

# Test
state = AgentState(
    task="I want to eat healthy and lose weight but I like pizza and donuts. I have a preference for greasy meals and I'm allergic to nuts and bananas.",
    plan="**Weekly Meal Plan:**\n\n**Day 1:**\n- **Breakfast:** Greek yogurt with mixed berries and a sprinkle of chia seeds.\n  - *Note:* Greek yogurt provides protein and probiotics, while berries offer antioxidants and fiber.\n- **Lunch:** Quinoa salad with roasted vegetables (bell peppers, zucchini, cherry tomatoes) and a lemon vinaigrette.\n  - *Note:* Quinoa is a great source of plant-based protein and fiber, while roasted vegetables add flavor and nutrients.\n- **Dinner:** Lentil and vegetable stir-fry with brown rice.\n  - *Note:* Lentils are high in protein and fiber, and the stir-fry provides a variety of vegetables for vitamins and minerals.\n\n**Day 2:**\n- **Breakfast:** Avocado toast on whole grain bread with a side of sliced tomatoes.\n  - *Note:* Avocado is rich in healthy fats and fiber, while whole grain bread offers complex carbohydrates.\n- **Lunch:** Chickpea and vegetable curry with a side of steamed broccoli.\n  - *Note:* Chickpeas are a good source of protein and fiber, and the curry provides flavorful spices and vegetables.\n- **Dinner:** Stuffed bell peppers with quinoa, black beans, corn, and salsa.\n  - *Note:* Bell peppers are packed with vitamins, and the quinoa and black beans offer a complete protein source.\n\n**Day 3:**\n- **Breakfast:** Smoothie bowl made with spinach, mango, and coconut milk, topped with granola.\n  - *Note:* Spinach adds nutrients, mango provides natural sweetness, and coconut milk offers healthy fats.\n- **Lunch:** Spinach and feta stuffed mushrooms with a side salad.\n  - *Note:* Mushrooms are low in calories and high in nutrients, while feta adds flavor and protein.\n- **Dinner:** Vegetable stir-fried noodles with tofu.\n  - *Note:* Tofu is a good source of plant-based protein, and the vegetables add color and texture.\n\n**Day 4:**\n- **Breakfast:** Oatmeal topped with sliced strawberries and a drizzle of honey.\n  - *Note:* Oatmeal is a filling breakfast option, and strawberries provide vitamin C and antioxidants.\n- **Lunch:** Caprese salad with fresh mozzarella, tomatoes, basil, and balsamic glaze.\n  - *Note:* Mozzarella offers protein, while tomatoes and basil add freshness and flavor.\n- **Dinner:** Eggplant parmesan with a side of mixed greens salad.\n  - *Note:* Eggplant is a low-calorie vegetable, and the salad adds fiber and nutrients.\n\n**Day 5:**\n- **Breakfast:** Whole grain pancakes with maple syrup and a side of fresh fruit.\n  - *Note:* Whole grain pancakes offer complex carbs, while fruit adds natural sweetness and vitamins.\n- **Lunch:** Lentil soup with a side of whole grain bread.\n  - *Note:* Lentils are high in protein and fiber, making them a filling and nutritious choice.\n- **Dinner:** Zucchini noodles with marinara sauce and grilled portobello mushrooms.\n  - *Note:* Zucchini noodles are a low-carb alternative, and portobello mushrooms provide a meaty texture.\n\n**Day 6:**\n- **Breakfast:** Chia seed pudding with sliced peaches and a sprinkle of cinnamon.\n  - *Note:* Chia seeds are rich in omega-3 fatty acids and fiber, while peaches offer vitamins and minerals.\n- **Lunch:** Black bean and corn salad with a lime-cilantro dressing.\n  - *Note:* Black beans are a good source of plant-based protein, and the salad is refreshing and flavorful.\n- **Dinner:** Vegetable and tofu stir-fry with quinoa.\n  - *Note:* Tofu provides protein, while the stir-fry offers a variety of vegetables for nutrients.\n\n**Day 7:**\n- **Breakfast:** Scrambled eggs with saut\u00e9ed spinach and whole grain toast.\n  - *Note:* Eggs are a good source of protein, and spinach adds vitamins and minerals.\n- **Lunch:** Roasted vegetable wrap with hummus in a whole wheat tortilla.\n  - *Note:* Roasted vegetables provide flavor and nutrients, while hummus adds protein and creaminess.\n- **Dinner:** Cauliflower crust pizza with assorted vegetables and a side salad.\n  - *Note:* Cauliflower crust is a low-carb alternative, and the vegetables offer a variety of nutrients.\n\n**Notes:**\n- Stay hydrated throughout the day by drinking plenty of water.\n- Portion control is key for weight loss, so be mindful of serving sizes.\n- Incorporate a variety of colorful fruits and vegetables for a range of nutrients.\n- Consider incorporating physical activity into your routine for overall health and weight loss.", 
    generated="", 
    content=["Healthy Pita Pizza. Margherita Flatbread. Pizza can be much healthier if you use the right toppings. Check my list of 45 healthy pizza toppings to enjoy and ones to avoid.", "Place a piece of oiled parchment paper on top of the dough ball (oiled side onto the dough) and roll it into a 10-inch circle. The parchment paper prevents the raw dough from sticking to the paper. Freeze the pizza base while making the yogurt dip. In a small bowl, stir yogurt, maple syrup, and cinnamon.", "How to Meal Plan for a Healthy, Balanced Diet\nPlanning healthy meals isn't difficult, but if you're not used to it, the planning can take a little practice. Download the 1-Week Healthy and Balanced Meal Plan\nDownload the Meal Plan\nDay 1\nBreakfast\nMacronutrients: approximately 327 calories, 18 grams protein, 41 grams carbohydrates, and 11 grams fat\nSnack\nMacronutrients: 324 calories, 14 grams protein, 62 grams carbohydrates, 4 grams fat\nLunch\nMacronutrients: 396 calories, 41 grams protein, 18 grams carbohydrates, 18 grams fat\nSnack\nMacronutrients: 192 calories, 7 grams protein, 31 grams carbohydrates, 5 grams fat\nDinner\nMacronutrients: 399 calories, 34 grams protein, 57 grams carbohydrates, 4 grams fat\nSnack\nMacronutrients: 302 calories, 3 grams protein, 49 grams carbohydrates, 12 grams fat\nDaily Totals: 1,940 calories, 117 grams protein, 258 grams carbohydrates, 55 grams fat\nNote that beverages are not included in this meal plan."],
    revision_number=0, 
    max_revisions=2
)

print(grader_node(state, use_saved_data=False))