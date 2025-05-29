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
        with open("actions/data/specialty_foods.json", "r", encoding="utf-8") as f:
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

        with open("actions/data/specialty_foods.json", "r", encoding="utf-8") as f:
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

        with open("actions/data/specialty_foods.json", "r", encoding="utf-8") as f:
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

        with open("actions/data/specialty_foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                dispatcher.utter_message(
                    text=f"📍Bạn có thể thưởng thức {food['name']} tại: {', '.join(food['addresses'])}.")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa biết địa điểm bán món {food_name} rồi :(")
        return []
    

# Coffee and Milk tea
class ActionListManyCoffee(Action):
    def name(self) -> Text:
        return "action_list_many_coffees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_coffees_indices = tracker.get_slot("shown_coffees_indices")

        with open("actions/data/danang_coffee_milktea_selenium.json", "r", encoding="utf-8") as f:
            coffees = json.load(f)

        if not shown_coffees_indices:
            shown_coffees_indices = []

        coffees_per_page = 7

        if len(shown_coffees_indices) >= len(coffees):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các quán cà phê/ trà sữa nổi tiếng của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_coffees_indices", [])]  # Reset lại slot

        remaining_indices = [i for i in range(
            len(coffees)) if i not in shown_coffees_indices]
        num_to_show = min(coffees_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        # Update danh sách các quán đã hiển thị
        shown_coffees_indices.extend(indices_to_show)

        response = "\n"
        response = "Đây là các quán cà phê mà bạn nên thử ghé qua một lần nhaaaaa: \n"
        for idx in indices_to_show:
            response += f"{coffees[idx]['name']}; "

        dispatcher.utter_message(text=response)

        # Lưu lại danh sách các món đã hiển thị
        return [SlotSet("shown_coffees_indices", shown_coffees_indices)]

class ActionProvideCoffeeInfo(Action):

    def name(self) -> Text:
        return "action_provide_coffee_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        coffee_name = next(tracker.get_latest_entity_values("coffee_name"), None)
        if not coffee_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về quán cà phê nào vậy?")
            return []

        with open("actions/data/danang_coffee_milktea_selenium.json", "r", encoding="utf-8") as f:
            coffees = json.load(f)

        for coffee in coffees:
            if coffee_name.lower().strip() in coffee["name"].lower():
                msg = f"☕ {coffee['name']} có điểm đánh giá trung bình {coffee['rating']}/10."

                if coffee['address'] != "N/A" and coffee['district'] != "N/A":
                    msg += f" Địa chỉ quán là {coffee['address']}, {coffee['district']}."
                else:
                    msg += " Đây là hệ thống quán và không có địa chỉ cụ thể."

                msg += f" Bạn có thể xem thêm chi tiết tại: {coffee['URL']}."
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về quán {coffee_name}. Mình sẽ cố gắng cập nhật thêm nhé!")
        return []

class ActionProvideCoffeeLocation(Action):

    def name(self) -> Text:
        return "action_provide_coffee_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        coffee_name = next(tracker.get_latest_entity_values("coffee_name"), None)
        if not coffee_name:
            dispatcher.utter_message(
                text="Bạn muốn tìm địa điểm của quán nào vậy?")
            return []

        with open("actions/data/danang_coffee_milktea_selenium.json", "r", encoding="utf-8") as f:
            coffees = json.load(f)

        found_coffee_info = False

        for coffee in coffees:
            if coffee_name.lower().strip() in coffee["name"].lower():
                found_coffee_info = True

                if coffee["address"] and coffee["address"].lower() != "n/a":
                    dispatcher.utter_message(
                        text=f"📍Bạn có thể ghé {coffee['name']} tại: {coffee['address']}."
                    )
                else:
                    dispatcher.utter_message(
                        text=f"Xin lỗi, mình chưa có thông tin địa điểm cụ thể cho quán {coffee['name']} rồi :("
                    )
                return [SlotSet("coffee_name", None)]

        if not found_coffee_info:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình chưa có thông tin về quán {coffee_name}. Bạn có chắc đó là tên quán không?"
            )
        
        return [SlotSet("coffee_name", None)] # Tùy chọn: reset slot ngay cả khi không tìm thấy

class ActionFilterCoffeeByRating(Action):

    def name(self) -> Text:
        return "action_filter_coffee_by_rating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị entity rating từ câu hỏi
        rating_str = next(tracker.get_latest_entity_values("rating"), None)
        if rating_str is None:
            dispatcher.utter_message(text="Bạn muốn tìm các quán có điểm rating lớn hơn bao nhiêu?")
            return []

        try:
            threshold = float(rating_str)
        except ValueError:
            dispatcher.utter_message(text="Mình không hiểu điểm bạn muốn tìm là bao nhiêu. Bạn thử lại nhé.")
            return []

        # Đọc file dữ liệu JSON
        with open("actions/data/danang_coffee_milktea_selenium.json", "r", encoding="utf-8") as f:
            coffees = json.load(f)

        # Lọc quán có rating lớn hơn threshold
        filtered = [
            f"{coffee['name']} (Rating: {coffee['rating']})"
            for coffee in coffees
            if float(coffee.get("rating", 0)) > threshold
        ]

        # Trả lời người dùng
        if filtered:
            message = f"Các quán có rating > {threshold}:\n- " + "\n- ".join(filtered)
        else:
            message = f"Không tìm thấy quán nào có điểm rating lớn hơn {threshold}."

        dispatcher.utter_message(text=message)
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
    

# Streetfood
class ActionListManyStreetFood(Action):
    def name(self) -> Text:
        return "action_list_many_streetfoods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_streetfoods_indices = tracker.get_slot("shown_streetfoods_indices")

        with open("actions/data/danang_streetfood_selenium.json", "r", encoding="utf-8") as f:
            streetfoods = json.load(f)

        if not shown_streetfoods_indices:
            shown_streetfoods_indices = []

        streetfoods_per_page = 7

        if len(shown_streetfoods_indices) >= len(streetfoods):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các quán ăn vặt nổi tiếng của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_streetfoods_indices", [])]  # Reset lại slot

        remaining_indices = [i for i in range(
            len(streetfoods)) if i not in shown_streetfoods_indices]
        num_to_show = min(streetfoods_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        # Update danh sách các quán đã hiển thị
        shown_streetfoods_indices.extend(indices_to_show)

        response = "\n"
        response = "Đây là các quán ăn vặt mà bạn nên thử ghé qua một lần nhaaaaa: \n"
        for idx in indices_to_show:
            response += f"{streetfoods[idx]['name']}; "

        dispatcher.utter_message(text=response)

        # Lưu lại danh sách các món đã hiển thị
        return [SlotSet("shown_streetfoods_indices", shown_streetfoods_indices)]
    
class ActionProvideStreetFoodInfo(Action):

    def name(self) -> Text:
        return "action_provide_streetfood_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        streetfood_name = next(tracker.get_latest_entity_values("streetfood_name"), None)
        if not streetfood_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về quán ăn vặt nào vậy?")
            return []

        with open("actions/data/danang_streetfood_selenium.json", "r", encoding="utf-8") as f:
            streetfoods = json.load(f)

        for streetfood in streetfoods:
            if streetfood_name.lower().strip() in streetfood["name"].lower():
                msg = f"🍗 {streetfood['name']} có điểm đánh giá trung bình {streetfood['street_rating']}/10."

                if streetfood['address'] != "N/A" and streetfood['district'] != "N/A":
                    msg += f" Địa chỉ quán là {streetfood['address']}, {streetfood['district']}."
                else:
                    msg += " Đây là hệ thống quán và không có địa chỉ cụ thể."

                msg += f" Bạn có thể xem thêm chi tiết tại: {streetfood['URL']}."
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về quán {streetfood_name}. Mình sẽ cố gắng cập nhật thêm nhé!")
        return []
    
class ActionProvideStreetFoodLocation(Action):

    def name(self) -> Text:
        return "action_provide_streetfood_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        streetfood_name = next(tracker.get_latest_entity_values("streetfood_name"), None)
        if not streetfood_name:
            dispatcher.utter_message(
                text="Bạn muốn tìm địa điểm của quán nào vậy?")
            return []

        with open("actions/data/danang_streetfood_selenium.json", "r", encoding="utf-8") as f:
            streetfoods = json.load(f)

        found_streetfood_info = False

        for streetfood in streetfoods:
            if streetfood_name.lower().strip() in streetfood["name"].lower():
                found_streetfood_info = True

                if streetfood["address"] and streetfood["address"].lower() != "n/a":
                    dispatcher.utter_message(
                        text=f"📍Bạn có thể ghé {streetfood['name']} tại: {streetfood['address']}."
                    )
                else:
                    dispatcher.utter_message(
                        text=f"Xin lỗi, mình chưa có thông tin địa điểm cụ thể cho quán {streetfood['name']} rồi :("
                    )
                return [SlotSet("streetfood_name", None)]

        if not found_streetfood_info:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình chưa có thông tin về quán {streetfood_name}. Bạn có chắc đó là tên quán không?"
            )
        
        return [SlotSet("streetfood_name", None)] # Tùy chọn: reset slot ngay cả khi không tìm thấy
    
class ActionFilterStreetFoodByRating(Action):

    def name(self) -> Text:
        return "action_filter_streetfood_by_rating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị entity rating từ câu hỏi
        rating_str = next(tracker.get_latest_entity_values("street_rating"), None)
        if rating_str is None:
            dispatcher.utter_message(text="Bạn muốn tìm các quán có điểm rating lớn hơn bao nhiêu?")
            return []

        try:
            threshold = float(rating_str)
        except ValueError:
            dispatcher.utter_message(text="Mình không hiểu điểm bạn muốn tìm là bao nhiêu. Bạn thử lại nhé.")
            return []

        # Đọc file dữ liệu JSON
        with open("actions/data/danang_streetfood_selenium.json", "r", encoding="utf-8") as f:
            streetfoods = json.load(f)

        # Lọc quán có rating lớn hơn threshold
        filtered = [
            f"{streetfood['name']} (Rating: {streetfood['street_rating']})"
            for streetfood in streetfoods
            if float(streetfood.get("street_rating", 0)) > threshold
        ]

        # Trả lời người dùng
        if filtered:
            message = f"Các quán có rating > {threshold}:\n- " + "\n- ".join(filtered)
        else:
            message = f"Không tìm thấy quán nào có điểm rating lớn hơn {threshold}."

        dispatcher.utter_message(text=message)
        return []