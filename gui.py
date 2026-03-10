










def load_best_times(self):
        if os.path.exists("best_times.json"):
            with open("best_times.json", "r") as f:
                return json.load(f)
        return {"10x10": float('inf'), "16x16": float('inf'), "20x20": float('inf')}
def save_best_times(self):
        with open("best_times.json", "w") as f:
            json.dump(self.best_times, f)

