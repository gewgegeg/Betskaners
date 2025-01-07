import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

class MatchPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def prepare_features(self, team1, team2, match):
        """Подготовка признаков для модели"""
        features = []
        
        # Базовые статистические показатели
        team1_winrate = team1.wins / team1.total_matches if team1.total_matches > 0 else 0.5
        team2_winrate = team2.wins / team2.total_matches if team2.total_matches > 0 else 0.5
        
        # Рейтинговая разница
        rating_diff = team1.rating - team2.rating
        
        # Форма команд (последние матчи)
        team1_recent_form = self._calculate_recent_form(team1)
        team2_recent_form = self._calculate_recent_form(team2)
        
        # История личных встреч
        h2h_advantage = self._calculate_h2h_advantage(team1, team2)
        
        # Усталость команд
        team1_fatigue = self._calculate_team_fatigue(team1)
        team2_fatigue = self._calculate_team_fatigue(team2)
        
        features.extend([
            rating_diff,
            team1_winrate,
            team2_winrate,
            team1_recent_form,
            team2_recent_form,
            h2h_advantage,
            team1_fatigue,
            team2_fatigue
        ])
        
        return np.array(features).reshape(1, -1)
    
    def _calculate_recent_form(self, team, matches_count=5):
        """Рассчитывает форму команды на основе последних матчей"""
        recent_matches = (
            team.home_matches + team.away_matches + team.won_matches
        )
        recent_matches.sort(key=lambda x: x.start_time, reverse=True)
        recent_matches = recent_matches[:matches_count]
        
        if not recent_matches:
            return 0.5
            
        wins = sum(1 for match in recent_matches if match.winner_id == team.id)
        return wins / len(recent_matches)
    
    def _calculate_h2h_advantage(self, team1, team2):
        """Рассчитывает преимущество в личных встречах"""
        h2h_matches = []
        
        # Собираем все матчи между командами
        for match in team1.home_matches + team1.away_matches:
            if (match.team1_id == team2.id or match.team2_id == team2.id) and match.winner_id:
                h2h_matches.append(match)
        
        if not h2h_matches:
            return 0
            
        # Сортируем по дате, берем последние матчи
        h2h_matches.sort(key=lambda x: x.start_time, reverse=True)
        h2h_matches = h2h_matches[:5]  # Последние 5 личных встреч
        
        team1_wins = sum(1 for match in h2h_matches if match.winner_id == team1.id)
        total_matches = len(h2h_matches)
        
        return (team1_wins / total_matches - 0.5) * 2  # Нормализуем в диапазон [-1, 1]
    
    def _calculate_team_fatigue(self, team):
        """Рассчитывает усталость команды на основе количества недавних матчей"""
        now = datetime.utcnow()
        recent_period = timedelta(days=7)
        
        recent_matches = [
            match for match in (team.home_matches + team.away_matches)
            if now - match.start_time <= recent_period
        ]
        
        # Больше матчей = больше усталость (отрицательный фактор)
        return -len(recent_matches) / 7  # Нормализуем по количеству дней
    
    def predict_winner(self, team1, team2, match):
        """Предсказывает победителя матча"""
        features = self.prepare_features(team1, team2, match)
        
        # Рассчитываем вероятность победы team1
        # Используем взвешенную сумму факторов
        weights = np.array([
            0.3,  # rating_diff
            0.15, # team1_winrate
            0.15, # team2_winrate
            0.1,  # team1_recent_form
            0.1,  # team2_recent_form
            0.1,  # h2h_advantage
            0.05, # team1_fatigue
            0.05  # team2_fatigue
        ])
        
        # Нормализуем признаки
        normalized_features = self.scaler.fit_transform(features)
        
        # Рассчитываем взвешенную сумму
        weighted_sum = np.dot(normalized_features, weights)
        
        # Применяем сигмоиду для получения вероятности
        probability = 1 / (1 + np.exp(-weighted_sum))
        
        return {
            'team1_win_probability': float(probability),
            'team2_win_probability': float(1 - probability),
            'prediction_confidence': float(abs(0.5 - probability) * 2),  # Уверенность в прогнозе
            'features_importance': {
                'rating_difference': features[0][0],
                'team1_winrate': features[0][1],
                'team2_winrate': features[0][2],
                'team1_recent_form': features[0][3],
                'team2_recent_form': features[0][4],
                'h2h_advantage': features[0][5],
                'team1_fatigue': features[0][6],
                'team2_fatigue': features[0][7]
            }
        } 