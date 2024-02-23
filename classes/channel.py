class Channel:
    def __init__(self, name):
        self.name = name
        self.members = {}
        
    def add_member(self, member, role="user"):
        if role not in ("admin", "moderator", "user"):
            print("Rôle invalide. Les rôles valides sont 'admin', 'moderator' et 'user'.")
            return
        if member in self.members:
            print(f"{member} est déjà membre de ce salon.")
        else:
            self.members[member] = role

    def remove_member(self, member):
        if member in self.members:
            del self.members[member]
        else:
            print(f"{member} n'est pas un membre de ce salon.")

    def edit_role(self, member, new_role):
        if member in self.members:
            self.members[member] = new_role
        else:
            print(f"{member} n'est pas un membre de ce salon.")

    def show_members(self):
        print("Membres du salon:")
        for member, role in self.members.items():
            print(f"{member} - {role}")

# Exemple d'utilisation
if __name__ == "__main__":
    channel1 = Channel("channel1")
    channel1.add_member("utilisateur1", "admin")
    channel1.add_member("utilisateur2", "moderator")
    channel1.add_member("utilisateur3")  # Par défaut, utilisateur normal
    channel1.show_members()  # Affiche les membres et leurs rôles

    channel1.edit_role("utilisateur1", "moderator")
    channel1.show_members()  # Affiche les membres et leurs rôles après la modification

    channel1.remove_member("utilisateur3")
    channel1.show_members()  # Affiche les membres après la suppression
