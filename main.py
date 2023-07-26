

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        return self.items.pop(0)

    def size(self):
        return len(self.items)


class Channel:
    def __init__(self, name):
        self.name = name
        self.subscribers = set()
        self.videos = []

    def add_subscriber(self, subscriber):
        self.subscribers.add(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def add_video(self, video):
        self.videos.append(video)
        self.notify_subscribers(video)

    def notify_subscribers(self, video):
        for subscriber in self.subscribers:
            subscriber.update(self, video)


class Observer:
    def __init__(self, name):
        self.name = name

    def update(self, channel, video):
        print(f"Notification for {self.name}: New video '{video}' added to channel '{channel.name}'.")


class MultiReaderQueue(Queue):
    def __init__(self):
        super().__init__()

        self.cartoon_queue = Queue()
        self.news_queue = Queue()
        self.channels = set()

    def add_channel(self, channel):
        self.channels.add(channel)

    def remove_channel(self, channel):
        self.channels.remove(channel)

    def add_item(self, item):
        category, video = item.split("-", 1)
        if category.lower() == "cartoon":
            self.cartoon_queue.enqueue(video)
        elif category.lower() == "news":
            self.news_queue.enqueue(video)
        self.notify_channels()

    def notify_channels(self):
        for channel in self.channels:
            if channel.name.lower() == "cartoon":
                while not self.cartoon_queue.is_empty():
                    video = self.cartoon_queue.dequeue()
                    channel.add_video(f"Cartoon-{video}")
            elif channel.name.lower() == "news":
                while not self.news_queue.is_empty():
                    video = self.news_queue.dequeue()
                    channel.add_video(f"News-{video}")
