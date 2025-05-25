from typing import Any, Text, Dict, List
import json, re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import difflib

from rasa_sdk.events import SlotSet


class ActionProvideFoodInfo(Action):

    # Trả về tên của action, dùng tên này để gọi đúng action tương ứng khi dự đoán
    # Ni là type hint -> hàm sẽ trả về 1 giá trị kiểu text
    def name(self) -> Text:
        return "action_provide_food_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(tracker.get_latest_entity_values("food_name"), None)
        if not food_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về món gì vậy?")
            return []

        # Load data tu JSON
        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                msg = f"🍽 {food['name']}\n"
                msg += f"{food['description']}. Địa chỉ nằm ở: {', '.join(food['addresses'])}. Giá trung bình ở đà nẵng là {food['average_price']}k bạn nhé💰!"
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về món {food_name}. Mình sẽ gắng cập nhật thông tin để giải đáp thắc mắc cho bạn nhé!")
        return []

class ActionListManyFoods(Action):
    def name(self) -> Text:
        return "action_list_many_foods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_foods_indices = tracker.get_slot("shown_foods_indices")

        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        if not shown_foods_indices:
            shown_foods_indices = []

        foods_per_page = 7

        if len(shown_foods_indices) >= len(foods):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các món ăn đặc sản của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_foods_indices", [])]  # Reset lại slot

        remaining_indices = [i for i in range(
            len(foods)) if i not in shown_foods_indices]
        num_to_show = min(foods_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        # Update danh sách các món đã hiển thị
        shown_foods_indices.extend(indices_to_show)

        response = "\n"
        for idx in indices_to_show:
            response += f"{foods[idx]['name']}; "
        response += "\nBạn muốn biết thêm thông tin chi tiết về món nào? Hãy nhắn tên món ăn để mình giới thiệu nhé!"

        dispatcher.utter_message(text=response)

        # Lưu lại danh sách các món đã hiển thị
        return [SlotSet("shown_foods_indices", shown_foods_indices)]


class ActionProvideFoodPrice(Action):
    def name(self) -> Text:
        return "action_provide_food_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(tracker.get_latest_entity_values("food_name"), None)
        if not food_name:
            dispatcher.utter_message(text="Bạn muốn hỏi giá món gì vậy?")
            return []

        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                dispatcher.utter_message(
                    text=f"💰 Món {food['name']} có giá trung bình khoảng {food['average_price']}k bạn nhé!")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin giá của món {food_name}.")
        return []


class ActionProvideFoodLocation(Action):

    def name(self) -> Text:
        return "action_provide_food_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(tracker.get_latest_entity_values("food_name"), None)
        if not food_name:
            dispatcher.utter_message(
                text="Bạn muốn tìm địa điểm của món nào vậy?")
            return []

        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                dispatcher.utter_message(
                    text=f"📍Bạn có thể thưởng thức {food['name']} tại: {', '.join(food['addresses'])}.")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa biết địa điểm bán món {food_name} rồi :(")
        return []
    
# FAQ Food
class ActionAnswerFoodFAQ(Action):

    def name(self) -> Text:
        return "action_answer_food_faq" 
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_question = tracker.latest_message.get("text", "").lower()

        # Doc file excel
        df = pd.read_excel("actions/data/100_questions_answers_grabfood.xlsx")
        questions = df["Question"].astype(str).tolist()
        answers = df["Answer"].astype(str).tolist()

        # So khop voi cau hoi gan nhat
        closest = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.5)
        if closest: 
            idx = questions.index(closest[0])
            dispatcher.utter_message(text=answers[idx])
        else:
            dispatcher.utter_message(text="Xin lỗi, mình chưa rõ câu hỏi đó. Bạn có thể hỏi lại rõ hơn được không?")

        return []