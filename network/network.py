import collections

class Member:
    def __init__(self, name):
        self.name = name
        self.following = set()
        self.likes_given = 0
        self.likes_received = 0
        self.comments_given = 0
        self.comments_received = 0

    def add_follower(self, member):
        self.following.add(member)
        member.following.add(self)  # Establishing the reverse relationship
        print(f"{self.name} is now following {member.name}")
        print(f"{member.name} is now following {self.name}")

    def like(self, member):
        self.likes_given += 1
        member.likes_received += 1

    def comment(self, member):
        self.comments_given += 1
        member.comments_received += 1

    def likes_of(self, member):
        if member in self.following:
            return 1
        return 0

    def comments_of(self, member):
        if member in self.following:
            return 0.1
        return 0

class Network:
    def __init__(self):
        self.members = {}

    def add_member(self, member):
        self.members[member.name] = member

    def calculate_engagement_rate(self, member):
        if member.likes_received + member.comments_received == 0:
            return 0
        return (member.likes_given + member.comments_given) / (member.likes_received + member.comments_received)

    def influence(self, member1, member2):
        if member1 == member2:
            return 100.0
        if member1 not in self.members or member2 not in self.members:
            return 0
        engagement_rate = self.calculate_engagement_rate(member1)
        if engagement_rate == 0:
            return 0
        return (member1.likes_of(member2) + member1.comments_of(member2)) / engagement_rate

    def shortest_path(self, member1, member2):
        if member1 == member2:
            return [member1]
        if member1 not in self.members:
            return None
        if member2 not in self.members:
            return None
        visited = set()
        queue = collections.deque([(member1, [member1])])
        while queue:
            current, path = queue.popleft()
            if current == member2:
                return path
            visited.add(current)
            for neighbor in current.following:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return None

    def highest_engagement_path(self, member1, member2):
        if member1 == member2:
            return [member1], 100.0
        if member1 not in self.members or member2 not in self.members:
            return [], 0
        paths = []
        max_engagement = 0
        for neighbor in member1.following:
            path, engagement = self.highest_engagement_path(neighbor, member2)
            if path is not None and engagement > max_engagement:
                max_engagement = engagement
                paths = [path]
            elif path is not None and engagement == max_engagement:
                paths.append(path)
            path.insert(0, member1)
        if not paths:
            return [], 0
        return paths[0], max_engagement

# Create members
member1 = Member("member1")
member2 = Member("member2")
member3 = Member("member3")
member4 = Member("member4")
member5 = Member("member5")

# Connect members
member1.add_follower(member2)
member1.add_follower(member3)
member2.add_follower(member4)
member3.add_follower(member4)
member4.add_follower(member5)

# Add members to the network
network = Network()
network.add_member(member1)
network.add_member(member2)
network.add_member(member3)
network.add_member(member4)
network.add_member(member5)

# Calculate influence, shortest path, and highest engagement path
print("Influence of member 1 on member 2:", round(network.influence(member1, member2), 2))

path1_5 = network.shortest_path(member1, member5)
if path1_5 is not None:
    print("Shortest path between member1 and member5:", [member.name for member in path1_5])
else:
    print("Shortest path between member1 and member5: None")

highest_engagement_path1_5 = network.highest_engagement_path(member1, member5)
if highest_engagement_path1_5 is not None:
    paths, engagement = highest_engagement_path1_5
    print("Highest engagement path between member 1 and member 5:", [member.name for member in paths])
    print("Engagement:", round(engagement, 2))
else:
    print("Highest engagement path between member 1 and member 5: None")

path2_5 = network.shortest_path(member2, member5)
if path2_5 is not None:
    print("Shortest path between member2 and member5:", [member.name for member in path2_5])
else:
    print("Shortest path between member2 and member5: None")

highest_engagement_path2_5 = network.highest_engagement_path(member2, member5)
if highest_engagement_path2_5 is not None:
    paths, engagement = highest_engagement_path2_5
    print("Highest engagement path between member 2 and member 5:", [member.name for member in paths])
    print("Engagement:", round(engagement, 2))
else:
    print("Highest engagement path between member 2 and member 5: None")                                                        