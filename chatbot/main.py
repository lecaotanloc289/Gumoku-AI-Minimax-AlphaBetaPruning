import json
import re
import random_responses


# Tải dữ liệu JSON từ file
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Lưu dữ liệu JSON
response_data = load_json("bot.json")


def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Kiểm tra tất cả các phản hồi
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Kiểm tra nếu có chứa từ ngữ yêu cầu
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1
        # Xác định số lượng từ khóa trong câu hỏi của người dùng và trong câu trả lời của chat
        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        # thêm số điểm vào danh sách
        score_list.append(response_score)

    # Tìm câu trả lời tốt nhất và trả về
    best_response = max(score_list)
    response_index = score_list.index(best_response)


    # Nếu không có phản hồi tốt, trả về 1 phản hồi bất kỳ
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    # Kiểm tra input rỗng
    if input_string == "":
        return "Please type something so we can chat :("
    
    
    return random_responses.random_string()


while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))
    if(user_input == "exit"):
        print("Bot: Goodbye!")
        break
    