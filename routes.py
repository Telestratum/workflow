from flask import Flask, request, jsonify
from main import Queue, Channel, Observer, MultiReaderQueue
import json

app = Flask(__name__)

# Create instances of Queue, Channel, and MultiReaderQueue
queue = MultiReaderQueue()
que=Queue()
observer=Observer("name")
channel_cartoon = Channel("Cartoon")
channel_news = Channel("News")

queue.add_channel(channel_cartoon)
queue.add_channel(channel_news)

# Function to save subscriber details to subscribers.json
def save_subscribers(subscribers):
    with open("subscribers.json", "w") as file:
        json.dump(subscribers, file)

# Function to load subscriber details from subscribers.json
def load_subscribers():
    try:
        with open("subscribers.json", "r") as file:
            data = file.read()
            if data:
                return json.loads(data)
            else:
                return {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Function to save videos to a JSON file based on the category
def save_videos(category, video):
    filename = f"{category.lower()}.json"
    videos = load_videos(category)
    videos.append(video)
    with open(filename, "w") as file:
        json.dump(videos, file)

# Function to load videos from a JSON file based on the category
def load_videos(category):
    filename = f"{category.lower()}.json"
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Function to save the queue to queue.json
def save_queue(queue):
    with open("queue.json", "w") as file:
        json.dump(queue, file)

# Function to load the queue from queue.json
def load_queue():
    try:
        with open("queue.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Endpoint for admin to add a video
@app.route("/admin/add_video", methods=["POST"])
def admin_add_video():
    try:
        data = request.json
        password = data.get("password")
        if password != "12345":
            return jsonify({"error": "Invalid password. Access denied."}), 401

        category = data.get("category")
        video = data.get("video")

        if category and video and (category == "Cartoon" or category == "News"):
            queue.add_item(f"{category.lower()}-{video}")
            queue_videos = load_queue()
            queue_videos.append(f"{category.lower()}-{video}")
            save_queue(queue_videos)
            save_videos(category, video)

            return jsonify({"message": f"Video '{video}' added to the queue and stored in the '{category}' category."})
        else:
            return jsonify({"error": "Invalid category or video name."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for user subscription
@app.route("/user/subscribe", methods=["POST"])
def user_subscribe():
    try:
        data = request.json
        channel_name = data.get("channel_name")

        if channel_name and (channel_name == "Cartoon" or channel_name == "News"):
            name = data.get("name")

            if name:
                subscribers = load_subscribers()
                if channel_name == "Cartoon":
                    channel_cartoon.add_subscriber(name)
                elif channel_name == "News":
                    channel_news.add_subscriber(name)

                if channel_name in subscribers:
                    subscribers[channel_name].append(name)
                else:
                    subscribers[channel_name] = [name]

                save_subscribers(subscribers)
                return jsonify({"message": f"Subscribed to {channel_name} channel."})
            else:
                return jsonify({"error": "Name not provided."}), 400

        else:
            return jsonify({"error": "Invalid channel name."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=2229)
