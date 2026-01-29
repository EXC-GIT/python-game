import os
import json
from pathlib import Path


class ScoreManager:
    """Manages game scores and high scores"""
    
    def __init__(self, game_name="game"):
        self.game_name = game_name
        self.score_file = Path(f"scores/{game_name}_scores.json")
        self.score_file.parent.mkdir(exist_ok=True)
        self.high_scores = self._load_scores()
    
    def _load_scores(self):
        """Load scores from file"""
        try:
            if self.score_file.exists():
                with open(self.score_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading scores: {e}")
        return []
    
    def save_score(self, score, player_name="Player"):
        """Save a score to the high scores list"""
        try:
            # Add new score
            self.high_scores.append({
                "name": player_name,
                "score": int(score)
            })
            
            # Sort and keep top 10
            self.high_scores.sort(key=lambda x: x["score"], reverse=True)
            self.high_scores = self.high_scores[:10]
            
            # Save to file
            with open(self.score_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving score: {e}")
            return False
    
    def get_top_scores(self, count=5):
        """Get top N scores"""
        return self.high_scores[:count]
    
    def is_high_score(self, score):
        """Check if a score would make the high score list"""
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1]["score"]
    
    def get_rank(self, score):
        """Get the rank of a score"""
        for i, entry in enumerate(self.high_scores):
            if score > entry["score"]:
                return i + 1
        return len(self.high_scores) + 1
