function updateLiveMatches() {
    fetch('/api/v1/matches/live')
        .then(response => response.json())
        .then(data => {
            const matchesContainer = document.querySelector('.row-cols-1');
            if (!matchesContainer) return;

            if (data.matches.length === 0) {
                matchesContainer.innerHTML = `
                    <div class="alert alert-info text-center">
                        В данный момент нет активных матчей
                    </div>`;
                return;
            }

            const matchesHTML = data.matches.map(match => `
                <div class="col">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${match.tournament_name}</h5>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="team">
                                    <img src="${match.team1.logo_url}" alt="${match.team1.name}" class="team-logo">
                                    <span>${match.team1.name}</span>
                                </div>
                                <div class="score">
                                    <span class="badge bg-danger">LIVE</span>
                                    <div class="match-score">
                                        ${match.score_team1} : ${match.score_team2}
                                    </div>
                                </div>
                                <div class="team text-end">
                                    <span>${match.team2.name}</span>
                                    <img src="${match.team2.logo_url}" alt="${match.team2.name}" class="team-logo">
                                </div>
                            </div>
                            <div class="text-center mt-3">
                                <a href="/predictions/${match.id}" class="btn btn-primary">
                                    Сделать прогноз
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');

            matchesContainer.innerHTML = matchesHTML;
        })
        .catch(error => console.error('Error:', error));
}

// Обновляем каждые 30 секунд
setInterval(updateLiveMatches, 30000);

// Обновляем при загрузке страницы
document.addEventListener('DOMContentLoaded', updateLiveMatches); 